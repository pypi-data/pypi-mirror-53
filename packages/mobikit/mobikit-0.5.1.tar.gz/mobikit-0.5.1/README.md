# Mobikit Data Science Library

## Setup

To install the Mobikit data science module locally:

```
pip3 install -e .
```

## Overview

See `/documentation` for more information on how to use the library and its methods.

## Public Distribution

Currently, the feeds portion of the data science library is approved for public distribution. In order to release a new version of the library, follow the steps below:

1. Make sure you have the credentials for Mobikit's PyPl account available. you will need these in order to publish.

2. Bump the library version appropriately in `setup_base.py`.

3. Bundle the library for distribution:
   `rm -rf dist && rm -rf build && python setup_public.py sdist bdist_wheel`

4. Distribute the library to PyPl: (you will be asked to provide Mobikit's PyPl credentials here)
   test index: `pip install --upgrade twine && twine upload --repository-url https://test.pypi.org/legacy/ dist/*`
   production index: `pip install --upgrade twine && twine upload dist/*`

5. Install your newly distributed `mobikit` library:
   install from test index: `pip install --index-url https://test.pypi.org/simple/ --no-deps mobikit`
   install from production index: `pip install mobikit`

## e2e testing

To setup for e2e testing, start by decrypting the staging environment file found in `data-science/enc` and exporting the decrypted variables to your environment:

```sh
gcloud kms decrypt \
    --ciphertext-file=./enc/.staging_env.test.enc \
    --plaintext-file=./env/.staging_env.test \
    --location=global \
    --keyring=mobikit \
    --key=data-science-e2e
```

You can run tests with

```sh
$ docker-compose up
```

If you prefer to run locally rather than inside a Docker container,
first load the decrypted environment variables:

```sh
export $(cat ./env/.staging_env.test | xargs)
```

You can now run any of the premade e2e test scripts located in `data-science/e2e/test`.

In addition, you can use the environment variables to write and execute your own e2e tests.

```python
api_token = os.getenv("MOBIKIT_TEST_TOKEN")
schema = os.getenv("MOBIKIT_TEST_SCHEMA")
feed_id = int(os.getenv("MOBIKIT_TEST_FEED"))
```
