"""
The file_processor is in charge of processing the files
looking for the log_mappings to generate an object with
the function, log_message and level
"""

import re
import configparser
import glob

config = configparser.ConfigParser()
config.read("settings.ini")

files_match = config.get('file_parsers', 'FilesMatchFilter')
log_debug_detector = config.get('file_parsers', 'LogDebugDetector')
log_debug_filter = config.get('file_parsers', 'LogDebugFilter')
log_info_detector = config.get('file_parsers', 'LogInfoDetector')
log_info_filter = config.get('file_parsers', 'LogInfoFilter')
log_warn_detector = config.get('file_parsers', 'LogWarnDetector')
log_warn_filter = config.get('file_parsers', 'LogWarnFilter')
log_error_detector = config.get('file_parsers', 'LogErrorDetector')
log_error_filter = config.get('file_parsers', 'LogErrorFilter')
log_critical_detector = config.get('file_parsers', 'LogCriticalDetector')
log_critical_filter = config.get('file_parsers', 'LogCriticalFilter')
log_exception_detector = config.get('file_parsers', 'LogExceptionDetector')
log_exception_filter = config.get('file_parsers', 'LogExceptionFilter')

FILE_RESULTS = []

LOG_MAPPING = [
    {
        "type": "debug",
        "detector": log_debug_detector,
        "filter": log_debug_filter,
    },
    {
        "type": "info",
        "detector": log_info_detector,
        "filter": log_info_filter,
    },
    {
        "type": "warn",
        "detector": log_warn_detector,
        "filter": log_warn_filter,
    },
    {
        "type": "error",
        "detector": log_error_detector,
        "filter": log_error_filter,
    },
    {
        "type": "critical",
        "detector": log_critical_detector,
        "filter": log_critical_filter,
    },
    {
        "type": "exception",
        "detector": log_exception_detector,
        "filter": log_exception_filter,
    },
]


def process_folder(folder: str) -> []:
    if not folder:
        folder = ""
    for file in glob.iglob(folder + files_match, recursive=True):
        read_file_for_logs(file)
    return FILE_RESULTS


def read_file_for_logs(filename: str):
    with open(filename) as f:
        for line in f:
            process_line_log_mapping(line)


def process_line_log_mapping(line: str):
    for mapping in LOG_MAPPING:
        if re.findall(mapping["detector"], line):
            message = re.findall(mapping["filter"], line)
            if message:
                FILE_RESULTS.append({
                    "type": mapping["type"],
                    "query": 'message: "' + message[0] + '"',
                    "label": mapping["type"] + ": " + message[0]
                })
                return
