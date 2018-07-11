Prometheus Grafana setup
========================

Firstly you need add this projects URL to the prometheus.yml file for the installed prometheus on the system

For example for the local setup:

 ```
    - job_name: FORD
    # If django_prometheus metric exporter is installed and configured,
    # it will export feti metrics.
    static_configs:
      - targets: ['0.0.0.0:63102']
    scrape_interval: 5s
    scrape_timeout: 15s
```

#### Then to set up the dashboard in grafana:

- Remove the ```.TEMPLATE``` extension in the example dashboard file in the ```docs/prometheus``` directory
- Setup a data source to point to the prometheus running instance URL such as *http://localhost:9090*
- And then import the template dashboard
