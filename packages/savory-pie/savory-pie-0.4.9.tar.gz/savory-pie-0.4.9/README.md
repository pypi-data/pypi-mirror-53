#Savory Pie

Savory Pie is an API building library, we give you the pieces to build the API
you need. Currently Django is the main target, but the only dependencies on
Django are a single view and Resources and Fields that understand Django's ORM.


[![Build Status](https://travis-ci.org/RueLaLaTech/savory-pie.svg?branch=master)](https://travis-ci.org/RueLaLaTech/savory-pie)
[![Coverage Status](https://coveralls.io/repos/RueLaLa/savory-pie/badge.svg?branch=master&service=github)](https://coveralls.io/github/RueLaLa/savory-pie?branch=master)

[![PyPi version](https://pypip.in/v/savory-pie/badge.png)](https://crate.io/packages/savory-pie/)
[![PyPi downloads](https://pypip.in/d/savory-pie/badge.png)](https://crate.io/packages/savory-pie/)
[![PyPi license](https://pypip.in/license/savory-pie/badge.png)](https://pypi.python.org/pypi/savory-pie/)

Documentation
-----
http://savory-pie.readthedocs.org/en/latest/


Installing
----
Note: it's recommended that you use `ujson` over the built in `json` library due to increased performance
```
    pip install savory-pie
```

Installing for Django
-----
```
    pip install django_dirty_bits >= 0.1.3.2
    pip install Django > 1.4
```

Local Development Environment
-----
It is highly recommended to use a virtualenv
```
    pip install -r requirements.txt
    pip install -e .
```


Running Tests
-----
```
    python run_tests.py
```

Running Tests Coverage
-----
```
    python run_tests.py --with-coverage
    coverage report -m  # To check the %
    coverage html
```

Updating PyPi (to whom it may concern)
-----
Build a release (e.g. `dist/savory-pie-0.2.0.tar.gz`), then upload via the PyPi website.
```
python setup.py sdist
```


```
its a pie, mate

        ---                       ---
    -.UU   UU.-     _____     -.UU    UU.-
   -UU       UU.------------.UU         UU-
   -U   ``                       ``     U-
    ~Uu  ```                   ```   uU~
     ~u                              u~
      '       ()            ()       '
       '           / "" \           '
      ~            |    |            ~
       ~           \    /           ~
       ~             ''             ~
        ~          /-----\         ~
          ~~~                  ~~~
              ~~~~~~~~~~~~~~~~
```
