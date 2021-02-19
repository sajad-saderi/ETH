from typing import Union
import markdown

def cross_secrecy_escape(value: Union[str, bytes]) -> str:
    if value is None:
        return None
    if value is not type(str):
        value = value.decode('utf-8')
    return value.replace('<', '&lt;').replace('>', '&gt;') # we can't tolerate intruders

def chat_escape(value: Union[str, bytes]) -> str:
    if value is None:
        return None
    try:
        value = value.decode('utf-8')
    except Exception:
        pass
    return markdown.markdown(value)
