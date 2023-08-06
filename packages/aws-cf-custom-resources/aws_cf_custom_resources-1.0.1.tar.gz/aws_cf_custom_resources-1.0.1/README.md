### aws-cf-custom-resources

#### Description
Container project which has different custom resources for AWS CloudFormation.
All of the resources use Troposphere python wrapper to manage CF templates.

#### Installation

```bash
pip install aws-cf-custom-resources
```

#### Usage
Create and add custom resources to your existing Troposphere template.

Before using this package a **global config manager** must be initialized.

Use **custom resources builder** to automatically upload and manage custom resources on AWS.
