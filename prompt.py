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

PROMPTS={
    "ullist": { "prompt": ULLISTPROMPT, "has_json_result": False, "requires_file": False },
    "ollist": { "prompt": OLLISTPROMPT, "has_json_result": False, "requires_file": False },
    "jsonobject": { "prompt": JSONOBJECTPROMPT, "has_json_result": True, "requires_file": False },
    "jsonarray": { "prompt": JSONARRAYPROMPT, "has_json_result": True, "requires_file": False },
    "ocrcard": { "prompt": OCRCARDPROMPT, "has_json_result": True, "requires_file": True },
    "jsontoxml": { "prompt": JSONTOXMLPROMPT, "has_json_result": False, "requires_file": True },
    "jsonrepair": { "prompt": JSONREPAIRPROMPT, "has_json_result": True, "requires_file": True },
    "translatese2en": { "prompt": TRANSLATESE2ENPROMPT, "has_json_result": False, "requires_file": False },
    "translateen2se": { "prompt": TRANSLATEEN2SEPROMPT, "has_json_result": False, "requires_file": False },
    "summarize": { "prompt": SUMMARIZEPROMPT, "has_json_result": False, "requires_file": True },
    "bullets": { "prompt": BULLETSPROMPT, "has_json_result": False, "requires_file": True }
}

def get_prompttype_list():
    return list(PROMPTS.keys())

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
