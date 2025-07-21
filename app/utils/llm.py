import re

def strip_code_block(text):
    if text is None:
        return ""
    return re.sub(r"^```[a-zA-Z]*\\n|```$", "", text.strip(), flags=re.MULTILINE) 