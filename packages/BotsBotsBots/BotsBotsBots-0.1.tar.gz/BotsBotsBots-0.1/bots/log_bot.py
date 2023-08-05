import logging

# pip install logdna
from logdna import LogDNAHandler

# https://github.com/logdna/python

key = '5ccb04bac8f5683fc91c00410096c5da'

log = logging.getLogger('logdna')
log.setLevel(logging.INFO)

options = {'hostname': 'pytest', 'ip': '10.0.1.1', 'mac': 'C0:FF:EE:C0:FF:EE', 'index_meta': True}

# Defaults to False; when True meta objects are searchable

test = LogDNAHandler(key, options)

log.addHandler(test)

log.warning("Warning message", {'app': 'bloop'})
log.info("Info message")

# Simplest use case
log.info('My Sample Log Line')

# Add a custom level
log.info('My Sample Log Line', {'level': 'MyCustomLevel'})

# Include an App name with this specific log
log.info('My Sample Log Line', {'level': 'Warn', 'app': 'myAppName'})

# Pass associated objects along as metadata
meta = {
    'foo': 'bar',
    'nested': {
        'nest1': 'nested text'
    }
}

opts = {
    'level': 'warn',
    'meta': meta
}

log.info('My Sample Log Line', opts)
