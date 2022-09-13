This software is a proof-of-concept and in what might be considered alpha stage. It comes with no guarantees. Use at your own risk.

# Terraform Drift Detector

The purpose of this script is to trigger an action when `terraform plan` either sees new drift or when it sees that drift has been resolved. The idea being that you use this script to notify yourself when drift occurs or is resolved.

## Why?

What's special about this script is that it only triggers the drift action when there is _new_ drift to account for. Why would you want this?

Let's say for example some drift occurs and you are not able to resolve it in a timely manner. Do you want to receive multiple notifications for the same drift? Probably not. Typically you would only want to know about the first time the drift is detected. That's what this does.

Also in some cases you may not be able to resolve the drift at all. This can happen with buggy providers or you have some weird resource that is created by Terraform but managed by something else like k8s.

## How It Works

Underneath the hood this script simply makes calls to `terraform plan`, captures the output and stores it, and then compares the output to the last time it ran. Based on the comparison it decides if there is new drift or if all drift has been resolved and takes the appropriate action.

NOTE: This means it's going to use whatever Terraform version you have installed. It's literally just running a shell for you.

## Usage

```
usage: detect_drift [-h] [--on-new-drift ON_NEW_DRIFT] [--on-resolve ON_RESOLVE] [--state-file-path STATE_FILE_PATH]

optional arguments:
  -h, --help            show this help message and exit
  --on-new-drift ON_NEW_DRIFT, -d ON_NEW_DRIFT
                        Bash expression to be executed when new drift is detected
  --on-resolve ON_RESOLVE, -r ON_RESOLVE
                        Bash expression to be executed when all drift is resolved
  --state-file-path STATE_FILE_PATH, -s STATE_FILE_PATH
                        Where to store the drift state. Default: ./previous_plan_results
```

## TODO

- Option to specify directory to run plan against
- Store state in the cloud so this can be used in CI/CD
- Pass script output like drift difference to callback scripts
- Have a warning action for when drift has changed but it has changed to a previously known state
