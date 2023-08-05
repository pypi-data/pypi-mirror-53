# bSecure Python Client

## Installation

PyPi is the easiest way to install:

``` bash
pip install bsecure-client
```

## Usage

To use the client, you'll first need to create an instance of the
client class:

``` python
from bsecure_client import BSecureClient

client = BSecureClient()
```

Now you may access any of the available APIs on the client. For
example, to integrate with the bSecure server and retrieve a JWT:

``` python
def prepare_endpoint(token):
    # Set the token at the endpoint specified below so as to
    # be retrieved by the integration process.
    pass

client.integrate(
    prepare_endpoint,
    endpoint='/integration/endpoint/',
    host='https://www.myapp.com/',
    secret='my-secret'
)
```

## Available APIs

### Integration

Integration is the process of confirming the identity of a client with
bSecure, and retrieving an access token allowing mutation
operations. In order to begin integration, the domain of the client
and a secret phrase must be registered with bSecure.

To successfully complete integration the caller must be able to set a
token known only to bSecure and the caller as the response to a GET
request against a particular endpoint on the caller's domain.

To integrate with bSecure, use the `integrate` API call:

``` python
def prepare_endpoint(token):
    # Set the token at the endpoint specified below so as to
    # be retrieved by the integration process.
    pass

client.integrate(
    prepare_endpoint,
    endpoint='/integration/endpoint/',
    host='https://www.myapp.com/',
    secret='my-secret'
)
```

The `prepare_endpoint` function is used to perform the necessary
actions to set the secret token against the caller's domain.

The return value from the integration call is a JWT token used to
authenticate your application with bSecure. Please include the token
in your `Authorization` header using the bearer notation, `Bearer
your-jwt-goes-here`.


### Place API

The place API covers mutation operations for creating places, and
tenants, and for uploading documents against places. In bSecure, a
place represents a physical location, whereas a tenant represents a
tenancy within a particular location.

"Pushing" a tenant refers to the action of creating a tenant if it
does not already exist, or identifying an existing tenant that matches
a set of details and returning the unique identifier. To push a tenant
to bSecure use the `push_tenant` API:

``` python
client.push_tenant(
	name="Tenant Name",
	formatted_address="123 Your Formatted Address",
	gcs_coord=(45.123, 45.123),  # longitude, latitude
)
```

The GCS coordinate is used in the disambiguation process: if a place
is found to be outside a 20 meter radius of another identically named
and addressed place, it will be created as a new place.

The return value from the tenant push operation is the unique UUID of
the tenant.

## Architecture

The client is composed of two main parts: the `Client` class and the
`API` class (and its descendants). The architecture is designed to
support extensibility, the single responsibility principle, the
open-closed principle, and also to be easy to read.

The `BSecureClient` class is responsible for the configuration of a
particular bSecure instance, including the domain to which requests
will be made, and the APIs to include. This class is the one users
will instantiate to access bSecure.

The `API` class is responsible for managing a particular grouping of
bSecure's API calls. This helps with encapsulation, and keeps
unrelated code away from one another. When adding to the bSecure API,
a new descendant of the `API` class can be written to accomodate the
new calls.

## Developer Quickstart

### I want to add a new set of APIs

Create a new file in `bsecure_client/api`, let's say
`new_api.py`. Create a new class to encapsulate your the API
interface, something like:

``` python
from .base import API

class NewAPI(API):
    pass
```

To add a method that is to be exposed to the users of the bSecure
client, use the `expose_method` decorator:

``` python
from .base import API

class NewAPI(API):
    @API.expose_method
    def do_something_awesome(self):
        # Access the API using a GraphQL call here.
        pass
```

To add your new API to the default list, alter
`bsecure_client/client.py` to include the module path:
`bsecure_client.apis.new_api`.

### I want to publish a new version

Update the `setup.py` file to have the new version you'd like to
publish. Commit the changes, and then create a new tag within the
repository referencing the version to be published:

``` bash
git tag v0.0.1
git push origin v0.0.1
```

Build a new distribution bundle to be shared:

``` bash
python3 setup.py sdist bdist_wheel
```

Now, upload your new version to PyPi, being sure to replace the
version number with the one you just created:

``` bash
twine upload dist/bsecure*client-0.1.4*
```

### I want to run the tests

TODO
