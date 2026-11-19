"""
QueryNest — AWS CloudTrail Activity & Security Audit Service
Tracks AWS API calls, account management events, and security access logs.
Provides an audit inspection interface and graceful local fallback.
"""
from datetime import datetime
from aws import aws_config

def _get_cloudtrail_client():
    session = aws_config.get_boto3_session()
    if session is None:
        return None
    try:
        return session.client('cloudtrail')
    except Exception as e:
        print(f"[CloudTrail] Client init error: {e}")
        return None

def check_trail_status(trail_name: str = None) -> dict:
    """
    Checks if CloudTrail logging is actively recording account events.
    """
    client = _get_cloudtrail_client()
    t_name = trail_name or aws_config.CLOUDTRAIL_NAME

    if client is None:
        return {
            "mode": "LOCAL_DEVELOPMENT",
            "is_logging": False,
            "trail_name": t_name,
            "status": "AWS CloudTrail disabled in local development mode.",
            "message": "When deployed to AWS, CloudTrail records all S3, Lambda, and Secrets Manager API activities."
        }

    try:
        trails = client.describe_trails(trailNameList=[t_name])
        trail_list = trails.get('trailList', [])
        if not trail_list:
            return {
                "mode": "AWS_CLOUD",
                "is_logging": False,
                "trail_name": t_name,
                "status": f"Trail '{t_name}' not found in region {aws_config.AWS_REGION}."
            }

        status = client.get_trail_status(Name=t_name)
        return {
            "mode": "AWS_CLOUD",
            "is_logging": status.get('IsLogging', False),
            "trail_name": t_name,
            "latest_delivery_time": str(status.get('LatestDeliveryTime', 'N/A')),
            "status": "Active" if status.get('IsLogging') else "Stopped"
        }
    except Exception as e:
        return {
            "mode": "ERROR",
            "is_logging": False,
            "error": str(e),
            "message": f"Could not fetch CloudTrail status: {e}"
        }

def get_recent_audit_events(lookup_attribute_key: str = None, lookup_attribute_value: str = None, max_results: int = 10) -> list:
    """
    Fetches recent API events from CloudTrail (e.g. S3 file access, Secret lookups).
    Returns mock audit entries in local dev mode.
    """
    client = _get_cloudtrail_client()
    if client is None:
        # Return mock audit trail for local testing
        return [
            {
                "EventId": "local-audit-001",
                "EventName": "LocalDevelopmentInit",
                "EventTime": datetime.now().isoformat(),
                "Username": "querynest-local-developer",
                "EventSource": "querynest.local",
                "ReadOnly": "True"
            }
        ]

    try:
        kwargs = {'MaxResults': max_results}
        if lookup_attribute_key and lookup_attribute_value:
            kwargs['LookupAttributes'] = [{
                'AttributeKey': lookup_attribute_key,
                'AttributeValue': lookup_attribute_value
            }]
        response = client.lookup_events(**kwargs)
        events = []
        for ev in response.get('Events', []):
            events.append({
                "EventId": ev.get('EventId'),
                "EventName": ev.get('EventName'),
                "EventTime": str(ev.get('EventTime')),
                "Username": ev.get('Username', 'N/A'),
                "EventSource": ev.get('EventSource'),
                "ReadOnly": str(ev.get('ReadOnly', 'N/A'))
            })
        return events
    except Exception as e:
        print(f"[CloudTrail] Error looking up events: {e}")
        return []
