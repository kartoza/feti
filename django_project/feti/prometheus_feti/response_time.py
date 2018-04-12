from __future__ import print_function

# coding: utf-8
__author__ = 'Alison Mukoma <alison@kartoza.com>'
__copyright__ = 'kartoza.com'

import time
from prometheus_client import Summary, Counter


from prometheus_client.process_collector import ProcessCollector

ProcessCollector(namespace='mydaemonCustomCollector', pid=lambda: open(
        '/proc/cpuinfo').read())


import random
import time

from prometheus_client import generate_latest, REGISTRY, PROCESS_COLLECTOR, \
    Counter, Gauge, \
    Histogram


# Count the total number of HTTP requests that feti is recieving.
REQUESTS = Counter('http_requests_total', 'Total HTTP Requests (count)', ['method', 'endpoint', 'status_code'])

# A gauge to monitor the total number of in progress requests
IN_PROGRESS = Gauge('http_requests_inprogress', 'Number of in progress HTTP requests')

# A histogram to measure the latency of the HTTP requests
TIME_DELAY = Histogram('http_request_duration_seconds',
                       'HTTP request latency (seconds)')


@IN_PROGRESS.track_inprogress()
@TIME_DELAY.time()
def count_200():
    REQUESTS.labels(method='GET', status_code=200).inc()
    return generate_latest(REGISTRY)

@IN_PROGRESS.track_inprogress()
@TIME_DELAY.time()
def count_404():
    REQUESTS.labels(method='GET', status_code=404).inc()
    return generate_latest(REGISTRY)

@IN_PROGRESS.track_inprogress()
@TIME_DELAY.time()
def count_500():
    REQUESTS.labels(method='GET', status_code=500).inc()
    return generate_latest(REGISTRY)

PROCESS_COLLECTION = Gauge('collect_running_process',
                       'Collect running processes')

@PROCESS_COLLECTION.track_inprogress()
def running_processes():
    PROCESS_COLLECTOR.collect()
    return generate_latest(REGISTRY)

