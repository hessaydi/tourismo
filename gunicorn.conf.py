import multiprocessing
import os

# Binding
bind = "0.0.0.0:8000"

# Workers: 2 * CPUs + 1 is the standard formula
workers = int(os.environ.get("GUNICORN_WORKERS", multiprocessing.cpu_count() * 2 + 1))
worker_class = "sync"
threads = int(os.environ.get("GUNICORN_THREADS", "2"))

# Timeouts
timeout = 120
keepalive = 5
graceful_timeout = 30

# Reliability: recycle workers to prevent memory leaks
max_requests = 1000
max_requests_jitter = 100

# Logging
accesslog = "-"
errorlog = "-"
loglevel = os.environ.get("GUNICORN_LOG_LEVEL", "info")
access_log_format = '{"remote_ip":"%(h)s","method":"%(m)s","path":"%(U)s","status":%(s)s,"response_bytes":%(b)s,"duration_ms":%(M)s}'

# Process naming
proc_name = "tourismo"
