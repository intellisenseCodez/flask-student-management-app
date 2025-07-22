from flask import request
from prometheus_client import make_wsgi_app, Counter, Histogram, Gauge
from werkzeug.middleware.dispatcher import DispatcherMiddleware
import time


# Custom metrics
REQUEST_COUNT = Counter('http_request_total', 'Total HTTP Requests', ['method', 'status', 'path'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP Request Duration', ['method', 'status', 'path'])
ACTIVE_REQUESTS = Gauge('http_requests_in_progress','Number of active HTTP requests', ['method', 'path'])

DATABASE_OPERATIONS = Counter('database_operations_total','Total database operations',['operation_type'])

ERROR_COUNT = Counter('http_errors_total','Total HTTP Errors',['error_type'])

# System metrics
CPU_USAGE = Gauge('process_cpu_usage', 'Current CPU usage in percent')
MEMORY_USAGE = Gauge('process_memory_usage_bytes', 'Current memory usage in bytes')


def setup_metrics(app):
    """Add Prometheus metrics WSGI app to Flask"""
    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
        '/metrics': make_wsgi_app()
    })

def monitor_request(f):
    """Decorator to monitor requests"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        REQUEST_COUNT.labels(request.method, request.path, None).inc()
        ACTIVE_REQUESTS.labels(request.method, request.path).inc()
        
        try:
            response = f(*args, **kwargs)
            REQUEST_COUNT.labels(request.method, request.path, response.status_code).inc()
            return response
        except Exception as e:
            ERROR_COUNT.labels(type(e).__name__).inc()
            raise
        finally:
            latency = time.time() - start_time
            REQUEST_LATENCY.labels(request.method, request.path).observe(latency)
            ACTIVE_REQUESTS.labels(request.method, request.path).dec()
    
    wrapper.__name__ = f.__name__
    return wrapper

def track_db_operation(operation_type):
    """Track database operations"""
    DATABASE_OPERATIONS.labels(operation_type).inc()