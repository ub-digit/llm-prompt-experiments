JSONTOXMLPROMPT="""
@@@INSTR@@@
You are a JSON to XML converter. You are given a JSON object or array and you must convert it to XML.

Example:

@@@INP@@@
Note: Make sure to always output XML format.
Convert:
{{
    "Mercury": 0.39,
    "Venus": 0.72,
    "Earth": 1.00
}}

@@@RESP@@@
```
<root>
    <Mercury>0.39</Mercury>
    <Venus>0.72</Venus>
    <Earth>1.00</Earth>
</root>
```

@@@INP@@@
Note: Make sure to always output XML format.
Convert:
{{
    "Stockholm": {{
        "_capital": true,
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

@@@RESP@@@
```
<root>
    <Stockholm capital="true">
        <population>975551</population>
        <area>381.63</area>
    </Stockholm>
    <Gothenburg>
        <population>583056</population>
        <area>215.00</area>
    </Gothenburg>
    <Malmö>
        <population>312994</population>
        <area>77.06</area>
    </Malmö>
</root>
```

@@@INP@@@
Note: Make sure to always output XML format.
Convert:
[
    {{
        "name": "Russia",
        "size": 170982425
    }},
    {{
        "name": "Canada",
        "size": 37000000
    }},
    {{
        "name": "China",
        "size": 1393900000
    }}
]

@@@RESP@@@
```
<root>
    <item>
        <name>Russia</name>
        <size>170982425</size>
    </item>
    <item>
        <name>Canada</name>
        <size>37000000</size>
    </item>
    <item>
        <name>China</name>
        <size>1393900000</size>
    </item>
</root>
```

@@@INP@@@
Note: Make sure to always output XML format.
Convert:
{question}

@@@RESP@@@
"""
