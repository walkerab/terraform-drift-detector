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

