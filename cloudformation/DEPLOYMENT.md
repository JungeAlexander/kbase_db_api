# validate template
aws --profile kbasedev cloudformation validate-template --template-body file://users-developers.yml

# create stack
aws --profile kbasedev cloudformation create-stack --stack-name users-group-developers --template-body file://users-developers.yml  --capabilities "CAPABILITY_IAM" "CAPABILITY_NAMED_IAM"

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
aws --profile kbasedev cloudformation validate-template --template-body file://microservices-network.yml

# create the stack for microservices network
aws --profile kbasedev cloudformation create-stack --stack-name microservices-network --template-body file://microservices-network.yml --parameters ParameterKey=VpcCidrPrefix,ParameterValue=10.0

<!--
# wait for the stack to finish
aws --profile kbasedev cloudformation wait stack-create-complete --stack-name microservices-network

# now list the exports
aws --profile dev cloudformation list-exports

# get a better display
aws --profile dev cloudformation list-exports --query 'Exports[].[Name,Value]' --output table

# do the same thing with jq
aws --profile dev cloudformation list-exports | jq -r '.Exports[] | "\(.Name): \(.Value)"' -->


### Network access

# validate the template
aws --profile kbasedev cloudformation validate-template --template-body file://microservices-internet.yml

# create the stack for microservices network internet access
aws --profile kbasedev cloudformation create-stack --stack-name microservices-internet --template-body file://microservices-internet.yml --parameters ParameterKey=NetworkStack,ParameterValue=microservices-network


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
aws --profile kbasedev cloudformation validate-template --template-body file://microservices-security-2.yml

# create the stack for microservices network internet access
aws --profile kbasedev cloudformation create-stack --stack-name microservices-security --template-body file://microservices-security-2.yml --parameters ParameterKey=NetworkStack,ParameterValue=microservices-network


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
aws --profile kbasedev cloudformation list-exports --query 'Exports[].Value'

# limit to just db subnets
aws --profile kbasedev cloudformation list-exports --query 'Exports[?starts_with(Name, `microservices-network-SubnetDb`) == `true`].[Name,Value]' --output table

# validate template
aws --profile kbasedev cloudformation validate-template --template-body file://rds-postgres.yml --query 'Parameters[].[ParameterKey,Description]' --output table

# create stack
aws --profile kbasedev cloudformation create-stack --stack-name rds-postgres --template-body file://rds-postgres.yml --parameters ParameterKey=NetworkStack,ParameterValue=microservices-network ParameterKey=Environment,ParameterValue=dev ParameterKey=DBUser,ParameterValue=dbadminpsqlkbase ParameterKey=DBPassword,ParameterValue=oicu8121231!

# TODO change db password manually

<!-- # wait for stack to complete
aws --profile dev cloudformation wait stack-create-complete --stack-name rds-postgres

# describe stack events (perhaps while you wait)
aws --profile dev cloudformation describe-stack-events --stack-name rds-postgres --query 'StackEvents[].[{Resource:LogicalResourceId, Status:ResourceStatus, Reason:ResourceStatusReason}]' --output table

# describe parameters (see db credentials out in plain text!)
aws --profile dev cloudformation describe-stacks --stack-name postgres --query 'Stacks[0].Parameters' --output table -->

### S3

aws --profile kbasedev cloudformation validate-template --template-body file://s3.yml

aws --profile kbasedev cloudformation create-stack --stack-name s3 --template-body file://s3.yml --parameters ParameterKey=MyBucketName,ParameterValue=${DB_API_LAMBDA_S3_BUCKET} # get from .env file

### Roles

aws --profile kbasedev cloudformation validate-template --template-body file://roles.yml

aws --profile kbasedev cloudformation create-stack --stack-name roles --template-body file://roles.yml --capabilities "CAPABILITY_IAM" "CAPABILITY_NAMED_IAM"

### Lambda deployment
VPC_ID=$(aws --profile kbasedev ec2 describe-vpcs --filters "Name=tag:Name,Values=microservices-network" --query 'Vpcs[0].VpcId' --output text) && echo ${VPC_ID}
SUBNET_ID=$(aws --profile kbasedev ec2 describe-subnets --filters "Name=tag:Name,Values=DMZ C" --query "Subnets[0].SubnetId" --output text) && echo ${SUBNET_ID}
NACL_ID=$(aws --profile kbasedev ec2 describe-network-acls --filters "Name=association.subnet-id,Values=${SUBNET_ID}" --query "NetworkAcls[0].Associations[0].NetworkAclId" --output text) && echo ${NACL_ID}
SECGROUP_ID=$(aws --profile kbasedev ec2 describe-security-groups --filters "Name=vpc-id,Values=${VPC_ID}" "Name=group-name,Values=default" --query "SecurityGroups[0].GroupId" --output text) && echo ${SECGROUP_ID}

export AWS_PROFILE=kbasedev
sam validate --template-file dbapi_lambda.yml
sam build --template-file dbapi_lambda.yml --use-container
sam package --s3-bucket ${DB_API_LAMBDA_S3_BUCKET} --region eu-west-1
sam deploy --stack-name db-api-lambda --s3-bucket ${DB_API_LAMBDA_S3_BUCKET} --region eu-west-1 --no-fail-on-empty-changeset \
  --capabilities CAPABILITY_IAM --parameter-overrides ParameterKey=NetworkStack,ParameterValue=microservices-network ParameterKey=MySecurityGroupID,ParameterValue=${SECGROUP_ID}

### EC2

#### SSH keys

# generate and save output of private key to a file
aws --profile dev ec2 create-key-pair --key-name kbase-dev --query 'KeyMaterial' --output text > ./kbase-dev.pem
# list key pairs
aws --profile kbasedev ec2 describe-key-pairs

#### Launching instance

aws --profile kbasedev ec2 run-instances --image-id ami-0aef57767f5404a3c --key-name kbase-dev --instance-type t2.nano --subnet-id ${SUBNET_ID} --security-group-ids ${SECGROUP_ID} --associate-public-ip-address # Runs Ubuntu Server 20.04 LTS (HVM), SSD Volume Type

#### Connect to instance via public IP
MY_IP=$(curl ifconfig.me) && echo ${MY_IP}
PUB_IP=$(aws --profile kbasedev ec2 describe-instances --query 'Reservations[0].Instances[0].PublicIpAddress' --output text) && echo ${PUB_IP}

aws --profile kbasedev ec2 authorize-security-group-ingress --group-id ${SECGROUP_ID} --protocol tcp --port 22 --cidr "${MY_IP}/32"
RULE_NUM=130
<!--
aws --profile kbasedev ec2 delete-network-acl-entry --network-acl-id ${NACL_ID} --ingress --rule-number ${RULE_NUM}
-->
aws --profile kbasedev ec2 create-network-acl-entry --network-acl-id ${NACL_ID} --ingress --rule-number ${RULE_NUM} --protocol tcp --port-range From=22,To=22 --cidr-block "${MY_IP}/32" --rule-action allow


ssh -i ./kbase-dev.pem ubuntu@${PUB_IP}
