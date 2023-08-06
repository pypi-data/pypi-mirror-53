# EPYLOG
Logs are the first.

This is a simple wrapper to standard [logging](https://docs.python.org/3/library/logging.html) library for Python.

Epylog provides to send log data to different sources e.g. file, rsyslog, graylog, http, etc.

Use different loggers for different needs and manage it from one place.

[![build status](https://travis-ci.org/iPhosgen/epylog.svg?branch=master)](https://travis-ci.org/iPhosgen/epylog) [![PyPi status](https://img.shields.io/pypi/v/epylog)](https://pypi.python.org/pypi/epylog) [![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FiPhosgen%2Fepylog.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2FiPhosgen%2Fepylog?ref=badge_shield)

## Installation

```shell script
pip install epylog
```

## Usage

- Move to project root directory and create `logging.cfg` file:
    ```shell script
    cd /project/root
    touch logging.cfg
    ```
- Fill configuration file with you logging settings. Push to `targets` array everything you want to send to. And fill `rules` array with logger names (use `*` wildcard if you want) and set which targets loggers can use:

    ```json
    {
      "targets": [
          {
            "name": "fl",
            "type":  "file",
            "filepath": "/var/log/my_log.log"
          },
          {
            "name": "gl",
            "type":  "graylog",
            "host": "localhost",
            "port": 12202,
            "facility": "test"
          },
          {
            "name": "rsl",
            "type":  "syslog",
            "address": "localhost",
            "facility": "test"
          }
      ],
      "rules": [
          {
            "name": "my_test_*",
             "level": "info",
             "write-to": "fl, gl",
             "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
          },
          {
            "name": "*",
             "level": "warning",
             "write-to": "rsl",
             "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
          }
      ]
    }
    ```
- Finally call `getLogger` function to initialize your logger:
    ```python
    from epylog import Logger

    # put some code here

    logger = Logger.getLogger('my_test_logger')
    logger.info('Hello from %s', logger.name)
    ```
- Enjoy sending your logs everywhere

## License

[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2FiPhosgen%2Fepylog.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2FiPhosgen%2Fepylog?ref=badge_large)
