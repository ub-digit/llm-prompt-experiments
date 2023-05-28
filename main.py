import sys
from langchain.llms import TextGenerationWebui, OpenAI
import prompt as pr
from langchain import PromptTemplate, LLMChain
from flexible_json_parser import find_all_json
import json
import argparse
import requests
import os
import dotenv
from bs4 import BeautifulSoup

dotenv.load_dotenv()

MODEL_TYPE="wizard-vicuna"
DEBUG=False
PRINTRESULT=False
OPTIONS={}
OPTION_TYPES={
    "table": str,
    "list": str,
    "textonly": bool,
    "segment": int,
    "_default": str
}

def debug(msg):
    if DEBUG:
        print(msg)

def fetch_table_from_url_data(soup):
    if OPTIONS["table"] != True:
        table = soup.select(OPTIONS["table"])
        if len(table) == 0:
            # Return the text content of the page if the table is not found
            return None
        if OPTIONS["textonly"] == True:
            input = table[0].get_text("   ").strip()
        else:
            input = str(table[0])
    else:
        # Get the text content of the largest table on the page
        tables = soup.find_all("table")
        if len(tables) == 0:
            # Return the text content of the page if there are no tables
            return soup.get_text().strip()
        input = tables[0].get_text().strip()
        for table in tables:
            if len(table.get_text().strip()) > len(input):
                if OPTIONS["textonly"] == True:
                    input = table.get_text("   ").strip()
                else:
                    input = str(table)
    return input

# Same as fetch_table_from_url_data except for lists (ul and ol)
def fetch_list_from_url_data(soup):
    if OPTIONS["list"] != True:
        list = soup.select(OPTIONS["list"])
        if len(list) == 0:
            # Return the text content of the page if the list is not found
            return None
        if OPTIONS["textonly"] == True:
            input = list[0].get_text("   ").strip()
        else:
            input = str(list[0])
    else:
        # Get the text content of the largest list on the page
        lists = soup.find_all(["ul", "ol"])
        if len(lists) == 0:
            # Return the text content of the page if there are no lists
            return soup.get_text().strip()
        input = lists[0].get_text().strip()
        for list in lists:
            if len(list.get_text().strip()) > len(input):
                if OPTIONS["textonly"] == True:
                    input = list.get_text("   ").strip()
                else:
                    input = str(list)
    return input

