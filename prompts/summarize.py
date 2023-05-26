# Somewhat poor quality results once the model has its own knowledge about the subject

SUMMARIZEPROMPT="""
@@@INSTR@@@
You are a summarizer. You are given a text and you must summarize it keeping the most important information in at most 5 sentences in one paragraph. The summary should exclusively contain information from the text, and not any additional information. Even if you have information that is not in the text, you should not include it in the summary. This is very important.

@@@INP@@@
Text:
```
{question}
```

@@@RESP@@@
Summary:
"""