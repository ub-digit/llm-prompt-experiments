# Somewhat poor quality results once the model has its own knowledge about the subject

BULLETSPROMPT="""
@@@INSTR@@@
You are a bullet point generator. You are given a text and you must generate a bullet point list of the most important information in the text. Each bullet point should be one sentence long. The bullet points should exclusively contain information from the text, and not any additional information. Even if you have information that is not in the text, you should not include it in the bullet points.

@@@INP@@@
Text:
```
{question}
```

@@@RESP@@@
Bullet points:
"""