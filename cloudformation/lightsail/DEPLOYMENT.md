# Lightsail

Create:

- Postgres database instance
- Compute instance

Update database access in `.env` file.

# S3

aws --profile kbasedev cloudformation validate-template --template-body file://s3.yml

aws --profile kbasedev cloudformation create-stack --stack-name s3 --template-body file://s3.yml \
    --parameters ParameterKey=MyBucketName,ParameterValue=${DB_API_LAMBDA_S3_BUCKET} # get DB_API_LAMBDA_S3_BUCKET from .env file

# Roles

aws --profile kbasedev cloudformation validate-template --template-body file://roles.yml

aws --profile kbasedev cloudformation create-stack --stack-name roles --template-body file://roles.yml --capabilities "CAPABILITY_IAM" "CAPABILITY_NAMED_IAM"

# Lambda

export AWS_PROFILE=kbasedev
sam validate --template-file dbapi_lambda.yml
sam build --template-file dbapi_lambda.yml --use-container
sam package --s3-bucket ${DB_API_LAMBDA_S3_BUCKET} --region eu-west-1 # get DB_API_LAMBDA_S3_BUCKET from .env file
sam deploy --stack-name db-api-lambda-public --s3-bucket ${DB_API_LAMBDA_S3_BUCKET} --region eu-west-1 --no-fail-on-empty-changeset \
  --capabilities CAPABILITY_IAM
