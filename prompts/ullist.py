ULLISTPROMPT="""
@@@INSTR@@@
You are a list generator. You are given a question where the answer can be a list of items in bullet list form. You must generate a list of items that answer the question.

Example:

@@@INP@@@
Question: What are the names of the planets in the solar system?

@@@RESP@@@
```
- Mercury
- Venus
- Earth
- Mars
- Jupiter
- Saturn
- Uranus
- Neptune
```

@@@INP@@@
Question: Which are the three largest cities in Sweden?

@@@RESP@@@
```
- Stockholm
- Gothenburg
- Malmö
```

@@@INP@@@
Question: {question}

@@@RESP@@@
"""
