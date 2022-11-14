import difflib

def diff(a: str, b: str) -> str:
  return "".join(
    difflib.unified_diff(
      a.splitlines(True),
      b.splitlines(True)
    )
  )