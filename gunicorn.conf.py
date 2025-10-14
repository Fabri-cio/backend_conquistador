import os
import multiprocessing

cpu_count = multiprocessing.cpu_count()

# Workers
workers = int(os.getenv("GUNICORN_WORKERS", min(cpu_count * 2 + 1, 12)))

# Threads
threads = int(os.getenv("GUNICORN_THREADS", 3))

# Timeout
timeout = int(os.getenv("GUNICORN_TIMEOUT", 90))

# Logging para Railway
capture_output = True