# Use requests and beautifulsoup to fetch the input from the text content of a URL
def fetch_input_from_url(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    # There is an option "table"
    # If the option "table" is True, get the text content of the largest table on the page
    # If the option "table" has a CSS selector, get the text content of the table that matches the CSS selector
    # If the option "table" is False or not set, get the text content of the page
    if "table" in OPTIONS:
        input = fetch_table_from_url_data(soup)
        if input is None:
            return soup.get_text().strip()
    elif "list" in OPTIONS:
        input = fetch_list_from_url_data(soup)
        if input is None:
            return soup.get_text().strip()
    else:
        # Get the text content of the page
        input = soup.get_text().strip()
        # If the text content is empty, raise an exception
        if input == "":
            raise Exception("The text content of the URL is empty")
    return input

# Parse options parameter from the command line
# If is an array of options. Each option is a string in the format "key=value" or just "key" in which case the value is True
def parse_options(options):
    global OPTIONS
    if options is None:
        return
    for option in options:
        if "=" in option:
            key, value = option.split("=")
            # Convert the value to the type specified in OPTION_TYPES
            if key in OPTION_TYPES:
                OPTIONS[key] = OPTION_TYPES[key](value)
            else:
                OPTIONS[key] = value
        else:
            OPTIONS[option] = True

def run(prompttype, input, llm):
    # If the option "segment" is set, run the input through the segmenter path instead of the normal path
    if "segment" in OPTIONS and pr.has_segmenter(prompttype):
        return run_segment(prompttype, input, llm)
    else:
        return run_normal(prompttype, input, llm)

def run_normal(prompttype, input, llm, print_result=True):
    debug("\n---------  INPUT  ---------\n")
    debug(input)
    debug("\n-------- END INPUT --------\n")
    prompttext = pr.get_prompt(prompttype)
    prompt = PromptTemplate.from_template(prompttext)
    llmchain = LLMChain(prompt=prompt, llm=llm)
    debug("\n---------  RESULT  ---------\n")
    result = llmchain.run({"input": input})
    result = result.strip()
    # Remove "###" from the end of the result if it's there
    if result.endswith("###"):
        result = result[:-3]
    if PRINTRESULT and print_result:
        print(result)
    else:
        debug(result)
    debug("\n-------- END RESULT --------\n")
    return result

# In the segmenter path, the input is split into segments of the size specified by the option "segment"
# Each segment is run through the segmenter prompt specified by the top-level prompttype
# The result of each segment is concatenated together and the process is repeated until
# The entire input is small enough to be run through the normal path
# If the input is already small enough to be run through the normal path, the normal path is used immediately.
# The segments should preferably be split at sentence boundaries, and if that is not possible, at word boundaries.
def run_segment(prompttype, input, llm):
    segment_length = OPTIONS["segment"]
    if segment_length == True:
        segment_length = 2000
    if len(input) <= segment_length:
        debug("Input is small enough to run through the normal path: " + str(len(input)) + " <= " + str(segment_length) + " characters")
        return run_normal(prompttype, input, llm, print_result=True)
    debug("Input is too large to run through the normal path: " + str(len(input)) + " > " + str(segment_length) + " characters")
    segments = []
    # Split the input into segments of the specified length
    while len(input) > segment_length:
        # Find the last space in the segment
        last_space = input[:segment_length].rfind(" ")
        if last_space == -1:
            # If there is no space in the segment, split at the specified length
            last_space = segment_length
        last_segment = input[:last_space]
        # If the remaining input is smaller than a fifth of the segment length, append it to the last segment
        if len(input[last_space:]) < segment_length*0.2:
            debug("Remaining input is too small: " + str(len(input[last_space:])) + " < " + str(segment_length*0.2) + " characters")
            last_segment += input[last_space:]
            last_space = len(input)
        if len(last_segment) > 0:
            segments.append(last_segment)
        input = input[last_space:]
    if len(input) > 0:
        segments.append(input)

    # If there is only one segment, run it through the normal path with the original prompttype
    if len(segments) == 1:
        debug("Only one segment")
        return run_normal(prompttype, segments[0], llm)

    segmenter_prompttype = pr.get_segmenter(prompttype)
    # Now run each segment through the segmenter prompt
    result = []
    # Enumerate the segments so that we can print the segment number
    for i, segment in enumerate(segments):
        print("\n---------  SEGMENT " + str(i+1) + "/" + str(len(segments)) + " (" + str(len(segment)) + " bytes) ---------\n")
        segment_result = run_normal(segmenter_prompttype, segment, llm, print_result=False)
        # If segment_result is too short, it means that the segmenter prompt probably wasn't useful, so append the full segment instead
        if len(segment_result) < len(segment)*0.1:
            debug("Segment result is too short: " + str(len(segment_result)) + " < " + str(len(segment)*0.1) + " characters")
            segment_result = segment
        result.append(segment_result)
    segment_sum = "\n".join(result)
    # Now run the segment sum through the original run function
    return run(prompttype, segment_sum, llm)

def main():
    global MODEL_TYPE
    global DEBUG
    global PRINTRESULT
    global OPTIONS
    outputfile = None
    outputjson = None
    inputfile = None
    verbose = False
    jsonoutput = False
    input = None
    openai_api_base = os.getenv("OPENAI_API_BASE", "http://localhost:5001/")
    openai_api_key = os.getenv("OPENAI_API_KEY", "change-me-if-necessary")
    llm = OpenAI(openai_api_base=openai_api_base, openai_api_key=openai_api_key, temperature=0.2, max_tokens=1000)

    parser = argparse.ArgumentParser(description='Run a prompt')
    # prompttype from -p
    parser.add_argument('-p', '--prompttype', type=str, help='Prompt type (use LIST to see available prompttypes)', required=True)
    # input from file using -f
    parser.add_argument('-f', '--inputfile', type=str, help='Input from file (cannot be used together with URL)', required=False)
    # output file using -o
    parser.add_argument('-o', '--outputfile', type=str, help='Output file', required=False)
    # model type from -m
    parser.add_argument('-m', '--modeltype', type=str, help='Model type (use LIST to see available modeltypes)', required=False)
    # verbose from -v
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose', required=False)
    # output JSON using -j
    parser.add_argument('-j', '--json', type=str, help='Output JSON', required=False)
    # fetch input from url with -u
    parser.add_argument('-u', '--url', type=str, help='Fetch input from URL (cannot be used together with inputfile)', required=False)
    # special options with -O and it should be repeated for each option
    parser.add_argument('-O', '--option', type=str, help='Special option', required=False, action='append')
    # input from command line
    parser.add_argument('input', type=str, nargs='*', help='Input')

    args = parser.parse_args()

    # You cannot have both an input file and an input url
    if args.inputfile != None and args.url != None:
        parser.error("You cannot have both an input file and an input URL")

    # If prompttype is LIST, list all prompttypes
    if args.prompttype == "LIST":
        print("Available prompttypes:")
        for prompttype in pr.get_prompttype_list():
            # prompttype is a dict with keys "name" and "description"
            print(prompttype["name"] + ": " + prompttype["description"])
        sys.exit(0)

    # If modeltype is LIST, list all modeltypes
    if args.modeltype == "LIST":
        print("Available modeltypes:")
        for modeltype in pr.get_modeltype_list():
            print(modeltype)
        sys.exit(0)

    if args.modeltype != None:
        MODEL_TYPE = args.modeltype
    if args.prompttype != None:
        prompttype = args.prompttype
    if args.outputfile != None:
        outputfile = args.outputfile
    if args.verbose != None:
        DEBUG = args.verbose
    if args.option != None:
        parse_options(args.option)
    if args.json != None:
        outputjson = args.json
    if args.inputfile != None:
        with open(args.inputfile, "r") as f:
            input = f.read()
    elif args.url != None:
        input = fetch_input_from_url(args.url)
    else:
        input = " ".join(args.input)

    # If no outputfile or outputjson is specified, print result
    if outputfile == None and outputjson == None:
        PRINTRESULT = True

    if pr.requires_file_input(prompttype) and args.inputfile == None and args.url == None:
        parser.error("Prompt type {} requires an input file or url".format(prompttype))

    # If prompttype does not have a JSON result, outputjson is invalid
    if not pr.has_json_result(prompttype) and outputjson:
        parser.error("Prompt type {} does not have a JSON result".format(prompttype))

    pr.set_style(MODEL_TYPE)

    result = run(prompttype, input, llm)
    # If outputfile is specified, write result to file
    if outputfile != None:
        with open(outputfile, "w") as f:
            f.write(result)
    # If outputjson is specified, write JSON to file
    if outputjson:
        jsonresult = find_all_json(result)
        if len(jsonresult) == 0:
            debug("No JSON result found")
        else:
            with open(outputjson, "w") as f:
                json.dump(jsonresult[0], f, indent=4)

def init():
    pr.load_all_prompts_from_yaml()

if __name__ == "__main__":
    init()
    main()
    # pr.convert_all_prompts_to_yaml()