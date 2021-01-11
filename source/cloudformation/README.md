# validate template
aws cloudformation validate-template --template-body file://users-developers.yml

# create stack
aws --profile kbase-prod-admin cloudformation create-stack --stack-name users-group-developers --template-body file://users-developers.yml  --capabilities "CAPABILITY_IAM" "CAPABILITY_NAMED_IAM"

<!--
# await creation
aws --profile kbase-prod-admin  cloudformation wait stack-create-complete --stack-name users-group-developers
aws --profile kbase-prod-admin  cloudformation describe-stacks --stack-name users-group-developers
aws --profile kbase-prod-admin  cloudformation describe-stacks --stack-name users-group-developers --query 'Stacks[].[StackName,StackStatus]' --output text

# describe cloudformation stack resources to see details
aws --profile kbase-prod-admin  cloudformation describe-stack-resources --stack-name users-group-developers

# list IAM users to
aws --profile kbase-prod-admin  iam list-users

# list customer managed policies (not AWS policies)
aws --profile kbase-prod-admin  iam list-policies --scope Local

# see details of the PolicyDocument
aws --profile kbase-prod-admin  iam get-policy-version --policy-arn <policy arn> --version-id v1
-->
