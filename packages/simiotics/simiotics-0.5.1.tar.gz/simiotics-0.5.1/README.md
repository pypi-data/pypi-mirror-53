# Simiotics Python client library

This package contains the Simiotics Python client library. It allows you to interact with Simiotics
APIs directly from your Python programs.

## Registries

This library currently supports interaction with the following types of Simiotics registries:
1. Data registries
2. Function registries

The Simiotics client reads registry-related configuration from environment variables:
1. To connect to a data registry, set the `SIMIOTICS_DATA_REGISTRY` environment variable to point at
a data registry instance (e.g. `export SIMIOTICS_DATA_REGISTRY=registry-alpha.simiotics.com:7010`)
2. To connect to a function registry, set the `SIMIOTICS_FUNCTION_REGISTRY` environment variable to
point at a function registry instance (e.g.
`export SIMIOTICS_FUNCTION_REGISTRY=registry-alpha.simiotics.com:7011`)


To communicate with a registry, you must first instantiate a registry client:
```
import simiotics.client

simiotics = simiotics.client.client_from_env()
```

If you specified `SIMIOTICS_DATA_REGISTRY` in your environment, you can access that registry using
`simiotics.data_registry`.

If you specified `SIMIOTICS_FUNCTION_REGISTRY` in your environment, you can access that registry
using `simiotics.function_registry`.

The [`simiotics_s3`](https://github.com/simiotics/simiotics-s3) tool provides a good example of how
to use these registries. For example, the
[`list_data_sources`](https://github.com/simiotics/simiotics-s3/blob/master/simiotics_s3/sources.py)
function shows how to list all the sources registered against a data registry.

`simiotics_s3` is a very convenient wrapper around the `simiotics` client library and we will likely
merge it into the client library proper in an upcoming version.
