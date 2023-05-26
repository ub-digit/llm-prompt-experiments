# A parser that looks for JSON objects in a string.
# The JSON object can be anywhere in the string. It always starts with either '{' or '['.
# The string must be parsed so that we check for the first '{' or '[' character, and then
# try to parse the string as JSON, however there may be text after the JSON object, so we
# must allow for that.

import json
import sys
from json.decoder import JSONDecodeError

# Find the first JSON object in the string and return a JSON object and the rest of the string, or None, None if no JSON object was found
def find_json(string):
    # We need to find the first '{' or '[' character
    # They must be checked simultaneously since one can contain the other
    for i in range(len(string)):
        if string[i] == '{' or string[i] == '[':
            # Now try to parse the string as JSON
            try:
                json_str = string[i:]
                json_obj = json.loads(json_str)
                return json_obj, string[i+len(json_str):]
            except JSONDecodeError as e:
                # If msg is "Extra data", then we try to parse the string as JSON again until the pos
                if e.msg == "Extra data":
                    try:
                        json_str = string[i:i+e.pos]
                        json_obj = json.loads(json_str)
                        return json_obj, string[i+len(json_str):]
                    except:
                        # If we can't parse it, then continue
                        continue
                # If we can't parse it, then continue
                continue
    return None, None

# Parse the string and find all JSON objects in the string
def find_all_json(string):
    json_objs = []
    remaining = string
    while True:
        json_obj, remaining = find_json(remaining)
        if json_obj is None:
            break
        json_objs.append(json_obj)
    return json_objs

def main():
    # Read the string from stdin
    string = sys.stdin.read()
    # Find the JSON objects in the string
    json_objs = find_all_json(string)
    # If we found a JSON object, then print it
    if len(json_objs) > 0:
        # Print each JSON object on a separate line
        for json_obj in json_objs:
            print(json.dumps(json_obj))
    else:
        # If we didn't find a JSON object, then print an empty line
        print("Nothing found")

if __name__ == "__main__":
    main()

