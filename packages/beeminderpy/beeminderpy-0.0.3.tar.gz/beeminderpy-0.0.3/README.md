# beeminderpy

Python async wrapper for the [Beeminder REST API](http://api.beeminder.com/#beeminder-api-reference)

## Installation

        $ pip install beeminderpy

## Usage

### Client

```python
async def run(args):
    beeminder = BeeminderClient(args.username, args.token)
    req_id = str(hash(args.comment))
    if args.datapoint:
        await beeminder.create_datapoint(args.goal, args.datapoint, comment=args.comment, requestid=req_id)
    await beeminder.close()
```

### CLI

        $ beeminderpy --username MYUSERNAME --token XYZ --goal coding --datapoint 1 --comment test
