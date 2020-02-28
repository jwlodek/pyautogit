# logger

Module containing logging classes and functions.



The logger is controlled via a set of global variables set by the pyautogit client.

#### Functions

 Function  | Doc
-----|-----
 toggle_logging | Function for opening/closing log file as required.
 set_log_file_path | Sets the path to the log file
 initialize_logger | Function for initializing log-file writing in addition to stdout output
 close_logger | Function that closes the opened logfile
 write | Main logging funcion. Called if write function was set




### toggle_logging

```python
def toggle_logging()
```

Function for opening/closing log file as required.







### set_log_file_path

```python
def set_log_file_path(log_file_path)
```

Sets the path to the log file




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 log_file_path  |  str | Path to the log file





### initialize_logger

```python
def initialize_logger()
```

Function for initializing log-file writing in addition to stdout output




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 initialized  |  bool | True if log file opened, false otherwise





### close_logger

```python
def close_logger()
```

Function that closes the opened logfile







### write

```python
def write(text, no_timestamp=False)
```

Main logging funcion. Called if write function was set




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 text  |  str | debug text to print
 no_timestamp=False  |  bool | a flag to disable timestamp printing when required





