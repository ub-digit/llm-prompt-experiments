import sys
from langchain.llms import TextGenerationWebui, OpenAI
import prompt as pr
from langchain import PromptTemplate, LLMChain
from flexible_json_parser import find_all_json
import json
# Handle cmd line arguments
import argparse
import requests
from bs4 import BeautifulSoup

MODEL_TYPE="wizard-vicuna"
DEBUG=False
PRINTRESULT=False

def debug(msg):
    if DEBUG:
        print(msg)

# Use requests and beautifulsoup to fetch the question from the text content of a URL
def fetch_question_from_url(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    # Get the text content of the page
    question = soup.get_text().strip()
    # If the text content is empty, raise an exception
    if question == "":
        raise Exception("The text content of the URL is empty")
    return question

def run(prompttype, question, llm):
    debug("\n---------  QUESTION  ---------\n")
    debug(question)
    debug("\n-------- END QUESTION --------\n")
    prompttext = pr.get_prompt(prompttype)
    prompt = PromptTemplate.from_template(prompttext)
    llmchain = LLMChain(prompt=prompt, llm=llm)
    debug("\n---------  RESULT  ---------\n")
    result = llmchain.run({"question": question})
    result = result.strip()
    # Remove "###" from the end of the result if it's there
    if result.endswith("###"):
        result = result[:-3]
    if PRINTRESULT:
        print(result)
    else:
        debug(result)
    debug("\n-------- END RESULT --------\n")
    return result

def main():
    global MODEL_TYPE
    global DEBUG
    global PRINTRESULT
    outputfile = None
    outputjson = None
    questionfile = None
    verbose = False
    jsonoutput = False
    question = None
    # llm = TextGenerationWebui(url="http://10.17.42.167:5000/api/v1", verbose=True, temperature = 0.2, max_new_tokens=1000, early_stopping = True, stopping_strings = ["\n###"])
    llm = OpenAI(openai_api_base="http://10.17.42.167:5001/", openai_api_key="whatever", temperature=0.2, max_tokens=1000)

    parser = argparse.ArgumentParser(description='Run a prompt')
    # prompttype from -p
    parser.add_argument('-p', '--prompttype', type=str, help='Prompt type (use LIST to see available prompttypes)', required=True)
    # question from file using -f
    parser.add_argument('-f', '--questionfile', type=str, help='Question from file (cannot be used together with URL)', required=False)
    # output file using -o
    parser.add_argument('-o', '--outputfile', type=str, help='Output file', required=False)
    # model type from -m
    parser.add_argument('-m', '--modeltype', type=str, help='Model type (use LIST to see available modeltypes)', required=False)
    # verbose from -v
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose', required=False)
    # output JSON using -j
    parser.add_argument('-j', '--json', type=str, help='Output JSON', required=False)
    # fetch question from url with -u
    parser.add_argument('-u', '--url', type=str, help='Fetch question from URL (cannot be used together with questionfile)', required=False)
    # question from command line
    parser.add_argument('question', type=str, nargs='*', help='Question')

    args = parser.parse_args()

    # You cannot have both a question file and a question url
    if args.questionfile != None and args.url != None:
        parser.error("You cannot have both a question file and a question URL")

    # If prompttype is LIST, list all prompttypes
    if args.prompttype == "LIST":
        print("Available prompttypes:")
        for prompttype in pr.get_prompttype_list():
            print(prompttype)
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
    if args.json != None:
        outputjson = args.json
    if args.questionfile != None:
        with open(args.questionfile, "r") as f:
            question = f.read()
    elif args.url != None:
        question = fetch_question_from_url(args.url)
    else:
        question = " ".join(args.question)

    # If no outputfile or outputjson is specified, print result
    if outputfile == None and outputjson == None:
        PRINTRESULT = True

    if pr.requires_file_input(prompttype) and args.questionfile == None and args.url == None:
        parser.error("Prompt type {} requires a question file or url".format(prompttype))

    # If prompttype does not have a JSON result, outputjson is invalid
    if not pr.has_json_result(prompttype) and outputjson:
        parser.error("Prompt type {} does not have a JSON result".format(prompttype))

    pr.set_style(MODEL_TYPE)

    result = run(prompttype, question, llm)
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

if __name__ == "__main__":
    main()