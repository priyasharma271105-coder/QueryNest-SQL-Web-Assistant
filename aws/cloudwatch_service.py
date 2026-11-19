"""
QueryNest — AWS CloudWatch Logging & Metrics Service
Provides centralized application logging and operational metrics monitoring.
Falls back safely to local console/file logging when AWS is disabled.
"""
import time
import logging
from pathlib import Path
from aws import aws_config

LOCAL_LOG_FILE = Path(__file__).resolve().parent.parent / "data" / "querynest_app.log"

class CloudWatchLoggingHandler(logging.Handler):
    """
    Custom Python logging handler that delivers log records to AWS CloudWatch Logs.
    Falls back to a local file/console if AWS is unconfigured.
    """
    def __init__(self, log_group=None, log_stream=None):
        super().__init__()
        self.log_group = log_group or aws_config.CLOUDWATCH_LOG_GROUP
        self.log_stream = log_stream or aws_config.CLOUDWATCH_LOG_STREAM
        self._sequence_token = None
        self._client = None
        self._stream_ready = False

    def _get_client(self):
        if self._client is None:
            session = aws_config.get_boto3_session()
            if session:
                try:
                    self._client = session.client('logs')
                except Exception as e:
                    print(f"[CloudWatch] Client init error: {e}")
        return self._client

    def _ensure_stream(self):
        if self._stream_ready or not self._get_client():
            return
        client = self._client
        try:
            client.create_log_group(logGroupName=self.log_group)
        except client.exceptions.ResourceAlreadyExistsException:
            pass
        except Exception:
            pass

        try:
            client.create_log_stream(logGroupName=self.log_group, logStreamName=self.log_stream)
        except client.exceptions.ResourceAlreadyExistsException:
            pass
        except Exception:
            pass
        self._stream_ready = True

    def emit(self, record):
        msg = self.format(record)
        client = self._get_client()
        timestamp_ms = int(time.time() * 1000)

        if client is not None:
            try:
                self._ensure_stream()
                kwargs = {
                    'logGroupName': self.log_group,
                    'logStreamName': self.log_stream,
                    'logEvents': [{'timestamp': timestamp_ms, 'message': msg}]
                }
                if self._sequence_token:
                    kwargs['sequenceToken'] = self._sequence_token
                response = client.put_log_events(**kwargs)
                self._sequence_token = response.get('nextSequenceToken')
                return
            except Exception as e:
                # If sequence token invalid, clear it and retry next time
                self._sequence_token = None

        # Local fallback log write
        try:
            LOCAL_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(LOCAL_LOG_FILE, 'a', encoding='utf-8') as f:
                f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")
        except Exception:
            pass

def log_event(level: str, message: str, extra: dict = None):
    """
    Direct helper to log an application event (e.g. login, query search, PDF export).
    """
    logger = logging.getLogger("QueryNest")
    full_msg = f"{message} | extra: {extra}" if extra else message
    lvl = getattr(logging, level.upper(), logging.INFO)
    logger.log(lvl, full_msg)

def emit_metric(metric_name: str, value: float = 1.0, unit: str = "Count", dimensions: list = None) -> bool:
    """
    Puts custom metrics to CloudWatch (Namespace: QueryNest/Application).
    In local dev mode, logs metric to standard output.
    """
    session = aws_config.get_boto3_session()
    if session is not None:
        try:
            cw = session.client('cloudwatch')
            metric_data = {
                'MetricName': metric_name,
                'Value': value,
                'Unit': unit,
                'Timestamp': time.time()
            }
            if dimensions:
                metric_data['Dimensions'] = dimensions
            cw.put_metric_data(
                Namespace='QueryNest/Application',
                MetricData=[metric_data]
            )
            return True
        except Exception as e:
            print(f"[CloudWatch] Metric emission failed: {e}")

    # Local mode fallback
    # print(f"[Local Metric] QueryNest/Application -> {metric_name}: {value} {unit}")
    return True

def setup_cloudwatch_logging(app=None):
    """
    Initializes CloudWatch logging for the Flask application.
    """
    handler = CloudWatchLoggingHandler()
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] [%(name)s] %(message)s')
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)

    root_logger = logging.getLogger("QueryNest")
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(handler)

    if app:
        app.logger.addHandler(handler)
    return handler
