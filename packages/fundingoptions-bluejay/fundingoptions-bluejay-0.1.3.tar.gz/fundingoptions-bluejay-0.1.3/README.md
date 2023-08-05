# BlueJay Client

This is a thin client library for sending events to the BlueJay service.

## Backends

### SNS

BlueJay can currently receive events using AWS SNS.

You must provide access to Publish SNS requests. An example policy is:

```tf
data "aws_iam_policy_document" "bluejay-events" {
    statement {
        actions = [
            "sns:Publish",
        ]
        resources = [
            "arn:aws:sns:<region>:<account ID>:<topic name>"
        ]
    }
}
```

### Logging

We provide a Logging backend, for use in development.

Python `logging` is used, with a name of `bluejay.backend.logging`, and will output at the
`INFO` level to stdout by default.
You can configure the logging in 2 ways:

- Changing your central logging config
- Providing a custom Logging class


## Usage

```py
import bluejay
## SNS

topic_arn = ''
backend = bluejay.backend.SNSBackend.build(topic_arn=topic_arn)
### OR
backend = bluejay.backend.SNSBackend(client=boto3.client('sns'), topic_arn=topic_arn)

## Logging

backend = bluejay.backend.LoggingBackend()
### OR
backend = bleujay.backend.LoggingBackend(logger=logging.getLogger())

# Client
client = bluejay.Client(backend=backend)

client.send(bluejay.event.AppReceived(
    app_id='1234-45676',
    occurred_on=datetime.datetime.now(),
))
```

## Events

Events are described in `bluejay.events`, as well as in the `/schemas` directory in the BlueJay Receiver repo.

The code uses `attrs` for constructing objects, so everything you need to know (attributes, types) is very clear.

## Sending Raw data

Don't like using our Event objects? You can send the data in
a raw form if you so wish.

```py
client.send_raw(event_name="custom-event", message={
    "app_id": "1234-1234",
    "occurred_on": datetime.datetime.now(),
})
```

## Using the Backend directly

Not expecting this to be an actual usecase, but it's useful to know.

The backend receives a "command" object, `bluejay.backend.command.SendEvent`.
In reality, you can send any object in, for instance, this will work:

```py
class Event:
    pass
e = Event()
e.payload = {'app_id': '1234-1234', 'occurred_on': dt}
e.event_name = 'application_received'
backend.send(e)
```

The backend is responsible for taking an event (made of an event name, and a payload), encoding it, and sending it to wherever.

In our case, we JSON encode the payload, including transforming datetime objects to RFC3339 compliant date strings.

## Testing

Pytest is used as the testing framework, and tests are structured to loosely define the behaviour of what each component does.

Coverage reports are generated in an effort to identify untested code.
Remember that your tests are **not** complete until all your expected behaviours are covered.

In CI, `tox` is used to ensure we work across Python 3.5-3.7.

In development, you can run `make test`, which is the equivilant of running `python -m pytest`

## Linting

4 linting tools are used in this project:

- `black`, for the unforgiving formatting capabilities.
  If you wish to disobey it, make sure you document why in each case.
- `autoflake`, dead import/code removal
- `isort`, Order is key
- `mypy`, To make sure our components can interact with each other, and to aid IDEs and Mypy users with the development flows. Tests are not currently covered.

The bulk of the linting can be adhered to by running `make autofix`.

You can lint your code by running `make lint`.

## Publishing

We use [flit][flit] for publishing to the PyPI.

By default, we publish to the test PyPI. This is to prevent accidental publishing.

You need to configure your `~/.pypirc` file. An example is:

```ini
[distutils]
index-servers =
   pypi
   testpypi

[pypi]
repository = https://upload.pypi.org/legacy/

[testpypi]
repository = https://test.pypi.org/legacy/
```

To do an actual publish, run `PYPI_INDEX_NAME=pypi make publish`.
This will guide you through the process.


[flit]: https://flit.readthedocs.io/
