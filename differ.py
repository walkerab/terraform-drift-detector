from logging import FileHandler
import subprocess
import tempfile
import re

def diff(a: str, b: str) -> str:
  def tempf(contents: str) -> FileHandler:
    tf = tempfile.NamedTemporaryFile()
    tf.write(contents.encode())
    tf.flush()
    return tf
  files = list(map(tempf, [a, b]))
  p = subprocess.run(
    [
      "diff",
      "--ignore-all-space",
      "--unified=3",
      files[0].name,
      files[1].name
    ],
    capture_output=True,
    text=True
  )
  map(lambda tf: tf.close(), files)
  return re.sub("(.|\n)*@@.*\n", "", p.stdout, count = 1)