# jmpr
[![pipeline status](https://git.egt-labs.com/robert.patt-corner/jmpr/badges/master/pipeline.svg)](https://git.egt-labs.com/robert.patt-corner/jmpr/commits/master) [![PyPI version](https://badge.fury.io/py/jmpr.svg)](https://badge.fury.io/py/jmpr)

![eGT Labs Logo](https://avatars0.githubusercontent.com/u/5140903?s=200&v=4)

## What this is?
Tooling to permit AWS account navigation

## How does it work?
![Magic](https://media.giphy.com/media/12NUbkX6p4xOO4/giphy.gif)

But seriously, it does some cool stuff in really cool ways...

## How do I use it?

To get started using jmpr install via pip: `pip install jmpr`.

 (You may need to `pip install boto3 pyyaml` to preinstall the dependencies) 
 
 To run jmpr use `jmpr -y yourfile.yml`

 Use the following gitlab-ci.yml configuration to run in a GitLab CI/CD Pipeline:

 ```yaml
Deploy Test:
  stage: deploy
  before_script:
    - pip install . --quiet
  script:
    - jmpr -y test.yaml
 ```

### AWS Organization Configuration
TODO: EXPLAIN HOW TO SETUP THE AWS ORGS CONFIG

### AWS Account Configuration
TODO: EXPLAIN HOW TO CONFIGURE AWS ACCOUNTS TO BE USED. BOTH ORG ACCOUNTS AND NON ORG ACCOUNTS

### Your jmpr Manifest File
jmpr accepts yaml files as input. These files define your entire authentication infrastructure. Including Accounts, Roles, Users, and Policies. 

**Example Users**
```yaml
users:
  - name: testuser
    additional_path: "something"
    cloud: AWS
    target_roles:
      - account: 540253368830
        role_name: ROLE-ADMIN
        region: us-west-2
      - account: 879397242692
        role_name: ROLE-DEV
      - account: 611424868009
        role_name: ROLE-NEW-ROLE
      - account: 333422963795
        role_name: ROLE-BILLING
      - account: 355841365103
        role_name: ROLE-BILLING

```


**Example Roles**
```yaml
roles:
  - name: ROLE-ADMIN
    import:
      - arn:aws:iam::aws:policy/AdministratorAccess
  - name: ROLE-RO
    import:
      - arn:aws:iam::aws:policy/ReadOnlyAccess
      - arn:aws:iam::aws:policy/job-function/Billing
  - name: ROLE-BILLING
    import:
      - arn:aws:iam::aws:policy/job-function/Billing
  - name: ROLE-FOO
    import:
      - arn:aws:iam::aws:policy/ReadOnlyAccess
      - arn:aws:iam::aws:policy/job-function/Billing
```

**Example Accounts**
```yaml
accounts:
  test_acct_1:
    account_number: 616552976502

  test_acct_2:
    name: My Account
    account_number: 426276006285
    color: ffbd05
    default_region: us-east-1

  test_acct_3:
    name: Your Account
    account_number: 343074669674
    color: 225f91
    default_region: us-east-2
    purge: false
    allowed_roles:
      - admin
      - ro
      - billing

  '420355987158':
    name: No One's Account
```
For more examples please see [test.yml](test.yaml).

## Developer Notes: 
To work on this project the following two commands will be your best friends

`pip install . --no-deps` - Quickly install the local repo via pip without worring about dependencies

`jmpr -y test.yaml` - Runs jmpr on the test yaml file that is designed to exersize the yaml parser

The core library file is [cloudassets.py](./jmpr/cloudassets.py).

The jmpr cli configuration is [cli.py](./jmpr/cli.py)

### Note on paths:
AWS IAM fetch and create are carried out only using the name of an entity (user, group, role) by a client associated with an account.  Path does not play into AWS IAM entity retrieval or creation.

Paths are embedded in resulting entity ARN's, and ARNs are used to relate entities to each other, for instance in an 'assume role policy'.  In addition, paths can be used in policies to include or exclude.

So:
* Entities (users, roles, etc.) with the same name and different paths will collide
* Entities specified with an ARN that does not include the correct path will not be properly referenced.

Maintaining and managing YAML or JSON ARNs including path is likely to introduce frequent errors and failures.  

In consequence, the jmpr approach constructs entities in the way that they are fetched, by account and name, retaining any path information as decoration. 

When ARNs are needed for a call, the ARN is constructed dynamically in code from the attributes of the entity, which can include the path decoration.  This ensures consistent ARNs.

Initially in early release entity paths are guaranteed consistent and all equal to the asset_path, but in later releases entity-specific paths may be introduced so long as they are not embedded in ARNs.

## For More Information
[Roadmap](./ROADMAP.md)

[Tests](./TESTS.md)

Developed in [eGT Labs](https://www.eglobaltech.com/egt-labs/) by [eGlobalTech](https://www.eglobaltech.com/) a [TetraTech](https://www.tetratech.com/) Company

![eGT Labs Logo](https://avatars0.githubusercontent.com/u/5140903?s=200&v=4)

## License
jmpr - Python tooling to enable and manage AWS account navigation

Copyright (C) 2019  [eGlobalTech](https://www.eglobaltech.com)


This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
