#!/usr/bin/env python

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

import certifi
import json

############

def get_total_list(url):
    """
    Receive the content of ``url``, parse it as JSON and return the object.

    Parameters
    ----------
    url : str

    Returns
    -------
    dict
    """
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")
    return json.loads(data)

allTicket = ("https://financialmodelingprep.com/api/v3/financial-statement-symbol-lists?apikey=1a82bbd72952f10cfeb9bf5ba9b205b2")
print(get_total_list(allTicket))