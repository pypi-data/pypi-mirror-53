import os

from aws_infrastructure_sdk.cloud_formation.custom_resources import custom_root_dir
from aws_infrastructure_sdk.cloud_formation.custom_resources.service.abstract_custom_service import AbstractCustomService
from troposphere.iam import Role, Policy


class CognitoDomainService(AbstractCustomService):
    def __init__(self):
        super().__init__()

        self.src = os.path.join(
            custom_root_dir,
            'package',
            'cognito_domain'
        )

        self.lambda_handler = 'index.handler'
        self.lambda_runtime = 'python3.6'
        self.lambda_memory = 128
        self.lambda_timeout = 60
        self.lambda_name = 'CfCustomResourceCognitoUserPoolDomainName'
        self.lambda_description = (
            'Lambda function enabling AWS CloudFormation '
            'to create domain name for AWS Cognito user pool.'
        )

    def role(self) -> Role:
        return Role(
            "CfCustomResourceCognitoUserPoolDomainNameLambdaRole",
            Path="/",
            Policies=[Policy(
                PolicyName="CfCustomResourceCognitoUserPoolDomainNameLambdaPolicy",
                PolicyDocument={
                    "Version": "2012-10-17",
                    "Statement": [{
                        "Action": ["logs:*"],
                        "Resource": "arn:aws:logs:*:*:*",
                        "Effect": "Allow"
                    }, {
                        "Action": [
                            "cognito-idp:CreateUserPoolDomain",
                            "cognito-idp:UpdateUserPoolDomain",
                            "cognito-idp:DeleteUserPoolDomain",
                        ],
                        "Resource": "*",
                        "Effect": "Allow"
                    }]
                })],
            AssumeRolePolicyDocument={"Version": "2012-10-17", "Statement": [
                {
                    "Action": ["sts:AssumeRole"],
                    "Effect": "Allow",
                    "Principal": {
                        "Service": [
                            "lambda.amazonaws.com",
                        ]
                    }
                }
            ]},
        )
