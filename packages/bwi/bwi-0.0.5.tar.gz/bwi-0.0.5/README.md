# BWI-lib

_python client for BWI interactions_

## Usage

### Instantiate a client

```python
import bwi


client = bwi.Client(api_key='xxxxxxxxxxxxxxxx', workflow='shop')
```

### Manipulate your logs

```python
# provide step duration
with client.Step('fetch client information') as bwi:
    bwi.logger.info('found client with user id %d', 18)

```

### Metric management

```python
# manipulate metrics
client.Step('validate order')
# Your business-oriented code goes here
# ...
total_paid = 220

# increment the income metric for this step
bwi.metrics.inc('income', total_paid)
```

### Error-handling

```python
# report any unknown exception to the bwi handler
try:
    # Your business-oriented code goes here
except Exception as err:
    bwi.handler.catch(err)
    # the error is now available for this specific step
```

### Mark a step as (un)succesful

```python
step = bwi.Step('process order')

# Your business-oriented code goes here
step.success()

# other scenario, where thing go bad
step.failed()
```
