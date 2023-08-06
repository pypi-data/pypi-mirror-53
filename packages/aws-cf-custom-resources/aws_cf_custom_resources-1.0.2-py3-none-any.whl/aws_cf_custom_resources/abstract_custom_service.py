from abc import ABC, abstractmethod
from troposphere import GetAtt, Template
from troposphere.awslambda import Function, Code
from troposphere.iam import Role
from aws_cf_custom_resources.global_config_manager import GlobalConfigManager


class AbstractCustomService(ABC):
    def __init__(self):
        self.src = None
        self.lambda_handler = None
        self.lambda_runtime = None
        self.lambda_memory = None
        self.lambda_timeout = None
        self.lambda_description = None
        self.lambda_name = None

    @abstractmethod
    def role(self) -> Role:
        pass

    def service_token(self) -> GetAtt:
        return GetAtt(self.function(), 'Arn')

    def function(self) -> Function:
        assert self.lambda_name
        assert self.lambda_handler
        assert self.lambda_runtime
        assert self.lambda_memory
        assert self.lambda_timeout
        assert self.lambda_description

        return Function(
            self.lambda_name,
            Code=Code(
                S3Bucket=GlobalConfigManager.get_params().custom_resources_bucket,
                S3Key=self.lambda_name
            ),
            Handler=self.lambda_handler,
            Role=GetAtt(self.role(), "Arn"),
            Runtime=self.lambda_runtime,
            MemorySize=self.lambda_memory,
            FunctionName=self.lambda_name,
            Timeout=self.lambda_timeout,
            Description=self.lambda_description
        )

    def add(self, template: Template):
        template.add_resource(self.function())
        template.add_resource(self.role())
