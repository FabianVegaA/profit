# Profit model


## Running Tests

To run the tests, you can use the `uv` command line tool. The following command will run the tests using the `python -m unittest` command.

```bash
$ uv run python -m unittest
```

If you don't have `uv` installed, you can use the `docker` command line tool to run the tests. The following command will run the tests using the `python -m unittest` command.

```bash
$ docker build -t profit-model .
$ docker run profit-model python -m unittest
```
