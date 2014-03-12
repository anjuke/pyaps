## APS for Python

Python client library for using [Anjuke Private Service](http://git.corp.anjuke.com/_aps/spec).

Version 1.2

## How to use

```python
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from aps.client import APS
from aps.base import wait_for_replies

bayes_client = APS()
bayes_client.connect("tcp://10.10.3.46:51000")
mss_client = APS()
mss_client.connect("tcp://10.10.3.46:6000")

bayes_seq = bayes_client.start_request("bayes->guess_all", ["hz_prop", "未来资产大厦"])
mss_seq = mss_client.start_request("search", ["浦东两室精装修","ac"])

replies = wait_for_replies(timeout=600)

if bayes_seq in replies:
    bayes_rep = replies.get(bayes_seq)
    print(bayes_rep)
if mss_seq in replies:
    mss_rep = replies.get(mss_seq)
    print(mss_rep)
```

## Quick Start

grab the source

```
git clone git://git.corp.anjuke.com/_aps/pyaps
cd pyaps
python setup.py install
```

or in `setup.py`

```python
setup(
    # ...

    install_requires = [
        # ...
        'aps==1.2.0.0.dev'
    ],

    dependency_links = [
        'http://git.corp.anjuke.com/_aps/pyaps/archive/master.zip#aps-1.2.0.0.dev'
    ]

    # ...
)
```

run tests

```
make test
```

**MAKE SURE ALL TESTS PASSED BEFORE CONTRIBUTING ANY CODE**
