# CloudWatch Log cleaner

[![PyPI version](https://badge.fury.io/py/cwlogcleaner.svg)](https://pypi.python.org/pypi/cwlogcleaner)
[![license](https://img.shields.io/github/license/taimos/cwlogcleaner.svg)](LICENSE)

`cwlogcleaner` is a small utility to clean up log groups in AWS CloudWatch Logs.

## Installation

CloudWatch Log cleaner can be installed through pip:

```shell
pip3 install -U cwlogcleaner
```

## Quick example

```shell
$ cwlogcleaner

[?] Which groups should be deleted?: 
   o /aws/lambda/Lambda1
   o /aws/lambda/Lambda2
   o /aws/lambda/Lambda3
   o API-Gateway-Execution-Logs_1234567890/beta
 > X MySuperLogGroup
   o sns/eu-central-1/123456789012/app/GCM/Foobar


```

## Contributing

### **Did you find a bug?**

* **Ensure the bug was not already reported** by searching on GitHub under [Issues](https://github.com/taimos/cwlogcleaner/issues).

* If you're unable to find an open issue addressing the problem, [open a new one](https://github.com/taimos/cwlogcleaner/issues/new). Be sure to include a **title and clear description**, as much relevant information as possible, and a **code sample**demonstrating the expected behavior that is not occurring.

### **Did you write a patch that fixes a bug?**

* Open a new GitHub pull request with the patch.

* Ensure the PR description clearly describes the problem and solution. Include the relevant issue number if applicable.

### **Did you fix whitespace, format code, or make a purely cosmetic patch?**

Changes that are cosmetic in nature and do not add anything substantial to the stability, functionality, or testability will normally not be accepted.

### **Do you intend to add a new feature or change an existing one?**

* Suggest your change under [Issues](https://github.com/taimos/cwlogcleaner/issues).

* Do not open a pull request on GitHub until you have collected positive feedback about the change.

### **Do you want to contribute to the cwlogcleaner documentation?**

* Just file a PR with your recommended changes