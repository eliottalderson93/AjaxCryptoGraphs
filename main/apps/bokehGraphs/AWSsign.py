import requests, boto3
from aws_requests_auth.aws_auth import AWSRequestsAuth
def amazonCall(url):
    sts_client = boto3.client('sts')
    # Call the assume_role method of the STSConnection object and pass the role
    # ARN and a role session name.
    assumedRoleObject = sts_client.assume_role(
        RoleArn="arn:aws:iam::543303400543:role/MyApiCall",
        RoleSessionName="mySession"
    )
    # From the response that contains the assumed role, get the temporary 
    # credentials that can be used to make subsequent API calls
    credentials = assumedRoleObject['Credentials']
    # Use the temporary credentials that AssumeRole returns to make a 
    # connection to Amazon S3  
    # s3_resource = boto3.resource(
    #     's3',
    #     aws_access_key_id = ,
    #     aws_secret_access_key = ,
    #     aws_session_token = credentials['SessionToken'],
    # )
    # print("s3 resource:",s3_resource)
    # # let's talk to our AWS Elasticsearch cluster
    auth = AWSRequestsAuth(aws_access_key= credentials['AccessKeyId'],
                        aws_secret_access_key= credentials['SecretAccessKey'],
                        aws_host='ec2-18-220-161-116.us-east-2.compute.amazonaws.com',
                        aws_region='us-east-2',
                        aws_service='compute')
    response = requests.get(url, auth=auth)
    return response

    # The calls to AWS STS AssumeRole must be signed with the access key ID
    # and secret access key of an existing IAM user or by using existing temporary 
    # credentials such as those from antoher role. (You cannot call AssumeRole 
    # with the access key for the root account.) The credentials can be in 
    # environment variables or in a configuration file and will be discovered 
    # automatically by the boto3.client() function. For more information, see the 
    # Python SDK documentation: 
    # http://boto3.readthedocs.io/en/latest/reference/services/sts.html#client

    # create an STS client object that represents a live connection to the 
    # STS service
