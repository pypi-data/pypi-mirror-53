# Mobikit Utilities

## Overview

This library contains a variety of mobikit python utilities. To install:

```py
pip3 install -e .
```

To check your install:

```sh
mkutils --version
```

To import programmatically:

```py
import mobikit_utils as mku
```

## Public Distribution

Currently, the query_builder portion of the mobikit utils library is approved for public distribution. In order to release a new version of the library, follow the steps below:

1. Make sure you have the credentials for Mobikit's PyPl account available. you will need these in order to publish.

2. Bump the library version appropriately in `setup_base.py`.

3. Bundle the library for distribution:
   `rm -rf dist && rm -rf build && python setup_public.py sdist bdist_wheel`

4. Distribute the library to PyPl: (you will be asked to provide Mobikit's PyPl credentials here)

test index: `pip install --upgrade twine && twine upload --repository-url https://test.pypi.org/legacy/ dist/*`
production index: `pip install --upgrade twine && twine upload dist/*`

5. Install your newly distributed `mobikit-utils`:
   install from test index: `pip install --index-url https://test.pypi.org/simple/ --no-deps mobikit-utils`
   install from production index: `pip install mobikit-utils`

## Integration

To integrate into a docker image within snake-pit, add the following to the `Dockerfile`:

```Dockerfile
# Install mobikit-utils
ADD ./mobikit-utils /usr/src/mobikit/mobikit-utils
RUN pip install -e /usr/src/mobikit/mobikit-utils
```

If integrating with another local module, install mobikit-utils in the environemnt, add to its `setup.py`, and package with any docker images depending on the module. For example, if `my_module` depends on mobikit-utils, and `my_container` required `my_module`, then the dockerfile would include something like the following:

```Dockerfile
# Install mobikit-utils (needs to be before `my_module` is installed!)
ADD ./mobikit-utils /usr/src/mobikit/mobikit-utils
RUN pip install -e /usr/src/mobikit/mobikit-utils

# Install my_module
...
```

And the `setup.py`:

```py
setup(
    ...
    install_requires=[
        "mobikit-utils==0.1.0",
        ...
    ],
)
```

## Testing

To run tests locally:

```sh
# Decrypt secrets
mkdir ./env
gcloud kms decrypt \
    --ciphertext-file=./enc/.mobikit_utils_env.enc \
    --plaintext-file=./env/.mobikit_utils_env \
    --location=global \
    --keyring=mobikit \
    --key=mobikit-utils-symmetric


# Bash into container
docker-compose -f docker-compose.test.yaml \
    run --rm mobikit-utils bash

# Execute tests
py.test -vv -x
```
