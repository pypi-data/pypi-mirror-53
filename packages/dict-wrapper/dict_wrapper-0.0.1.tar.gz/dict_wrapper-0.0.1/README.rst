dict_wrapper

=====
user DictWrapper to visit the value like an object

Installing
----------

Install and update using `pip`_:

.. code-block:: text

    pip install -U dict_wrapper


A Simple Example
----------------

.. code-block:: python

    data = {
        "who": 'your name',
        "area": ['specify', 'china'],
        "province": {
            "city": ['shenzhen', 'guangzhou']
        }
    }
    config = DictWrapper(data)
    assert config.who == 'your name'
    assert config.province.city == ['shenzhen', 'guangzhou']
    print(config.area)
