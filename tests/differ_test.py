import sys
sys.path.append("..")
from differ import diff

def test_basic_diff():
  a = """
hello
"""
  b = """
goodbye
"""
  expected_diff = """ 
-hello
+goodbye
"""
  assert expected_diff == diff(a,b)

def test_empty_diff():
  assert '' == diff('', '')
  assert '' == diff('a', 'a')

def test_ignores_whitespace():
  assert '' == diff('a', 'a ')
  assert '' == diff('a', ' a')
  assert '' == diff('    a     ', '  a   ')
  assert '' == diff('    a     b   ', '  a b  ')
