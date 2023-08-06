# btrdb-admin-python

This repo contains a quick and dirty Python3 implementation of the BTRDB administrative API.

**Note: At the moment only the ACL and Core API calls are available**

**Note: due to the quick/informal nature of this codebase, the tests ONLY include integration tests that expect to connect to a REAL btrdb server.  A dotenv file or ENV config is required to run the tests**

## Usage

Install the API bindings with `pip` (using Python 3.6 or later):

    $ pip install btrdb-admin

Then, obtain a connection to the database using a valid username and password that is able to use the admin API.  Then you can execute admin methods directly off of the object.

    from btrdb_admin import connect

    db = connect("brtrdb.example.net:4411", username="marmaduke", password="usiB6iUsRLyn")
    users = db.get_all_users()

## JupyterHub Integration

The `btrdb_admin` library provides support for JupyterHub authentication using the BTrDB IDP. To use with JupyterHub, simply `pip install -U btrdb-admin` then in your `jupyterhub_config.py` add the following line:

    c.JupyterHub.authenticator_class = 'btrdb'

Note that you should see a comment above the default position of this configuration that `btrdb` is one of the installed authenticators for use.

## Development Notes

### Protocol Buffers

To build the protocol buffers, first update `btrdb_admin/grpcinterface/admin.proto` with the latest version of the protocol buffers from [github.com/PingThingsIO/smartgridstore](https://github.com/PingThingsIO/smartgridstore/blob/v5/tools/adminapi/pb/admin.proto). You can then use the convience function:

    $ make grpc

To build the protocol buffers. Note that this command has a `sed` statement that is intended to replace the import statement with the correct one in `btrdb_admin/grpcinterface/admin_pb2_grpc.py`. Ensure that:

```python
import admin_pb2 as admin__pb2
```

is replaced with:

```python
import btrdb_admin.grpcinterface.admin_pb2 as admin__pb2
```

To build the protocol buffers manually, use the following command:

    $ PBPKG=btrdb_admin/grpcinterface python -m grpc_tools.protoc -I $PBPKG \
        --python_out=$PBPKG --grpc_python_out=$PBPKG $PBPKG/*.proto

### Tests

To run the tests a live PredictiveGrid allocation is required. In the project root directory, create a `.env` file as follows:

    BTRDB_ADMIN_ENDPOINTS="admin.foo.predictivegrid.com:4411"
    BTRDB_ADMIN_USERNAME="admin"
    BTRDB_ADMIN_PASSWORD="my-admin-password"

Note that you may have to wipe your pgenv to ensure this works:

    $ eval $(pgops env --wipe)

This project includes a suite of automated tests based upon [pytest](https://docs.pytest.org/en/latest/).  For your convenience, a `Makefile` has been provided with a target for evaluating the test suite.  Use the following command to run the tests.

    $ make test

Aside from basic unit tests, the test suite is configured to use [pyflakes](https://github.com/PyCQA/pyflakes) for linting and style checking as well as [coverage](https://coverage.readthedocs.io) for measuring test coverage.

Note that the test suite has additional dependencies that must be installed for them to successfully run: `pip install -r tests/requirements.txt`.

### Documentation

The project documentation is written in reStructuredText and is built using Sphinx, which also includes the docstring documentation from the `btrdb-admin` Python package. For your convenience, the `Makefile` includes a target for building the documentation:

    $ make html

This will build the HTML documentation in `docs/build`, which can be viewed using `open docs/build/index.html`. Other formats (PDF, epub, etc) can be built using `docs/Makefile`. The documentation is automatically built when pushed to GitHub and hosted on [Read The Docs](https://btrdb.readthedocs.io/en/latest/).

Note that the documentation also requires Sphinx and other dependencies to successfully build: `pip install -r docs/requirements.txt`.
