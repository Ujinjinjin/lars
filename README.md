# From txt to sqlite3 parser of logs

## Installation

```
$ pip install ulars
```

## Usage

### Parsing

First of all place `lars.yml` (see Examples for more info) file in the directory with your .log file then run `lars parse`  one of the following command:

```shell script
$ lars parse --path PATH_TO_LOG_FILE
$ lars parse --name APP_NAME
$ lars parse --id APP_ID
```

In order to use `--name` or `--id` arguments you have to add applications to `lars`. To get more information about application management see *Application management* part.

### Application management

#### Add

To add application to list, use:

```shell script
$ lars apps add --name APP_NAME --path PATH_TO_LOG_FILE
```

#### List

To list all applications, use:

```shell script
$ lars apps list
```

#### Remove

To remove application from list use

```shell script
$ lars apps remove --id APP_ID
```

## Examples

### lars.yml

```yaml
headers:
  - guid
  - log_date
  - log_level
  - logger_name
  - msg
primary_key: "guid"
table_name: "logs"
separator: " | "
encoding: "utf8"
db_filename: "logs.sqlite3"
```

### .log

```text
9951e948f4a64c859a8589ae111a1eea | 2019-12-05 21:10:06.2561727Z | Debug | Code.Engines.Player.PlayerInputToActionEngine | Found 0 entities with <PlayerInputEntityViewStruct, ActionEntityStruct>
c52029ca8e694c98845a417688c4f0c3 | 2019-12-05 21:10:06.4945353Z | Debug | Code.Engines.Common.MovementEngine | Found 0 entities with <ActionEntityStruct>
1e4c0ba2ebcb486499bfa06f592e3b3d | 2019-12-05 21:10:06.4945353Z | Debug | Code.Engines.Common.MovementEngine | Found 0 entities with <ActionEntityStruct>
e7515daf01484f5196e7bb1a0b6b3329 | 2019-12-05 21:10:06.4945353Z | Debug | Code.Engines.Common.MovementEngine | Found 0 entities with <ActionEntityStruct>
```

## Development

This project includes a number of helpers in the `Makefile` to streamline common development tasks.

### Environment Setup

The following demonstrates setting up and working with a development environment:

```
### create a virtualenv for development

$ make virtualenv

$ source env/bin/activate


### run lars cli application

$ lars --help


### run pytest / coverage

$ make test
```
