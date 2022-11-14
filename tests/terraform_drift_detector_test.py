import sys
sys.path.append("..")
import os
import tempfile
import pytest
from terraform_drift_detector import TerraformDriftDetector
from terraform_plan_results import TerraformPlanResults

def test_should_not_detect_drift_or_resolve_because_there_is_no_state():
  drift_detector = TerraformDriftDetector()
  assert drift_detector.new_drift_detected() == False
  assert drift_detector.drift_resolved() == False

def test_should_not_detect_drift_or_resolve_because_there_is_no_drift(
  plan_results_with_no_drift
):
  drift_detector = TerraformDriftDetector(
    current_plan_results = plan_results_with_no_drift
  )
  assert drift_detector.new_drift_detected() == False
  assert drift_detector.drift_resolved() == False

def test_should_detect_drift_but_not_resolve_because_there_is_drift(
    plan_results_with_some_drift
):
  drift_detector = TerraformDriftDetector(
    current_plan_results = plan_results_with_some_drift
  )
  assert drift_detector.new_drift_detected() == True
  assert drift_detector.drift_resolved() == False

def test_should_not_detect_drift_or_resolve_because_there_is_no_drift_and_there_previously_was_no_drift(
  plan_results_with_no_drift
):
  drift_detector = TerraformDriftDetector(
    previous_plan_results = plan_results_with_no_drift,
    current_plan_results = plan_results_with_no_drift
  )
  assert drift_detector.new_drift_detected() == False
  assert drift_detector.drift_resolved() == False

def test_should_detect_drift_but_not_resolve_because_there_was_no_drift_but_now_there_is(
  plan_results_with_no_drift, plan_results_with_some_drift
):
  drift_detector = TerraformDriftDetector(
    previous_plan_results = plan_results_with_no_drift,
    current_plan_results = plan_results_with_some_drift
  )
  assert drift_detector.new_drift_detected() == True
  assert drift_detector.drift_resolved() == False

def test_should_resolve_but_not_detect_drift_because_there_is_no_drift_but_there_previously_was_drift(
  plan_results_with_no_drift, plan_results_with_some_drift
):
  drift_detector = TerraformDriftDetector(
    previous_plan_results = plan_results_with_some_drift,
    current_plan_results = plan_results_with_no_drift
  )
  assert drift_detector.new_drift_detected() == False
  assert drift_detector.drift_resolved() == True

def test_should_not_detect_drift_or_resolve_because_drift_is_same_as_last_time(
  plan_results_with_some_drift
):
  drift_detector = TerraformDriftDetector(
    previous_plan_results = plan_results_with_some_drift,
    current_plan_results = plan_results_with_some_drift
  )
  assert drift_detector.new_drift_detected() == False
  assert drift_detector.drift_resolved() == False

def test_should_detect_drift_but_not_resolve_because_drift_is_different_from_last_time(
  plan_results_with_some_drift, plan_results_with_more_drift
):
  drift_detector = TerraformDriftDetector(
    previous_plan_results = plan_results_with_some_drift,
    current_plan_results = plan_results_with_more_drift
  )
  assert drift_detector.new_drift_detected() == True
  assert drift_detector.drift_resolved() == False

def test_saving_and_loading_plan_results():
  RESULTS_PATH = os.path.join(tempfile.gettempdir(), 'plan_results')
  plan_results = TerraformPlanResults(changes_present = True, message = "test message")
  plan_results.save(RESULTS_PATH)
  loaded_plan_results = TerraformPlanResults.load(RESULTS_PATH)
  print(loaded_plan_results)
  print(plan_results)
  assert loaded_plan_results == plan_results

# FIXTURES

@pytest.fixture()
def plan_results_with_no_drift():
    yield TerraformPlanResults(message = """
No changes. Your infrastructure still matches the configuration.

Terraform has checked that the real remote objects still match the result of your most recent changes, and found no differences.""")

@pytest.fixture()
def plan_results_with_some_drift():
  yield TerraformPlanResults(
    changes_present = True,
    message = """
Note: Objects have changed outside of Terraform

Terraform detected the following changes made outside of Terraform since the last "terraform apply":

  # aws_security_group.sg has been changed
  ~ resource "aws_security_group" "sg" {
        id                     = "sg-00455d825359f2773"
        name                   = "terraform-20220911221017222100000001"
      ~ tags                   = {
          ~ "Name" = "terraform-drift-test" -> "foobar"
        }
      ~ tags_all               = {
          ~ "Name" = "terraform-drift-test" -> "foobar"
        }
        # (8 unchanged attributes hidden)
    }

Unless you have made equivalent changes to your configuration, or ignored the relevant attributes using ignore_changes, the following plan may
include actions to undo or respond to these changes.

────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  ~ update in-place

Terraform will perform the following actions:

  # aws_security_group.sg will be updated in-place
  ~ resource "aws_security_group" "sg" {
        id                     = "sg-00455d825359f2773"
        name                   = "terraform-20220911221017222100000001"
      ~ tags                   = {
          ~ "Name" = "foobar" -> "terraform-drift-test"
        }
      ~ tags_all               = {
          ~ "Name" = "foobar" -> "terraform-drift-test"
        }
        # (8 unchanged attributes hidden)
    }

Plan: 0 to add, 1 to change, 0 to destroy.
"""
  )

@pytest.fixture()
def plan_results_with_more_drift():
  yield TerraformPlanResults(
    changes_present = True,
    message = """
Note: Objects have changed outside of Terraform

Terraform detected the following changes made outside of Terraform since the last "terraform apply":

  # aws_security_group.sg has been changed
  ~ resource "aws_security_group" "sg" {
        id                     = "sg-00455d825359f2773"
        name                   = "terraform-20220911221017222100000001"
      ~ tags                   = {
          + "AnotherTag" = "more-different"
          ~ "Name"       = "terraform-drift-test" -> "foobar"
        }
      ~ tags_all               = {
          + "AnotherTag" = "more-different"
          ~ "Name"       = "terraform-drift-test" -> "foobar"
        }
        # (8 unchanged attributes hidden)
    }

Unless you have made equivalent changes to your configuration, or ignored the relevant attributes using ignore_changes, the following plan may
include actions to undo or respond to these changes.

────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  ~ update in-place

Terraform will perform the following actions:

  # aws_security_group.sg will be updated in-place
  ~ resource "aws_security_group" "sg" {
        id                     = "sg-00455d825359f2773"
        name                   = "terraform-20220911221017222100000001"
      ~ tags                   = {
          - "AnotherTag" = "more-different" -> null
          ~ "Name"       = "foobar" -> "terraform-drift-test"
        }
      ~ tags_all               = {
          - "AnotherTag" = "more-different" -> null
          ~ "Name"       = "foobar" -> "terraform-drift-test"
        }
        # (8 unchanged attributes hidden)
    }

Plan: 0 to add, 1 to change, 0 to destroy.
"""
  )
