from __future__ import annotations
import pickle
from typing import Optional
from xmlrpc.client import Boolean

class TerraformPlanResults:
  EXIT_CODES = {"NO_CHANGES": 0, "ERROR": 1, "CHANGES_PRESENT": 2}

  def __init__(
    self,
    message:str = "",
    exit_code:Optional[int] = None,
    no_changes:Boolean = False,
    error:Boolean = False,
    changes_present:Boolean = False
  ) -> None:
    self.message = message
    if exit_code != None:
      self.exit_code = exit_code
    elif error:
      self.exit_code = self.EXIT_CODES["ERROR"]
    elif changes_present:
      self.exit_code = self.EXIT_CODES["CHANGES_PRESENT"]
    elif no_changes:
      self.exit_code = self.EXIT_CODES["NO_CHANGES"]
    else:
      self.exit_code = self.EXIT_CODES["NO_CHANGES"]

  def no_changes(self) -> Boolean:
    return self.exit_code == self.EXIT_CODES["NO_CHANGES"]

  def error(self) -> Boolean:
    return self.exit_code == self.EXIT_CODES["ERROR"]

  def changes_present(self) -> Boolean:
    return self.exit_code == self.EXIT_CODES["CHANGES_PRESENT"]

  def save(self, path) -> None:
    try:
      file = open(path, "wb")
    except:
      return None
    pickle.dump(self, file)
    file.close()

  def __eq__(self, other: TerraformPlanResults) -> bool:
    if not isinstance(other, TerraformPlanResults):
      return NotImplemented
    return (
      self.exit_code == other.exit_code
      and
      self.message == other.message
    )

  def __str__(self) -> str:
    return f"""exit_code: {self.exit_code}
message: {self.message}
"""

  @classmethod
  def load(cls, path) -> TerraformPlanResults:
    try:
      file = open(path, "rb")
    except:
      return cls()
    results = pickle.load(file)
    file.close()
    return results

