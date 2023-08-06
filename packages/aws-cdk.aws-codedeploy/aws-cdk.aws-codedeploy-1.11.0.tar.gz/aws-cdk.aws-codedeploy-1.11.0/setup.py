import json
import setuptools

kwargs = json.loads("""
{
    "name": "aws-cdk.aws-codedeploy",
    "version": "1.11.0",
    "description": "The CDK Construct Library for AWS::CodeDeploy",
    "url": "https://github.com/aws/aws-cdk",
    "long_description_content_type": "text/markdown",
    "author": "Amazon Web Services",
    "project_urls": {
        "Source": "https://github.com/aws/aws-cdk.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "aws_cdk.aws_codedeploy",
        "aws_cdk.aws_codedeploy._jsii"
    ],
    "package_data": {
        "aws_cdk.aws_codedeploy._jsii": [
            "aws-codedeploy@1.11.0.jsii.tgz"
        ],
        "aws_cdk.aws_codedeploy": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii~=0.17.1",
        "publication>=0.0.3",
        "aws-cdk.aws-autoscaling~=1.11,>=1.11.0",
        "aws-cdk.aws-cloudwatch~=1.11,>=1.11.0",
        "aws-cdk.aws-elasticloadbalancing~=1.11,>=1.11.0",
        "aws-cdk.aws-elasticloadbalancingv2~=1.11,>=1.11.0",
        "aws-cdk.aws-iam~=1.11,>=1.11.0",
        "aws-cdk.aws-lambda~=1.11,>=1.11.0",
        "aws-cdk.aws-s3~=1.11,>=1.11.0",
        "aws-cdk.core~=1.11,>=1.11.0"
    ]
}
""")

with open('README.md') as fp:
    kwargs['long_description'] = fp.read()


setuptools.setup(**kwargs)
