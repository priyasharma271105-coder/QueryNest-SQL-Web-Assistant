"""
QueryNest — AWS IAM (Identity & Access Management) Service
Provides identity verification, STS caller inspection, and least-privilege policy generation.
"""
import json
from aws import aws_config

def get_current_identity() -> dict:
    """
    Checks the active AWS identity using AWS STS (Security Token Service).
    Returns identity metadata if configured, or local development status if disabled.
    """
    session = aws_config.get_boto3_session()
    if session is None:
        return {
            "mode": "LOCAL_DEVELOPMENT",
            "connected": False,
            "message": "AWS is disabled or credentials are not configured. Running with local development credentials.",
            "account_id": "LOCAL-MOCK-ACCOUNT",
            "arn": "arn:aws:iam::local:user/querynest-dev-user",
            "user_id": "LOCAL-USER-QUERYNEST"
        }
    
    try:
        sts = session.client('sts')
        identity = sts.get_caller_identity()
        return {
            "mode": "AWS_CLOUD",
            "connected": True,
            "account_id": identity.get("Account"),
            "arn": identity.get("Arn"),
            "user_id": identity.get("UserId"),
            "message": f"Successfully authenticated as {identity.get('Arn')}"
        }
    except Exception as e:
        return {
            "mode": "ERROR",
            "connected": False,
            "error": str(e),
            "message": f"Failed to authenticate with AWS STS: {e}"
        }

def get_recommended_iam_policy(bucket_name: str = None, secret_name: str = None) -> dict:
    """
    Generates a recommended least-privilege IAM Policy JSON document
    suitable for attaching to the QueryNest IAM User or EC2/Lambda Role.
    """
    bucket = bucket_name or aws_config.S3_BUCKET_NAME
    secret = secret_name or aws_config.AWS_SECRET_NAME
    region = aws_config.AWS_REGION

    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "QueryNestS3Permissions",
                "Effect": "Allow",
                "Action": [
                    "s3:PutObject",
                    "s3:GetObject",
                    "s3:DeleteObject",
                    "s3:ListBucket"
                ],
                "Resource": [
                    f"arn:aws:s3:::{bucket}",
                    f"arn:aws:s3:::{bucket}/*"
                ]
            },
            {
                "Sid": "QueryNestCloudWatchLogs",
                "Effect": "Allow",
                "Action": [
                    "logs:CreateLogGroup",
                    "logs:CreateLogStream",
                    "logs:PutLogEvents",
                    "logs:DescribeLogStreams"
                ],
                "Resource": f"arn:aws:logs:{region}:*:log-group:/querynest/*"
            },
            {
                "Sid": "QueryNestSecretsManager",
                "Effect": "Allow",
                "Action": [
                    "secretsmanager:GetSecretValue"
                ],
                "Resource": f"arn:aws:secretsmanager:{region}:*:secret:{secret}*"
            },
            {
                "Sid": "QueryNestLambdaInvocation",
                "Effect": "Allow",
                "Action": [
                    "lambda:InvokeFunction"
                ],
                "Resource": f"arn:aws:lambda:{region}:*:function:querynest-*"
            },
            {
                "Sid": "QueryNestCloudTrailAudit",
                "Effect": "Allow",
                "Action": [
                    "cloudtrail:DescribeTrails",
                    "cloudtrail:LookupEvents"
                ],
                "Resource": "*"
            }
        ]
    }
    return policy

def save_policy_template_file(output_path: str):
    """Saves the least-privilege policy to a JSON file for easy reference."""
    policy = get_recommended_iam_policy()
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(policy, f, indent=2)
