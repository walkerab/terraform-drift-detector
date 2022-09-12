#!/usr/bin/env python3
import subprocess
from terraform_drift_detector import TerraformDriftDetector
from terraform_plan_results import TerraformPlanResults

def main():
  previous_plan_results = TerraformPlanResults.load('previous_plan_results')
  current_plan_results = run_terraform_plan()
  drift_detector = TerraformDriftDetector(
    previous_plan_results = previous_plan_results,
    current_plan_results = current_plan_results
  )
  drift_detector.debug()
  current_plan_results.save('previous_plan_results')

def run_terraform_plan() -> TerraformPlanResults:
  # By splitting this into two steps we can suppress the "Refreshing..."
  # lines from the output.
  # See https://github.com/hashicorp/terraform/issues/27214#issuecomment-742809948
  PLAN_COMMAND = "terraform plan -detailed-exitcode -out=tfplan"
  SHOW_COMMAND = "terraform show -no-color tfplan"
  completed_plan_process = subprocess.run(
    PLAN_COMMAND.split(), stdout=subprocess.DEVNULL
  )
  # TODO: Check that plan succeeded before running show
  completed_show_process = subprocess.run(
    SHOW_COMMAND.split(), capture_output=True
  )

  return TerraformPlanResults(
    exit_code = completed_plan_process.returncode,
    message = completed_show_process.stdout.decode("UTF-8")
  )

if __name__ == "__main__":
  main()