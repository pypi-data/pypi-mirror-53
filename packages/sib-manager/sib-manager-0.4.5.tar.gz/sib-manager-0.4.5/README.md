# Startin'Blox Manager

## Requirements

You will need both Python3 and Pip3 installed. You can follow [this article](https://realpython.com/installing-python/) if you don't konw where to start.

Before diving in Startin' Blox manager, just make sure you got the last version of `pip` by upgrading it:
```
sudo pip3 install --upgrade pip
```

Then install the `sib` command line:
```
$ pip3 install --user -U sib-manager
```

Note:

 * This install the `sib` program in the user context. `sib` doesn't need system priveleges
 * In some distribution the system can't find the user programs. In that case you have to add it manually, for example, by adding `export PATH=$HOME/.local/bin:$PATH` in your `~/.bashrc`.

## Get started with a new project

`sib` supports installation inside `venv`

Create a new project:
```
$ sib startproject myproject
$ cd myproject
```

Note:

 * The project name must be a valid python package name (no dashes).

Configure the modules you want to use in `packages.yml`:
```
ldppackages:
  djangoldp_project: djangoldp_project
  oidc_provider:     django-oidc-provider
```

Run the installation:
```
$ sib install myproject
```

And launch it locally !
```
$ python3 manage.py runserver
```

The administration interface is available at `http://localhost:8000/admin/` with default `admin` user and password.

## Usage

```
$ sib --help
Usage: sib [OPTIONS] COMMAND [ARGS]...

  Startin'Blox installer
```

`sib` manager can be used to deploy local development and production instances. Whereas a development instance relies on testing components as a `sqlite` database and comes with default configuration, a production instance needs more parameters to configure the `postgresql` database.

## Contribute

Get the last unreleased version of the project:
```
$ pip3 install --user -U git+https://git.happy-dev.fr/startinblox/devops/sib
```

## Test strategy

To test:

 * create superuser twice
 * add a package after install and update
 * install without packages

Unit testing:
```
# docker run --rm -v $PWD:/code -w /code -it happydev1/sib:3.6 bash
# pip install --user -e .[dev]
# pytest tests/unit
```

Integration testing with postgres:
```
# docker network create sib
# docker run --rm --network sib --name postgres -e POSTGRES_DB=sib -e POSTGRES_USER=sib -e POSTGRES_PASSWORD=test -d postgres
# docker run --rm --network sib -p 127.0.0.1:80:8000 -v $PWD:/code -it happydev1/sib:3.6 bash
# pip install --user -e .[dev]
# bash tests/integration/run_test.sh
```

