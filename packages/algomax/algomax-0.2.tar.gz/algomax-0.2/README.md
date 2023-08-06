# Algomax-CLI

A command line tools for working with EMAX API.

install the package with bellow command:

`-> pip install algomax`

use bellow command for working with the package:

`-> algomax algorithm.py config.json -p params.json -m schedule.json`

## Example
Here is a simple example of using **algomax**

> algorithm.py

```
import os
import sys
import json
import math
from order import Order
import utils


def run_algorithm():
    config = utils.get_settings()
    trader_order = Order(config['broker_url'])

    params = utils.get_params()

    # algorithm
    data = fibonacci_algorithm(params['data'])

    # trade
    trader_order.create(data)


def isPerfectSquare(number: int): 
    squrare_number = int(math.sqrt(number)) 
    return squrare_number * squrare_number == number 
  

def isFibonacci(number): 
    return isPerfectSquare(5 * number * number + 4) or isPerfectSquare(5 * number * number - 4) 


def fibonacci_algorithm(data: dict):
    qunatity = data['quantity']
    if isFibonacci(qunatity):
        qunatity += 3
    else:
        qunatity -= 3
    
    data['quantity'] = qunatity
    return data

if __name__ == '__main__':

    run_algorithm()
```

> config.json


```
{
    "broker_url": "http://your-broker.server",
    "access_token": "YoUr-ToKeN",
    "account_id": "your-account-id"
}
```

> params.json (your algorithm data)


```
{
    "data": {
        "agent_id": "2",
        "side_id": "1",
        "instrument_id": "instrument-id",
        "price": 1234.0,
        "quantity": 1934,
        "validity_type_id": "1",
        "validity_date": ""
    }
}
```

> mode.json (scheduling)


```
{
    "mode": "interval",
    "schedule": {
        "start_date": "2019-09-22",
        "end_date": "2019-10-23",
        "minutes_interval": 1,
        "start_time": "8:30",
        "end_time": "13:00"
    }
}
```

**Caution**: utils.py, order.py -> use **algomax-engine** package, but it's not ready yet ;)