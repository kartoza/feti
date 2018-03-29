# coding: utf-8
__author__ = 'Alison Mukoma <alison@kartoza.com>'
__copyright__ = 'kartoza.com'

from prometheus_client import Counter, Gauge

landing_page_counter = Counter(
                'open_landing_page',
                'User open the landing page')


class PrometheusCounter:

    @staticmethod
    def increase_landing_page_view():
        landing_page_counter.inc()


status_codes_200_counter = Counter(
		'success_requests',
		'Success user requests (200).')

class StatusCodesCounter(object):
    """Object to hold status code counters."""

    from prometheus_client import Gauge

    gauge = Gauge('my_inprogress_requests', '')
    gauge.inc()  # Increment by 1
    gauge.dec(10)  # Decrement by given value
    gauge.set(4.2)  # Set to a given value

#------------------------------------
from prometheus_client import Counter

model_inserts_total = Counter(
    'feti_model_inserts_total', 'Number of inserts on a certain model',
		['model']
)
model_updates_total = Counter(
    'django_model_updates_total', 'Number of updates on a certain model', ['model']
)
model_deletes_total = Counter(
    'django_model_deletes_total', 'Number of deletes on a certain model', ['model']
)


def MetricsModelMixin(name):
    class Mixin(object):
        def _do_insert(self, *args, **kwargs):
            model_inserts_total.labels(name).inc()
            return super(Mixin, self)._do_insert(*args, **kwargs)

        def _do_update(self, *args, **kwargs):
            model_updates_total.labels(name).inc()
            return super(Mixin, self)._do_update(*args, **kwargs)

        def _do_delete(self, *args, **kwargs):
            model_deletes_total.labels(name).inc()
            return super(Mixin, self).delete(*args, **kwargs)

    return Mixin