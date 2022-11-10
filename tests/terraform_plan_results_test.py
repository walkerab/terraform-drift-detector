import sys
sys.path.append("..")
from terraform_plan_results import TerraformPlanResults

def test_terraform_cruft_is_stripped_from_output():
    input = """
Note: Objects have changed outside of Terraform

Terraform detected the following changes made outside of Terraform since the last "terraform apply":

  # aws_security_group.sg has been changed
  ~ resource "aws_security_group" "sg" {
        id                     = "sg-00455d825359f2773"
        name                   = "terraform-20220911221017222100000001"
      ~ tags                   = {
          + "AnotherTag" = "more-different"
            # (1 unchanged element hidden)
        }
      ~ tags_all               = {
          + "AnotherTag" = "more-different"
            # (1 unchanged element hidden)
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
            # (1 unchanged element hidden)
        }
      ~ tags_all               = {
          - "AnotherTag" = "more-different" -> null
            # (1 unchanged element hidden)
        }
        # (8 unchanged attributes hidden)
    }

Plan: 0 to add, 1 to change, 0 to destroy."""
    expected = """Terraform will perform the following actions:

  # aws_security_group.sg will be updated in-place
  ~ resource "aws_security_group" "sg" {
        id                     = "sg-00455d825359f2773"
        name                   = "terraform-20220911221017222100000001"
      ~ tags                   = {
          - "AnotherTag" = "more-different" -> null
        }
      ~ tags_all               = {
          - "AnotherTag" = "more-different" -> null
        }
    }

Plan: 0 to add, 1 to change, 0 to destroy."""
    assert TerraformPlanResults(message = input).message == expected
