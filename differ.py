import difflib
import re

def diff(a: str, b: str) -> str:
  diff_string = "".join(
    difflib.unified_diff(
      a.splitlines(True),
      b.splitlines(True)
    )
  )
  return re.sub("(.|\n)*@@.*\n", "", diff_string, count = 1)