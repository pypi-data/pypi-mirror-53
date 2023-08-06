Usage
----



To import the Class and satellite APIs for mainnet and testnet:

```python
from blocksat_api import blocksat
```

-----

Create a new order object to place a new order, increase an order bid, get an order status or delete an order:

```python
# create a new order object with optional message and network
o = blocksat.Order(message='Hello, world.', network='mainnet')
```

Methods called will return nothing upon success, storing the API status_code and a json-encoded response.text in the appropriate object attribute.

------


To check pending orders, queued orders, sent orders or the satellite lightning node info use the external methods which return a successful result as a json of response.text and a failure as a tuple of (response.status_code, response.reason, response.text):

```python
# to check sent_orders
sent_orders = blocksat.sent_orders(sat_url=blocksat.SATELLITE_API)
```

------