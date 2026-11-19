"""
QueryNest — Amazon S3 Storage Service
Handles storing generated PDFs, query files, and uploaded assets.
Supports seamless offline local fallback when AWS is disabled.
"""
import os
import io
from pathlib import Path
from aws import aws_config

# Local fallback base directory
LOCAL_STORAGE_BASE = Path(__file__).resolve().parent.parent / "data"

def _get_s3_client():
    session = aws_config.get_boto3_session()
    if session is None:
        return None
    try:
        return session.client('s3')
    except Exception as e:
        print(f"[S3 Service] Failed to initialize S3 client: {e}")
        return None

def upload_file(file_content, s3_key: str, content_type: str = "application/octet-stream") -> dict:
    """
    Uploads file content (bytes, str, or file-like object) to S3 or local disk.
    
    :param file_content: bytes, string, or file-like object
    :param s3_key: S3 object key or relative file path (e.g. 'generated_pdfs/user1/report.pdf')
    :param content_type: MIME type of the file
    :return: dict with upload details and status
    """
    s3 = _get_s3_client()
    clean_key = s3_key.replace('\\', '/')
    
    # Normalize bytes
    if isinstance(file_content, str):
        data_bytes = file_content.encode('utf-8')
    elif hasattr(file_content, 'read'):
        data_bytes = file_content.read()
        if isinstance(data_bytes, str):
            data_bytes = data_bytes.encode('utf-8')
    else:
        data_bytes = file_content

    # If S3 is enabled and connected
    if s3 is not None:
        try:
            s3.put_object(
                Bucket=aws_config.S3_BUCKET_NAME,
                Key=clean_key,
                Body=data_bytes,
                ContentType=content_type
            )
            return {
                "success": True,
                "storage": "S3",
                "bucket": aws_config.S3_BUCKET_NAME,
                "key": clean_key,
                "size": len(data_bytes),
                "url": f"https://{aws_config.S3_BUCKET_NAME}.s3.{aws_config.AWS_REGION}.amazonaws.com/{clean_key}"
            }
        except Exception as e:
            print(f"[S3 Service] S3 upload failed ({e}). Falling back to local storage.")

    # Local fallback
    local_path = LOCAL_STORAGE_BASE / clean_key
    local_path.parent.mkdir(parents=True, exist_ok=True)
    with open(local_path, 'wb') as f:
        f.write(data_bytes)

    return {
        "success": True,
        "storage": "LOCAL",
        "key": clean_key,
        "size": len(data_bytes),
        "local_path": str(local_path),
        "url": f"/data/{clean_key}"
    }

def get_file(s3_key: str) -> dict:
    """
    Retrieves file bytes from S3 or local disk.
    """
    clean_key = s3_key.replace('\\', '/')
    s3 = _get_s3_client()
    if s3 is not None:
        try:
            response = s3.get_object(Bucket=aws_config.S3_BUCKET_NAME, Key=clean_key)
            content = response['Body'].read()
            return {
                "success": True,
                "storage": "S3",
                "content": content,
                "content_type": response.get('ContentType', 'application/octet-stream')
            }
        except Exception as e:
            print(f"[S3 Service] S3 fetch failed ({e}). Checking local storage.")

    # Local fallback
    local_path = LOCAL_STORAGE_BASE / clean_key
    if local_path.exists():
        with open(local_path, 'rb') as f:
            content = f.read()
        return {
            "success": True,
            "storage": "LOCAL",
            "content": content,
            "local_path": str(local_path)
        }

    return {"success": False, "message": f"File '{clean_key}' not found in S3 or local storage."}

def generate_presigned_url(s3_key: str, expiration_seconds: int = 3600) -> str:
    """
    Generates an S3 presigned download URL, or returns a local route if AWS is disabled.
    """
    clean_key = s3_key.replace('\\', '/')
    s3 = _get_s3_client()
    if s3 is not None:
        try:
            url = s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': aws_config.S3_BUCKET_NAME, 'Key': clean_key},
                ExpiresIn=expiration_seconds
            )
            return url
        except Exception as e:
            print(f"[S3 Service] Presigned URL error: {e}")

    # Local fallback URL
    return f"/data/{clean_key}"

def delete_file(s3_key: str) -> bool:
    """Deletes the file from S3 and/or local storage."""
    clean_key = s3_key.replace('\\', '/')
    deleted = False
    s3 = _get_s3_client()
    if s3 is not None:
        try:
            s3.delete_object(Bucket=aws_config.S3_BUCKET_NAME, Key=clean_key)
            deleted = True
        except Exception as e:
            print(f"[S3 Service] S3 delete failed: {e}")

    local_path = LOCAL_STORAGE_BASE / clean_key
    if local_path.exists():
        try:
            local_path.unlink()
            deleted = True
        except Exception:
            pass

    return deleted

def save_generated_pdf(user_id: str, filename: str, pdf_bytes: bytes) -> dict:
    """
    Convenience method for saving QueryNest PDF exports to S3 or local storage.
    """
    clean_user = "".join(c for c in str(user_id) if c.isalnum() or c in ('-', '_'))
    key = f"{aws_config.S3_PDF_PREFIX}{clean_user}/{filename}"
    return upload_file(pdf_bytes, key, content_type="application/pdf")
