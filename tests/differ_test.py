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
  expected_diff = """--- 
+++ 
@@ -1,2 +1,2 @@
 
-hello
+goodbye
"""
  print(diff(a,b))
  assert expected_diff == diff(a,b)