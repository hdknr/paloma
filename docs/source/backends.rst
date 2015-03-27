================
Backends
================

.. contents:: Backends

Django Email Backend
=====================

- refer to https://docs.djangoproject.com/en/dev/topics/email/#email-backends

.. todo::
    
    - Use intefsphinx to Djanog document

Example
--------

.. code-block:: python

    if 'test' not in sys.argv:
        #: on production, send messages thru Celery task queue
        #:
        EMAIL_BACKEND = 'paloma.backends.CeleryEmailBackend'
    else:
        #: on testin, save messages directory to Journal model
        #:
        EMAIL_BACKEND = 'paloma.backends.JournalEmailBackend'


Email Backends
====================================

.. _paloma.backends.PalomaEmailBackend:

PalomaEmailBackend
--------------------------------

.. autoclass:: paloma.backends.PalomaEmailBackend
    :members:

.. _paloma.backends.JournalEmailBackend:

JournalEmailBackend
--------------------------------

.. autoclass:: paloma.backends.JournalEmailBackend
    :members:

