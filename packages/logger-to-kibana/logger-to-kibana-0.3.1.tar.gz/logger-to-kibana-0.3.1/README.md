# logger-to-kibana

[![Build Status](https://dev.azure.com/ismaelmartinez0550/logger-to-kibana/_apis/build/status/IsmaelMartinez.logger-to-kibana?branchName=master)](https://dev.azure.com/ismaelmartinez0550/logger-to-kibana/_build/latest?definitionId=5&branchName=master)

---

This project is inteded to generate view from the log messages encountered.

The python executable can be found in [https://pypi.org/project/logger-to-kibana/](https://pypi.org/project/logger-to-kibana/)

You will need to install the dependences by running

```bash
pip install -r requirements.txt
```

To get the programs help just type:

```bash
python main.py
```

This returns:

```bash
  Usage: main.py [OPTIONS] COMMAND [ARGS]...

  Process the file provided according to conditions

Options:
  --help  Show this message and exit.

Commands:
  pommands:
  process                    Process the folder
  process_and_generate       Process the folder and generate visualization
  process_generate_and_send  Process the folder, generate visualization and
                             send
```

## Default settings

The default settings can be found in the [settings.ini](settings.ini) file. You can provide a different settings
file by specifying it as an environment variable LOGGER_TO_KIBANA_CONFIG

## commands

The current available commands are:

### process

Process a folder and prints out the processed functions/logs in the following format:

```bash
[{'type': '<log_type>', 'query': 'message: "<log_filter>"', 'label': '<log_type>: <log_filter>'}]
```

To execute the command run:

```bash
python main.py process -f <folder_location>
```

Check the table under [How does it work] section to get more info about log_type and log_filter.

### process_and_generate

Process a folder (as shown in the process section) and generates a table visualization for kibana.

To execute the command run:

```bash
python main.py process_and_generate -f <folder_location>
```

### process_generate_and_send

Process a folder, generates a table visualization for kibana and send it to kibana (currently in localhost:5601)

To execute the command run:

```bash
python main.py process_and_generate -f <folder_location>
```

### How does it work

By default, it scans for files under the folder specified and with the  pattern `app/src/**/*.py`. You can specify another patter in the FilesMatchFilter in the [settings.ini](settings.ini)

This program uses different regex `detectors` to filter logs and files to process.

Those can be changed in the [settings.ini](settings.ini) file.

The current available detectors are:

| Detector | Default Value | Propose |
|---|---|---|
| FilesMatchFilter | app/src/**/*.py | Filter the files to process in the provided folder |
| FunctionMappingDetector | def | Detect a function |
| FunctionMappingFilter | (?<=def ).*?(?=\() | Filter the function name |
| LogDebugDetector | LOG.debug | Detect the log debug message |
| LogDebugFilter | (?<=LOG.debug\(["\']).*?(?=["\']) | Filter the log debug message |
| LogInfoDetector | LOG.info | Detect the log info message |
| LogInfoFilter | (?<=LOG.info\(["\']).*?(?=["\']) | Filter the log info message |
| LogWarnDetector | LOG.warn | Detect the log warn message |
| LogWarnFilter | (?<=LOG.warn\(["\']).*?(?=["\']) | Filter the log warn message |
| LogErrorDetector | LOG.error | Detect the log error message |
| LogErrorFilter | (?<=LOG.error\(["\']).*?(?=["\']) | Filter the log error message |
| LogCriticalDetector | LOG.critical | Detect the log critical message |
| LogCriticalFilter | (?<=LOG.critical\(["\']).*?(?=["\']) | Filter the log critical message |
| LogExceptionDetector | LOG.exception | Detect the log exception message |
| LogExceptionFilter | (?<=LOG.exception\(["\']).*?(?=["\']) | Filter the log exception message |

Other configuration available in the settings.ini file are:
| Type | Value | Propose |
| -- | -- | -- |
| BaseUrl | [http://localhost:5601](http://localhost:5601) | Kibana base url |
| Index | 59676040-e7fd-11e9-9209-1f165c3af176 | Kibana index |

## The process

The commands for the application are done in the following logical order.

```bash
    process -> generate -> send
```

As an example, when processing a file in `tests/unit/resources/example.py` with the content:

```python
def lambda_handler(_event: dict, _context):
    LOG.debug('Initialising')
    LOG.info('Processing')
    LOG.warn('Success')
    LOG.error('Failure')
    LOG.critical('Bananas')
    LOG.exception('Exception')
)
```

Will return the next object:

```python
[{'filename': 'tests/unit/resources/example.py', 'function': 'lambda_handler',
'type': 'debug', 'query': 'message: "Initialising"', 'label': 'debug: Initialising'},
{'filename': 'tests/unit/resources/example.py', 'function': 'lambda_handler',
'type': 'info', 'query': 'message: "Processing"', 'label': 'info: Processing'},
{'filename': 'tests/unit/resources/example.py', 'function': 'lambda_handler',
'type': 'warn', 'query': 'message: "Success"', 'label': 'warn: Success'},
{'filename': 'tests/unit/resources/example.py', 'function': 'lambda_handler',
'type': 'error', 'query': 'message: "Failure"', 'label': 'error: Failure'},
{'filename': 'tests/unit/resources/example.py', 'function': 'lambda_handler',
'type': 'critical', 'query': 'message: "Bananas"', 'label': 'critical: Bananas'},
{'filename': 'tests/unit/resources/example.py', 'function': 'lambda_handler',
'type': 'exception', 'query': 'message: "Exception"', 'label': 'exception: Exception'}]
```

Generate, will generate a table visualization with filters for all the logs that have found.

The choise of having a table visualization is for the amount of information available. It is, basically, a good place to start as later we can split the visualizations by file, function or whatever we choose to do so.

You can change the type of visualization generated by modifying the VisualizationType in the [settings.ini](settings.ini). The current available values are metric or table. The default value is table.

To finish, it sends the generated visualization to Kibana with the following name format:

[Generated - <folder_name> ]

## Limitations

Currently, this project does not separate logs per file or function [see #25 as this is in process](#25). For that reason, it was choosen to use the table visualization as it is easy to generate too many filter for the other types of visualizations.

It only generates the visualizations and not the dashboards.
