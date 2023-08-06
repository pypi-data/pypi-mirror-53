# cdp_validator_for_aws
This package will validate the artifacts in an AWS account using the
`cdp json` file (i.e. the json file that the UI generates for the
output of a CDP creation) and two other pieces of information
(`idbroker arn` and `storage base location`). 

An example of running it is here, using a prepackaged `cdp json` file that can be found in the package

```
python -m cdp_validator_for_aws -i arn:aws:iam::007856030109:role/lord-of-the-roles -s s3a://bucket/path -c euw1-autocreate-vpc.json
```

# AWS 
## CLI
We assume you have installed and configured the AWS CLI as per
https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html


## Permissions
The minimum permissions needed to run this system are:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeRouteTables",
                "ec2:DescribeSecurityGroups",
                "ec2:DescribeSubnets",
                "ec2:DescribeVpcs",
                "ec2:DescribeVpcAttribute",
                "eks:ListClusters",
                "iam:GetContextKeysForPrincipalPolicy",
                "iam:GetInstanceProfile",
                "iam:GetRole",
                "iam:SimulatePrincipalPolicy",
                "s3:GetBucketLocation",
                "s3:HeadBucket"
            ],
            "Resource": "*"
        }
    ]
}
```
The permissions that have the deepest security impact are those
required to simulate the various roles
(`iam:GetContextKeysForPrincipalPolicy` &
`iam:SimulatePrincipalPolicy`), as
[documented](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_testing-policies.html#policies-simulator-using-api)
by AWS. This system will do what it can with whatever permissions you
can give it.

The system takes a `--profile profile_name` argument, as per the usual
AWS CLI, and all calls are handed off to `boto3` to do the actual work.

### Setting up the permissions structure
Lets assume you've setup to execute AWS CLI commands with the
`default` profile with whatever permissions you normally get.

1. Create a role (lets call it `cdp_validation`) that:
   a. Trusts your `default` role
   b. Has the above permissions (or most of them)
   
1. In `${HOME}/.aws/credentials` put the following:

```
[validator]
role_arn = arn:aws:iam::YOUR_AWS_ACCOUNT_ID:role/cdp_validation
source_profile = default
```

Now you can run the validator thus:
```
python -m cdp_validator_for_aws -i arn:aws:iam::007856030109:role/lord-of-the-roles -s s3a://bucket/path -c euw1-autocreate-vpc.json
```

# Configuration
## Policy Management
Cloudera's documentation *LINK NEEDED* shows the various policy files
that are combined to give each of the four roles their necessary
permissions for various resources.

These files are in the `policies` directory and are named according to
Cloudera's naming conventions. They dictate the actions and resources
that are simulated for each role. If the actions change in the future
then these files can be simply updated. If the variables in the
resources change then I'm afraid you'll have to change the code
(look in the `policy_manager.py` to start)

# Development
## Testing
We drive our testing through make. There's a makefile in the top level
directory. 

Interesting targets are:

- `good`, `bad_1`, `bad_2` - this will make the acceptance tests
  (which builds infrastructure in AWS) for each of the three different
  test cases, derive a cdp json file from it, and then run the
  validator against that file

- `unittest` - this will run the python unittests

## Acceptance tests
Overall the acceptance tests go end to end - they use real live AWS
resources and run against those resources.

The acceptance tests are divided into equivalence classes, so that,
amongs the three sets of tests, every path, good and bad, is
executed. (An equivalence class treats classes of errors as the same -
we don't need to repeat a test if its already covered by another
test.)

When you run an acceptance test you need the following minimum
permissions:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "dynamodb:CreateTable",
                "dynamodb:DeleteTable",
                "dynamodb:DescribeContinuousBackups",
                "dynamodb:DescribeTable",
                "dynamodb:DescribeTimeToLive",
                "dynamodb:ListTagsOfResource",
                "dynamodb:TagResource",
                "ec2:AttachInternetGateway",
                "ec2:AuthorizeSecurityGroupEgress",
                "ec2:AuthorizeSecurityGroupIngress",
                "ec2:CreateInternetGateway",
                "ec2:CreateRoute",
                "ec2:CreateSecurityGroup",
                "ec2:CreateSubnet",
                "ec2:CreateVpc",
                "ec2:DeleteInternetGateway",
                "ec2:DeleteRoute",
                "ec2:DeleteSecurityGroup",
                "ec2:DeleteSubnet",
                "ec2:DeleteVpc",
                "ec2:DescribeAccountAttributes",
                "ec2:DescribeInternetGateways",
                "ec2:DescribeNetworkAcls",
                "ec2:DescribeNetworkInterfaces",
                "ec2:DescribeRouteTables",
                "ec2:DescribeSecurityGroups",
                "ec2:DescribeSubnets",
                "ec2:DescribeVpcAttribute",
                "ec2:DescribeVpcClassicLink",
                "ec2:DescribeVpcClassicLinkDnsSupport",
                "ec2:DescribeVpcDetails",
                "ec2:DescribeVpcs",
                "ec2:DetachInternetGateway",
                "ec2:ModifySubnetAttribute",
                "ec2:ModifyVpcAttribute",
                "ec2:RevokeSecurityGroupEgress",
                "ec2:RevokeSecurityGroupIngress",
                "iam:AddRoleToInstanceProfile",
                "iam:AttachRolePolicy",
                "iam:CreateInstanceProfile",
                "iam:CreatePolicy",
                "iam:CreateRole",
                "iam:DeleteInstanceProfile",
                "iam:DeletePolicy",
                "iam:DeleteRole",
                "iam:DetachRolePolicy",
                "iam:GetInstanceProfile",
                "iam:GetPolicy",
                "iam:GetPolicy",
                "iam:GetPolicyVersion",
                "iam:GetPolicyVersion",
                "iam:GetRole",
                "iam:ListAttachedRolePolicies",
                "iam:ListInstanceProfilesForRole",
                "iam:ListPolicyVersions",
                "iam:PassRole",
                "iam:RemoveRoleFromInstanceProfile",
                "iam:UpdateAssumeRolePolicy",
                "s3:CreateBucket",
                "s3:DeleteBucket",
                "s3:GetAccelerateConfiguration",
                "s3:GetBucketCORS",
                "s3:GetBucketLocation",
                "s3:GetBucketLogging",
                "s3:GetBucketObjectLockConfiguration",
                "s3:GetBucketRequestPayment",
                "s3:GetBucketTagging",
                "s3:GetBucketVersioning",
                "s3:GetBucketWebsite",
                "s3:GetEncryptionConfiguration",
                "s3:GetLifecycleConfiguration",
                "s3:GetReplicationConfiguration",
                "s3:ListBucket"
            ],
            "Resource": "*"
        }
    ]
}
```
