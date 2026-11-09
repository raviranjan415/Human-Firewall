"""Gunicorn WSGI production server configuration for Human Firewall replicas."""

import multiprocessing
import os

# Binding
bind = f"0.0.0.0:{os.environ.get('PORT', '5000')}"

# Worker processes: 2-4 per core is standard, defaulting to 4 for container replicas
workers = int(os.environ.get("GUNICORN_WORKERS", 4))
threads = int(os.environ.get("GUNICORN_THREADS", 2))
worker_class = "gthread"

# Connection limits
worker_connections = 1000
backlog = 2048

# Timeouts
timeout = int(os.environ.get("GUNICORN_TIMEOUT", 30))
graceful_timeout = 30
keepalive = 2

# Logging (Structured stdout/stderr for Docker and Prometheus scrapers)
accesslog = "-"
errorlog = "-"
loglevel = os.environ.get("GUNICORN_LOG_LEVEL", "info")
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(L)s'

# Process naming
proc_name = "human_firewall_replica"

# Server Mechanics
daemon = False
pidfile = None
umask = 0o027
preload_app = True


def on_starting(server):
    server.log.info("Starting Human Firewall WSGI cluster replica on %s", bind)


def worker_int(worker):
    worker.log.info("Worker received SIGINT/SIGQUIT — draining connections gracefully")

