# validate template
aws cloudformation validate-template --template-body file://users-developers.yml

# create stack
aws --profile admin cloudformation create-stack --stack-name users-group-developers --template-body file://users-developers.yml  --capabilities "CAPABILITY_IAM" "CAPABILITY_NAMED_IAM"

<!--
# await creation
aws --profile admin  cloudformation wait stack-create-complete --stack-name users-group-developers
aws --profile admin  cloudformation describe-stacks --stack-name users-group-developers
aws --profile admin  cloudformation describe-stacks --stack-name users-group-developers --query 'Stacks[].[StackName,StackStatus]' --output text

# describe cloudformation stack resources to see details
aws --profile admin  cloudformation describe-stack-resources --stack-name users-group-developers

# list IAM users to
aws --profile admin  iam list-users

# list customer managed policies (not AWS policies)
aws --profile admin  iam list-policies --scope Local

# see details of the PolicyDocument
aws --profile admin  iam get-policy-version --policy-arn <policy arn> --version-id v1
-->


### Network

# validate template
aws cloudformation validate-template --template-body file://microservices-network.yml

# create the stack for microservices network
aws --profile dev cloudformation create-stack --stack-name microservices-network --template-body file://microservices-network.yml --parameters ParameterKey=VpcCidrPrefix,ParameterValue=10.0

<!--
# wait for the stack to finish
aws --profile dev cloudformation wait stack-create-complete --stack-name microservices-network

# now list the exports
aws --profile dev cloudformation list-exports

# get a better display
aws --profile dev cloudformation list-exports --query 'Exports[].[Name,Value]' --output table

# do the same thing with jq
aws --profile dev cloudformation list-exports | jq -r '.Exports[] | "\(.Name): \(.Value)"' -->


### Network access

# validate the template
aws cloudformation validate-template --template-body file://source/cloudformation/network/microservices-internet.yml

# create the stack for microservices network internet access
aws --profile dev cloudformation create-stack --stack-name microservices-internet --template-body file://source/cloudformation/network/microservices-internet.yml --parameters ParameterKey=NetworkStack,ParameterValue=microservices-network


<!-- # wait for the stack to finish
aws --profile dev cloudformation wait stack-create-complete --stack-name microservices-internet

# describe stack events
aws --profile dev cloudformation describe-stack-events --stack-name microservices-internet --query 'StackEvents[].[{Resource:LogicalResourceId, Status:ResourceStatus, Reason:ResourceStatusReason}]' --output table

# capture VPC ID to env variable
VPC_ID=$(aws --profile dev ec2 describe-vpcs --filters "Name=tag:Name,Values=microservices-network" --query 'Vpcs[0].VpcId' --output text)

# show routes
aws --profile dev ec2 describe-route-tables --filters "Name=vpc-id,Values=${VPC_ID}"

# show routes with cleaner output
aws --profile dev ec2 describe-route-tables --filters "Name=vpc-id,Values=${VPC_ID}" --query 'RouteTables[].[Tags[?Key==`Name`].Value, Associations[].SubnetId]' --output text -->


# validate the template
aws cloudformation validate-template --template-body file://microservices-security-2.yml

# create the stack for microservices network internet access
aws --profile dev cloudformation create-stack --stack-name microservices-security --template-body file://microservices-security-2.yml --parameters ParameterKey=NetworkStack,ParameterValue=microservices-network


<!-- # wait for the stack to finish
aws --profile dev cloudformation wait stack-create-complete --stack-name microservices-security

# capture VPC ID to env variable
VPC_ID=$(aws --profile dev ec2 describe-vpcs --filters "Name=tag:Name,Values=microservices-network" --query 'Vpcs[0].VpcId' --output text)

# list Network ACLs
aws --profile dev ec2 describe-network-acls --filters "Name=vpc-id,Values=${VPC_ID}" "Name=tag:aws:cloudformation:stack-name,Values=microservices-security" --query 'NetworkAcls[].[NetworkAclId,Tags[?Key==`Name`]|[0].Value]' --output text

# list NACL entries
aws --profile dev ec2 describe-network-acls --filters "Name=vpc-id,Values=${VPC_ID}" "Name=tag:aws:cloudformation:stack-name,Values=microservices-security" --query 'NetworkAcls[].Entries[]' -->

### Database

# get exports from microservices-network cloudformation stack
aws --profile dev cloudformation list-exports --query 'Exports[].Value'

# limit to just db subnets
aws --profile dev cloudformation list-exports --query 'Exports[?starts_with(Name, `microservices-network-SubnetDb`) == `true`].[Name,Value]' --output table

# validate template
aws cloudformation validate-template --template-body file://rds-postgres.yml --query 'Parameters[].[ParameterKey,Description]' --output table

# create stack
aws --profile dev cloudformation create-stack --stack-name rds-postgres --template-body file://rds-postgres.yml --parameters ParameterKey=NetworkStack,ParameterValue=microservices-network ParameterKey=Environment,ParameterValue=dev ParameterKey=DBUser,ParameterValue=dbadminpsqlkbase ParameterKey=DBPassword,ParameterValue=oicu8121231!

# TODO change db password manually

<!-- # wait for stack to complete
aws --profile dev cloudformation wait stack-create-complete --stack-name rds-postgres

# describe stack events (perhaps while you wait)
aws --profile dev cloudformation describe-stack-events --stack-name rds-postgres --query 'StackEvents[].[{Resource:LogicalResourceId, Status:ResourceStatus, Reason:ResourceStatusReason}]' --output table

# describe parameters (see db credentials out in plain text!)
aws --profile dev cloudformation describe-stacks --stack-name postgres --query 'Stacks[0].Parameters' --output table -->
