[![pipeline status](https://gitlab.com/clearos/clearfoundation/datacustodian/badges/master/pipeline.svg)](https://gitlab.com/clearos/clearfoundation/datacustodian/commits/master) [![coverage report](https://gitlab.com/clearos/clearfoundation/datacustodian/badges/master/coverage.svg)](https://gitlab.com/clearos/clearfoundation/datacustodian/commits/master)

# `DataCustodian` Data Privacy Package Generator

`DataCustodian` generates other repositories for generalized
data privacy and consent systems. The generation follows YML specification files
that define the endpoints, handlers, authentication, validation, etc. for each
component of a data privacy solution.

`DataCustodian` is built to work with decentralized and distributed systems to
provide decentralized trust for storage and consent of data.

Check out the [API Documentation](https://clearos.gitlab.io/clearfoundation/datacustodian) and a [real-world implementation](https://gitlab.com/clearos/clearfoundation/clearshare).

## Installation

The package is available from the PyPI repository:

```bash
pip install datacustodian
```

## Generating a Package

Look at the documentation in `docs/configs` for an example setup that we use for
the unit tests. Customize that to your own application and then run:

```bash
datacustodian_app.py path/to/your/app_spec.yml --generate
```

That will auto-generate the package *and* start the REST API server.

## Running Unit Tests

Running unit tests can prove to be a massive pain because the gitlab CI runner
runs on docker. For a project like this that uses `docker-compose`, we have
to use `docker-in-docker` according to their instructions. However, the
documentation is sparse and there are lots of dead-ends... Here are the steps to
get the `docker-compose.yml` file to work:

1. Install a local `gitlab-runner` using `brew install gitlab-runner`.
2. `gitlab-runner exec docker --docker-privileged test`. Notice that there is a
   `--docker-privileged` argument. Without that, the `docker-in-docker` won't
   work.
3. Make sure all the `multiaddr` reference the `docker` service (which hosts
   all the other containers using `dind`).
4. `tox` should work, but for some reason: running the tests using `tox` produces
   connection refused errors, whereas running straight with `pytest` does not.
   Something about the tox environment screws things up.

## Problems with `coverage`

For an yet-unknown reason, when the unit tests run in the CI server using:

1. Only `pytest`, they pass with no issues.
2. `coverage run` with `pytest`, we get problems with connection reset errors,
   and connection refused errors.

Insead of trying to figure this out now, we just do the following:

1. Before pushing to the remote server, run `coverage` locally (which has no
   problems on MacOS).
2. Generate the `coverage report -m > codecov.out`.
3. Commit `codecov.out` and then push.

The CI server *only* runs `pytest`, but it also `cat codecov.out` so that the
output includes the regular code coverage matrix. That way, `gitlab` still has
correct statistics about code coverage.
