from prompts.ullist import ULLISTPROMPT
from prompts.ollist import OLLISTPROMPT
from prompts.jsonobject import JSONOBJECTPROMPT
from prompts.jsonarray import JSONARRAYPROMPT
from prompts.ocrcard import OCRCARDPROMPT
from prompts.jsontoxml import JSONTOXMLPROMPT
from prompts.jsonrepair import JSONREPAIRPROMPT
from prompts.translatese2en import TRANSLATESE2ENPROMPT
from prompts.translateen2se import TRANSLATEEN2SEPROMPT
from prompts.summarize import SUMMARIZEPROMPT
from prompts.bullets import BULLETSPROMPT
import yaml
import os

CURRENT_STYLE = "alpaca"
STYLES={
    "alpaca": {
        "@@@INSTR@@@": "### Instructions:",
        "@@@INP@@@": "### Input:",
        "@@@RESP@@@": "### Response:"
    },
    "vicuna": {
        "@@@INSTR@@@": "### Human:",
        "@@@INP@@@": "### Human:",
        "@@@RESP@@@": "### Assistant:"
    },
    "wizard-vicuna": {
        "@@@INSTR@@@": "USER:",
        "@@@INP@@@": "USER:",
        "@@@RESP@@@": "ASSISTANT:"
    }
}

PROMPTS={}

# PROMPTS={
#     "ullist": { "prompt": ULLISTPROMPT, "has_json_result": False, "requires_file": False },
#     "ollist": { "prompt": OLLISTPROMPT, "has_json_result": False, "requires_file": False },
#     "jsonobject": { "prompt": JSONOBJECTPROMPT, "has_json_result": True, "requires_file": False },
#     "jsonarray": { "prompt": JSONARRAYPROMPT, "has_json_result": True, "requires_file": False },
#     "ocrcard": { "prompt": OCRCARDPROMPT, "has_json_result": True, "requires_file": True },
#     "jsontoxml": { "prompt": JSONTOXMLPROMPT, "has_json_result": False, "requires_file": True },
#     "jsonrepair": { "prompt": JSONREPAIRPROMPT, "has_json_result": True, "requires_file": True },
#     "translatese2en": { "prompt": TRANSLATESE2ENPROMPT, "has_json_result": False, "requires_file": False },
#     "translateen2se": { "prompt": TRANSLATEEN2SEPROMPT, "has_json_result": False, "requires_file": False },
#     "summarize": { "prompt": SUMMARIZEPROMPT, "has_json_result": False, "requires_file": True },
#     "bullets": { "prompt": BULLETSPROMPT, "has_json_result": False, "requires_file": True }
# }

# Convert prompts to yaml with properties name, description, has_json_result, requires_file, and prompt.
# Prompt should be last so that it can be a multiline string.
# Prompts should be saved in prompts/ with the name of the prompt as the filename.
def convert_all_prompts_to_yaml():
    for prompt in PROMPTS:
        print("Converting prompt: " + prompt)
        prompt_dict = PROMPTS[prompt]
        prompt_yaml = "name: " + prompt + "\n"
        prompt_yaml += "description: " + prompt + "\n"
        prompt_yaml += "has_json_result: " + str(prompt_dict["has_json_result"]) + "\n"
        prompt_yaml += "requires_file: " + str(prompt_dict["requires_file"]) + "\n"
        prompt_yaml += "prompt: |\n"
        prompt_yaml += "  " + prompt_dict["prompt"].replace("\n", "\n  ")
        # Write the prompt to a yaml file
        with open("prompts/" + prompt + ".yaml", "w") as f:
            f.write(prompt_yaml)

# Load all prompts from yaml files in prompts/ and store them in PROMPTS
def load_all_prompts_from_yaml():
    global PROMPTS
    for filename in os.listdir("prompts"):
        if filename.endswith(".yaml"):
            with open("prompts/" + filename, "r") as f:
                prompt_dict = yaml.safe_load(f)
                prompt = prompt_dict["name"]
                PROMPTS[prompt] = prompt_dict

# Return a list of all prompt names and their descriptions as a list of dictionaries
def get_prompttype_list():
    prompttype_list = []
    for prompt in PROMPTS:
        prompttype_list.append({
            "name": prompt,
            "description": PROMPTS[prompt]["description"]
        })
    return prompttype_list

def get_modeltype_list():
    return list(STYLES.keys())

def set_style(s = "alpaca"):
    global CURRENT_STYLE
    if s in STYLES:
        CURRENT_STYLE = s

def get_prompt(prompttype):
    # If the prompttype is not in the list of prompts, return None
    if prompttype not in PROMPTS:
        return None
    prompt = PROMPTS[prompttype]["prompt"]
    
    instr = STYLES[CURRENT_STYLE]["@@@INSTR@@@"]
    inp = STYLES[CURRENT_STYLE]["@@@INP@@@"]
    resp = STYLES[CURRENT_STYLE]["@@@RESP@@@"]

    return prompt.replace("@@@INSTR@@@", instr).replace("@@@INP@@@", inp).replace("@@@RESP@@@", resp)

def has_json_result(prompt):
    if prompt not in PROMPTS:
        return False
    return PROMPTS[prompt]["has_json_result"]

def requires_file_input(prompt):
    if prompt not in PROMPTS:
        return False
    return PROMPTS[prompt]["requires_file"]
