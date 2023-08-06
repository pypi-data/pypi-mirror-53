# ClickHouse query tools
Exposes ClickHouse internals to parse and manipulate ClickHouse queries.

## Install pre-built packages
You can install a pre-compiled package for your platform, e.g.:
```
pip install dist/clickhouse_toolset-0.2dev-cp37-cp37m-linux_x86_64.whl
```

## Development

First, you need to clone the repo and its submodules.

```
git clone --recursive git@gitlab.com:tinybird/clickhouse-toolset.git
```

Then, you will compile the dependencies and the module itself. For this task you need to have gcc/g++ 8.

```
pip install --editable .
```

### Generate pre-built packages
You have to install the `wheel` dependency: `pip install .[build]`, then, you can generate pre-compiled binaries for your platform using:
```
python setup.py sdist bdist_wheel
python setup.py sdist
gsutil cp dist/clickhouse_toolset-0.2.dev0-cp36-cp36m-linux_x86_64.whl gs://tinybird-bdist_wheels
twine upload --repository-url https://test.pypi.org/legacy/ dist/clickhouse-toolset-0.2dev0.tar.gz
twine upload dist/clickhouse-toolset-0.2.dev0.tar.gz
```

## Examples

Check tests directory.
