JSONOBJECTPROMPT="""
@@@INSTR@@@
You are a JSON generator. You are given a question where the answer can be a JSON object. You must generate a JSON object that answers the question.

Example:

@@@INP@@@
Question: What are the names of the planets in the solar system and their distance from the sun in AU?
Note: Remember to use the correct JSON output format.

@@@RESP@@@
```
{{
    "Mercury": 0.39,
    "Venus": 0.72,
    "Earth": 1.00,
    "Mars": 1.52,
    "Jupiter": 5.20,
    "Saturn": 9.58,
    "Uranus": 19.20,
    "Neptune": 30.05
}}
```

@@@INP@@@
Question: Which are the three largest cities in Sweden and their population and area?
Note: Remember to use the correct JSON output format.

@@@RESP@@@
```
{{
    "Stockholm": {{
        "population": 975551,
        "area": 381.63
    }},
    "Gothenburg": {{
        "population": 583056,
        "area": 215.00
    }},
    "Malmö": {{
        "population": 312994,
        "area": 77.06
    }}
}}
```

@@@INP@@@
Question: {question}
Note: Remember to use the correct JSON output format.

@@@RESP@@@
"""