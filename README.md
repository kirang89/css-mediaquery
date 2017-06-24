## css-mediaquery

[![Build Status](https://travis-ci.org/kirang89/css-mediaquery.svg?branch=master)](https://travis-ci.org/kirang89/css-mediaquery) [![PyPI version](https://badge.fury.io/py/cssmediaquery.svg)](https://badge.fury.io/py/cssmediaquery)

Parses and determines if a given CSS Media Query matches a set of values.

This is a port of https://github.com/ericf/css-mediaquery.

### Usage

```python

from cssmediaquery import match, parse

isamatch = match('screen and (min-width: 40em)', {
	'type'  : 'screen',
	'width' : '1024px'
})
# returns True

ast = parse('screen and (min-width: 40em)')
print ast
# [
#    {
#        'inverse': 'false',
#        'type'   : 'screen',
#        'expressions': [{
#                'modifier': 'min',
#                'feature': 'width',
#                'value': '40em'
#         }]
#    }
# ]
```

### Installing

    $ pip install cssmediaquery

### Running Tests

    python tests.py -v
