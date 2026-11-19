import boto3
from aws.aws_config import (
    AWS_REGION,
    AWS_SNS_TOPIC_ARN,
    get_boto3_session
)

def publish_notification(subject, message):
    """
    Sends a notification through Amazon SNS.
    Returns True if published successfully, otherwise False.
    """

    try:
        session = get_boto3_session()

        if not session:
            print("[SNS] AWS session unavailable.")
            return False

        if not AWS_SNS_TOPIC_ARN:
            print("[SNS] Topic ARN not configured.")
            return False

        sns = session.client(
            "sns",
            region_name=AWS_REGION
        )

        response = sns.publish(
            TopicArn=AWS_SNS_TOPIC_ARN,
            Subject=subject[:100],
            Message=message
        )

        print("[SNS] Notification published:",
              response.get("MessageId"))

        return True

    except Exception as e:
        print(f"[SNS] Notification error: {e}")
        return False
