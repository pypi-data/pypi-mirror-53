import os

from troposphere.iam import Role, Policy
from aws_cf_custom_resources.abstract_custom_service import AbstractCustomService
from aws_cf_custom_resources.cognito_facebook import cognito_facebook_root


class CognitoFacebookService(AbstractCustomService):
    def __init__(self):
        super().__init__()

        self.src = os.path.join(
            cognito_facebook_root,
            'package'
        )

        self.lambda_handler = 'index.handler'
        self.lambda_runtime = 'python3.6'
        self.lambda_memory = 128
        self.lambda_timeout = 60
        self.lambda_name = 'CfCustomResourceCognitoFacebook'
        self.lambda_description = (
            'Lambda function enabling AWS CloudFormation to create Facebook as an '
            'identity provider for AWS Cognito user pool.'
        )

    def role(self) -> Role:
        return Role(
            "CfCustomResourceFacebookCognitoLambdaRole",
            Path="/",
            Policies=[Policy(
                PolicyName="CfCustomResourceFacebookCognitoLambdaPolicy",
                PolicyDocument={
                    "Version": "2012-10-17",
                    "Statement": [{
                        "Action": ["logs:*"],
                        "Resource": "arn:aws:logs:*:*:*",
                        "Effect": "Allow"
                    }, {
                        "Action": [
                            "cognito-idp:CreateIdentityProvider",
                            "cognito-idp:UpdateIdentityProvider",
                            "cognito-idp:DeleteIdentityProvider",
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
