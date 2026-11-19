"""
QueryNest — AWS Lambda Invocation Service
Invokes serverless Lambda functions for specialized tasks like SQL formatting & validation.
Falls back safely to local serverless emulation when AWS is disabled.
"""
import json
from aws import aws_config
from aws.lambda_functions.sql_formatter.lambda_function import format_sql as local_format_sql

def _get_lambda_client():
    session = aws_config.get_boto3_session()
    if session is None:
        return None
    try:
        return session.client('lambda')
    except Exception as e:
        print(f"[Lambda Service] Failed to initialize Lambda client: {e}")
        return None

def invoke_sql_formatter(sql_query: str) -> dict:
    """
    Invokes the AWS Lambda SQL formatter function if AWS is configured.
    Falls back seamlessly to local execution when running in development mode.
    """
    client = _get_lambda_client()
    function_name = aws_config.LAMBDA_SQL_FORMATTER

    # AWS Lambda Cloud Execution
    if client is not None:
        try:
            payload = json.dumps({"query": sql_query})
            response = client.invoke(
                FunctionName=function_name,
                InvocationType='RequestResponse',
                Payload=payload.encode('utf-8')
            )
            raw_payload = response['Payload'].read().decode('utf-8')
            res_json = json.loads(raw_payload)
            if 'body' in res_json and isinstance(res_json['body'], str):
                parsed_body = json.loads(res_json['body'])
            else:
                parsed_body = res_json
            parsed_body['execution_mode'] = 'AWS_LAMBDA'
            parsed_body['function_name'] = function_name
            return parsed_body
        except Exception as e:
            print(f"[Lambda Service] AWS Lambda invocation error ({e}). Falling back to local execution.")

    # Local Serverless Emulation
    result = local_format_sql(sql_query)
    result['execution_mode'] = 'LOCAL_EMULATION'
    result['function_name'] = function_name
    return result
