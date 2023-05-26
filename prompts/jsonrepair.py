JSONREPAIRPROMPT="""
@@@INSTR@@@
You are a JSON generator repairing broken JSON content. You are given a JSON input that is broken and you must repair it so that it is valid JSON.

Example:

@@@INP@@@
Note: Remember to use the correct JSON output format.
Repair:
{{
    "Mercury": 0.39
    "Venus": 0.72,
    "Earth": 1.00,
}}

@@@RESP@@@
```
{{
    "Mercury": 0.39,
    "Venus": 0.72,
    "Earth": 1.00
}}
```

@@@INP@@@
Note: Remember to use the correct JSON output format.
Repair:
{{
    "Stockholm": {{
        "population": 975551,
        "description": "Stockholm is the 
        capital of Sweden",
        "area": 381.63
    }},
    "Gothenburg": {{
        "population": 583056,
        "area": 215.00
    }}
}}

@@@RESP@@@
```
{{
    "Stockholm": {{
        "population": 975551,
        "description": "Stockholm is the capital of Sweden",
        "area": 381.63
    }},
    "Gothenburg": {{
        "population": 583056,
        "area": 215.00
    }}
}}
```

@@@INP@@@
Note: Remember to use the correct JSON output format.
Repair:
{question}

@@@RESP@@@
"""