from typing import Optional
from utils.file_parser import ParsedDocx

_current_resume: Optional[ParsedDocx] = None

def set_resume(parsed: ParsedDocx) -> None:
    global _current_resume
    _current_resume = parsed

def get_resume() -> Optional[ParsedDocx]:
    return _current_resume

