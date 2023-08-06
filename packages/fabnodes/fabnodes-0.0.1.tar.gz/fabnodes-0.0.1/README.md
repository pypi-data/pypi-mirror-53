# fabnodes

`fabnodes` is a Python CLI application that creates prefabricated lambda nodes.
Using these 'node prefabs' one can create complicated distributed processes.


## Requirements

The python requirements are stored in requirements.txt. `fabnodes` currently uses
[`cfndsl`](https://github.com/cfndsl/cfndsl) to generate CloudFormation
JSON files. The instructions to install `cfndsl` is available through the
provided link.

## Basic setup

Install the requirements:
```
$ pip install -r requirements.txt
```

Run the application:
```
$ python -m fabnodes --help
```

To run the tests (todo):
```
    $ pytest
```

## Prefab: Basic Node

The Basic Node (`samples/basic_node/node.py`) will create the most basic node
with the following features:

- `N` SQS inputs, where `N` can be 0 or greater
- `M` SNS outputs, where `M` can be 0 or greater
- 1 Lambda Function that triggers on any input, and can write to any output

Below is a masterpiece that will attempt to illustrate:

```
==========================================================================



                                    |----------- Basic Node ----------|

.. -> SNS(SomeNode.alpha) ----\                          /--> SNS(output) -> ..
                               ---> SQS(input) -> Lambda
.. -> SNS(random topic)    ---/                          \--> (something)



==========================================================================
```

To create this node your `cwd` needs to be the same as `node.py`:

```
fabnodes create node.py --account-arn XXXXXXXXXXXX
```

At the moment the account-arn needs to be passed in because security.

This will make the calls required to CloudFormation that will create the above
infrastructure.

### Use-cases:

The basic node has the following use-cases:

- **The Source Node**: A node that reads from an input source (that isn't
  another prefab node) that then can forward to many through a topic (`0:M`
  node)
- **The Router**: A node that takes an input and can 'farm' it out to
  specifically made workers (other prefab nodes) through named topics (`1:M`
  node)
- **The Worker**: A node that listens on a topic, performs a specific task,
  then creates output (`1:1` node)
- **The Ingest**: A node that listens to many topics, consumes data, and then
  produces output for a non-prefab node (`M:0` node)

### The Sample: node.py

Below is an explanation of the provided sample.

```
@fablib.Distribution('jlh-dev-lambda-functions')
@fablib.Inputs([
    {'name': 'Router', 'source': 'snsRouterTopicId'}])
@fablib.Outputs([
    {'name': 'Alpha'}])
@fablib.Node('BasicNode', 'comRoaetFabnodeSample', 'Basic Node')
def lambda_handler(events, context):
    client = boto3.client('sns')
    sns_target_arn = os.environ['Alpha']
    body_content = json.dumps(events)
    response = client.publish(
        TargetArn=sns_target_arn,
        Message=json.dumps({'default': body_content}),
        MessageStructure='json'
    )
    print(response)
```

- The `lambda_handler` method is defined exactly as a normal lambda handler
- The decorators:
  - `Distribution`: defines the S3 bucket to put the code into
  - `Inputs` (a list of dictionaries): creates an SQS trigger that is subscribed
    to the defined SNS topic
  - `Outputs` (a list of dictionaries): creates an SNS topic that can be
    referenced in the `os.environ` dictionary
  - `Node`: defines the name of the lambda function, the name of the stack, and
    the description of the stack
    - The name of the stack can be used as a reference in other prefabs to
      create the input/output connections

## References

`fabnodes` is a Python CLI application generated from https://github.com/roaet/rorochip-cookies

