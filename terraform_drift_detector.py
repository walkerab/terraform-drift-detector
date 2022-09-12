import difflib
from typing import Optional
from xmlrpc.client import Boolean

from terraform_plan_results import TerraformPlanResults

class TerraformDriftDetector:
  EXIT_CODES = {"NO_CHANGES": 0, "ERROR": 1, "CHANGES_PRESENT": 2}

  def __init__(self, current_plan_results:TerraformPlanResults = None, previous_plan_results:TerraformPlanResults = None) -> None:
    self.current_plan_results = current_plan_results
    self.previous_plan_results = previous_plan_results

  def should_alert(self) -> Boolean:
    if self.current_plan_results == None:
      return False
    else:
      return (
        self.current_plan_results != self.previous_plan_results
        and self.current_plan_results.changes_present()
      )

  def should_resolve(self) -> Boolean:
    return (
      self.current_plan_results != None
      and self.previous_plan_results != None
      and self.current_plan_results.no_changes()
      and self.previous_plan_results.changes_present()
    )

  def diff(self) -> Optional[str]:
    if self.current_plan_results != None and self.previous_plan_results != None:
      return "".join(
        difflib.unified_diff(
          self.strip_terraform_drift_message(self.previous_plan_results.message).splitlines(True),
          self.strip_terraform_drift_message(self.current_plan_results.message).splitlines(True),
        )
      )
    else:
      return None

  @classmethod
  def strip_terraform_drift_message(cls, message) -> str:
    marker = "Terraform will perform the following actions:"
    return message[message.find(marker):]

  def debug(self) -> None:
    print("========== REFRESH_RESULTS ==========")
    if self.current_plan_results != None:
      print(self.current_plan_results.message)
    else:
      print("N/A")

    print("========== PREVIOUS_REFRESH_RESULTS ==========")
    if self.previous_plan_results != None:
      print(self.previous_plan_results.message)
    else:
      print("N/A")

    print("========== DIFF ==========")
    print(self.diff())
    print("========== META ==========")
    print(f"SHOULD_ALERT: {self.should_alert()}")
    print(f"SHOULD_RESOLVE: {self.should_resolve()}")
