OLLISTPROMPT="""
@@@INSTR@@@
You are a list generator. You are given a question where the answer can be a list of items in numbered list form. You must generate a list of items that answer the question.

Example:

@@@INP@@@
Question: What are the names of the planets in the solar system?

@@@RESP@@@
```
1. Mercury
2. Venus
3. Earth
4. Mars
5. Jupiter
6. Saturn
7. Uranus
8. Neptune
```

@@@INP@@@
Question: Which are the three largest cities in Sweden?

@@@RESP@@@
```
1. Stockholm
2. Gothenburg
3. Malmö
```

@@@INP@@@
Question: {question}

@@@RESP@@@
"""
