JSONARRAYPROMPT="""
@@@INSTR@@@
You are a JSON generator. You are given a question where the answer can be a JSON array of JSON objects or values. You must generate a JSON array that answers the question.

Example:

@@@INP@@@
Question: What are the names of the planets in the solar system and their distance from the sun in AU?
Note: Remember to use the correct JSON output format.

@@@RESP@@@
```
[
    {{ "name": "Mercury", "distance": 0.39 }},
    {{ "name": "Venus", "distance": 0.72 }},
    {{ "name": "Earth", "distance": 1.00 }},
    {{ "name": "Mars", "distance": 1.52 }},
    {{ "name": "Jupiter", "distance": 5.20 }},
    {{ "name": "Saturn", "distance": 9.58 }},
    {{ "name": "Uranus", "distance": 19.20 }},
    {{ "name": "Neptune", "distance": 30.05 }}
]
```

@@@INP@@@
Question: Which are the three largest cities in Sweden and their population and area?
Note: Remember to use the correct JSON output format.

@@@RESP@@@
```
[
    {{ "name": "Stockholm", "population": 975551, "area": 381.63 }},
    {{ "name": "Gothenburg", "population": 583056, "area": 215.00 }},
    {{ "name": "Malmö", "population": 312994, "area": 77.06 }}
]
```

@@@INP@@@
Question: {question}
Note: Remember to use the correct JSON output format.

@@@RESP@@@
"""