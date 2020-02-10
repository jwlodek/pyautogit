# A subscreen that allows for setting a variety of pyautogit settings


# SettingsScreen 

``` python 
 class SettingsScreen(pyautogit.screen_manager.ScreenManager) 
```

Class representing settings subscreen for pyautogi.

--------- 

## Methods 

 
| method    | Doc             |
|:-------|:----------------|
| initialize_screen_elements | Override of base class function. Initializes widgets, and returns widget se. | 
| set_initial_values | Function that sets initial status bar text for settings windo. | 
| add_to_settings_log | Function that updates the settings info log pane. | 
| fetch_about_file | Function that grabs readme file and displays i. | 
| revert_settings_log | Function that resets to showing settings inf. | 
| open_web_docs | Function tasked with open docs in external browse. | 
| show_tutorial | Function that demonstrates tutorial for using pyautogi. | 
| ask_log_file_path | Prompts user to enter log file pat. | 
| get_settings_ascii_art | Gets ascii art settings log. | 
| toggle_editor_type | Function that toggles between internal and external edito. | 
| toggle_logging | Function that enables/disables loggin. | 
| ask_default_editor | Function that asks user for editor, and then refreshe. | 
| update_default_editor | Function that updates the new default edito. | 
| update_log_file_path | Function that updates log file path if vali. | 
| refresh_status | Override of base class refresh function. | 
 
 

### initialize_screen_elements

``` python 
    initialize_screen_elements() 
```


Override of base class function. Initializes widgets, and returns widget se.

| Returns    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         settings_widget_set | py_cui.widget_set.WidgetSet |             Widget set object for rsettings screen | 


### set_initial_values

``` python 
    set_initial_values() 
```


Function that sets initial status bar text for settings windo.

### add_to_settings_log

``` python 
    add_to_settings_log(text) 
```


Function that updates the settings info log pane.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         text | str |             New log item to write to settings info panel | 


### fetch_about_file

``` python 
    fetch_about_file(file) 
```


Function that grabs readme file and displays i.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         file | str |             Filename to fetch from github repository | 


### revert_settings_log

``` python 
    revert_settings_log() 
```


Function that resets to showing settings inf.

### open_web_docs

``` python 
    open_web_docs() 
```


Function tasked with open docs in external browse.

### show_tutorial

``` python 
    show_tutorial() 
```


Function that demonstrates tutorial for using pyautogi.

### ask_log_file_path

``` python 
    ask_log_file_path() 
```


Prompts user to enter log file pat.

### get_settings_ascii_art

``` python 
    get_settings_ascii_art() 
```


Gets ascii art settings log.

| Returns    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         settings_message | str |             Block letter ascii art settings logo | 


### toggle_editor_type

``` python 
    toggle_editor_type() 
```


Function that toggles between internal and external edito.

### toggle_logging

``` python 
    toggle_logging() 
```


Function that enables/disables loggin.

### ask_default_editor

``` python 
    ask_default_editor() 
```


Function that asks user for editor, and then refreshe.

### update_default_editor

``` python 
    update_default_editor(new_editor) 
```


Function that updates the new default edito.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         new_editor | str |             command used to open external editor | 


### update_log_file_path

``` python 
    update_log_file_path(new_log_file_path, default_path=False) 
```


Function that updates log file path if vali.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         new_log_file_path | str |             Path to new log file | 


### refresh_status

``` python 
    refresh_status() 
```


Override of base class refresh function.