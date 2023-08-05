# Django KCK
Django KCK is a flexible data pipeline framework for Django that makes
it easy to write code that periodically imports data from remote sources.

It's easy to define data products that depend on those updates and to
make sure they refresh as soon as possible after an update.

It's easy to make sure that some data products refresh every five
minutes while others refresh on demand, returning fresh data every time
they're requested.

Django KCK is designed to manage data products and keep them up-to-date,
whether they reflect authoritative sources like the daily reports from a
system of cash registers or conglomerate data products assembled from
assortments of authoritative and derivative data products, with uniquely
configured refresh schedules and triggers.

## History
Django KCK is a simplified version of KCK that targets the Django
environment exclusively.  It also uses PostgreSQL as the cache backend,
instead of Cassandra.

## Quick Install

## Basic Usage

```
# myapp/primers.py

from kck import Primer

class FirstDataProduct(Primer):
    key = 'first_data_product'
    parameters = [
        {"name": "id", "from_str": int}
    ]

    def compute(self, key):
        param_dict = self.key_to_param_dict(key)
        .
        .
        .
        return result
```

```
# myapp/views.py

from kck import Cache

cache = Cache.get_instance()


```

## Theory
Essentially, Django KCK is a lazy-loading cache.  Instead of warming the
cache in advance, Django KCK lets a developer tell the cache how to
prime itself in the event of a cache miss.

If we don't warm the cache in advance and we ask the cache for a data
product that depends on a hundred other data products in the cache, each
of which either gathers or computes data from other sources, then this
design will only generate or request the data that is absolutely
necessary for the computation.  In this way, Django KCK is able to do
the last amount of work possible to accomplish the task.

To further expedite the process or building derivative data products,
Django KCK includes mechanisms that allow for periodic or triggered
updates of data upon which a data product depends, such that it will be
immediately available when a request is made.

It also makes it possible to "augment" derivative data products with
new information so that, for workloads that can take advantage of the
optimization, a data product can be updated in place, without
regenerating the product in its entirety.  Where it works, this approach
can turn minutes of computation into milliseconds.
