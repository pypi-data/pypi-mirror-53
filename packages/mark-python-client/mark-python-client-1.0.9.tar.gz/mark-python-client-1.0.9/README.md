# mark-python-client

[![pipeline status](https://gitlab.cylab.be/cylab/mark-python-client/badges/master/pipeline.svg)](https://gitlab.cylab.be/cylab/mark-python-client/commits/master)
[![coverage report](https://gitlab.cylab.be/cylab/mark-python-client/badges/master/coverage.svg)](https://gitlab.cylab.be/cylab/mark-python-client/commits/master)
[![PyPI version](https://badge.fury.io/py/mark-python-client.svg)](https://badge.fury.io/py/mark-python-client)

A Python client for the MARK framework:

https://cylab.be/research/mark

## Installation

```bash
$ pip install mark-python-client
```

## Usage

To use the mark_python_client.py script just add it to your python code and you can invoke the different
methods defined in the script

```python
from mark_client import mark_python_client as mark_client

#initialize the MARK Client
client = mark_client.MarkClient()

#set the url of the MARK server
client.set_server_url("http://server.ip.address:ip.port")

#add evidence to the database via the MARK server
client.add_evidence(evidence_to_be_added)

#fetch the ranked list of the k-most suspicious entries
ranked_list = client.get_evidence()

#fetch evidences with a specific label and subject
evidences = client.find_evidence(label, subject)
```

## Contributing

### Installation

```bash
$ git clone https://gitlab.cylab.be/cylab/mark-python-client.git
$ cd mark-python-client
$ pip install -r requirements.txt
```

### Project overview

1. mark_client - source folder of the project

    1.1. mark_python_client.py : main code

    1.2. conftest.py : empty script used by pytest unit test library to point the global PATH variable to the modules and scripts used in the unit tests

2. tests - test folder of the project

   2.1. mark_python_client_test.py : integration test (requires a fully installed mark server)

### Testing

Currently the only implemented test is a complete integration test, which requires a fully running mark server. The recommended way to test the project is thus using gitlab-runner.

1. Install Docker
https://docs.docker.com/install/linux/docker-ce/ubuntu/

2. Install gitlab-runner
https://docs.gitlab.com/runner/

3. Run the tests
```bash
$ gitlab-runner exec docker test:integration
```



