import os
import pytest
import subprocess
import pdb

@pytest.fixture(autouse=True)
def run_around_tests():
  os.chdir('./terraform')
  exec_bash("""
  terraform destroy -auto-approve \
  && rm -rf .terraform
  terraform init
  rm did_drift
  rm did_resolve
  rm previous_plan_results
  """) 
  yield
  exec_bash("""
  rm did_drift
  rm did_resolve
  rm previous_plan_results
  terraform destroy -auto-approve \
  && rm -rf .terraform
  """)
  os.chdir('../')

def exec_bash(code: str) -> bool:
  return subprocess.run(code, shell=True).returncode == 0

def test_it_runs_on_a_fresh_terraform_module():
  assert exec_bash('../../detect_drift')

def test_we_can_specify_the_state_file():
  assert exec_bash("""
  terraform apply -auto-approve
  ../../detect_drift -s otherfile
  test -e otherfile && ! test -e previous_plan_results && rm otherfile
  """)

def test_it_detects_drift():
  assert exec_bash("""
  terraform apply -auto-approve
  export TEST_SG_ID=$(terraform output -raw sg_id)
  aws ec2 create-tags --region us-east-1 --resource $TEST_SG_ID --tags Key=AnotherTag,Value=another-tag-value
  ../../detect_drift -d "touch did_drift" -r "touch did_resolve"
  test -e did_drift && ! test -e did_resolve
  """)

def test_it_detects_additional_drift():
  assert exec_bash("""
  terraform apply -auto-approve
  export TEST_SG_ID=$(terraform output -raw sg_id)
  aws ec2 create-tags --region us-east-1 --resource $TEST_SG_ID --tags Key=AnotherTag,Value=another-tag-value
  ../../detect_drift
  aws ec2 create-tags --region us-east-1 --resource $TEST_SG_ID --tags Key=AnotherAdditionalTag,Value=another-additional-tag-value
  ../../detect_drift -d "touch did_drift" -r "touch did_resolve"
  test -e did_drift && ! test -e did_resolve
  """)

def test_it_detects_drift_is_resolved():
  assert exec_bash("""
  terraform apply -auto-approve
  export TEST_SG_ID=$(terraform output -raw sg_id)
  aws ec2 create-tags --region us-east-1 --resource $TEST_SG_ID --tags Key=AnotherTag,Value=another-tag-value
  ../../detect_drift
  terraform apply -auto-approve
  ../../detect_drift -d "touch did_drift" -r "touch did_resolve"
  ! test -e did_drift && test -e did_resolve
  """)
