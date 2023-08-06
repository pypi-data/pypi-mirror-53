# Django KCK
Django KCK is data orchestration for Django.  It can be used for:
* scheduled data imports from remote sources
* ensuring each data product kept fresh, either by updating at a regular
  interval or when there is a change in source data on upon which it
  depends
* preparing complex data products in advance of a likely request
* simplifying and optimizing complex data flows

The development pattern Django KCK encourages for data products
emphasizes compartmentalization and simplification over complexity,
cached data with configurable refresh routines over real-time
computation, and common-sense optimizations over sprawling distributed
parallelism.

## History
Django KCK is a simplified version of KCK that targets the Django
environment exclusively.  It also uses PostgreSQL as the cache backend,
instead of Cassandra.

## Quick Install

## Basic Usage

```
# myapp/primers.py

from kck import Primer


class TitleListPrimer(Primer):
    key = 'title_list'
    parameters = [
        {"name": "id", "from_str": int}
    ]

    def compute(self, key):
        param_dict = self.key_to_param_dict(key)
        results = [{ 'title': lkp_title(id) } for id in param_dict['id_list']]
        return results
```

```
# myapp/views.py

from kck import Cache
from django.http import JsonResponse

def first_data_product_view(request, author_id):
    cache = Cache.get_instance()
    title_list = cache.get(f'title_list/{author_id}')
    return JsonResponse(title_list)

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
