# microcosm-secretmanager

Secrets storage using AWS SecretsManager

[![Circle CI](https://circleci.com/gh/globality-corp/microcosm-secretmanager/tree/develop.svg?style=svg)](https://circleci.com/gh/globality-corp/microcosm-secretmanager/tree/develop)

## Usage

This project is intended to be used by the python projects based on flask through the graph.

```
# import
from microcosm_secretsmanager.loaders.conventions import load_from_secretsmanager
from microcosm.loaders.compose import load_config_and_secrets

# load
config_loader = load_each(
    load_default_config,
    load_from_json_file,
    load_from_environ,
)
partitioned_loader = load_config_and_secrets(
    config=config_loader,
    secrets=load_from_secretsmanager(),
)

```

Each of the services assumes the role that allows is to access the resources required for loading and parsing the secrets. 

### Local testing (through a service)

If you want to test secrets loading locally, you will need a few things

1. eval botoenv
2. `export MICROCOSM_ENVIRONMENT=dev`
3. `export MICROCOSM_CONFIG_VERSION={current_valid_version}`
4. Run the service

### Local testing (Without a service)

1. eval botoenv
2. `export MICROCOSM_ENVIRONMENT=dev`
3. `export MICROCOSM_CONFIG_VERSION={current_valid_version}`

From python

```
from microcosm.metadata import Metadata
from os import environ

metadata = Metadata("{service_name}")

from microcosm_secretsmanager.loaders.base import SecretsManagerLoader
environment = environ["MICROCOSM_ENVIRONMENT"]
version = environ["MICROCOSM_CONFIG_VERSION"]

loader = SecretsManagerLoader(environment)
loader(metadata, version)

```

## Testing

`nosetests microcosm_secretsmanager`


