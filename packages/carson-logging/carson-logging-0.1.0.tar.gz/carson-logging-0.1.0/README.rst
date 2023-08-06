===================
CLogging
===================

.. sectnum::



Install
===============

    * ``pip install carson-logging``

import packages
===============

.. code-block:: python

    from Carson.Class.Logging import CLogging

USAGE
===============

Basic
-----------

.. code-block:: python

    log = CLogging("log_name", "temp_dir/xxx.log")
    log.info('info msg')
    log.debug('info msg')
    log.warning('info msg')
    log.error('info msg')
    log.critical('info msg')
	
Advanced
----------

.. code-block:: python

    my_define_format = logging.Formatter(u'%(asctime)s|%(levelname)s|%(name)s|%(message)s')
    log = CLogging("log_name", "C:dir/xxx.log", logging.INFO, 'w', my_define_format, stream_handler_on=True, stream_level=logging.ERROR)

Issues
===============

* `Issues <https://github.com/CarsonSlovoka/carson-logging/issues>`_