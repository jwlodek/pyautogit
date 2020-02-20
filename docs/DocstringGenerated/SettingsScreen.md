# settings_screen

A subscreen that allows for setting a variety of pyautogit settings.




#### Classes

 Class  | Doc
-----|-----
 SettingsScreen | extends ScreenManager base, adds widgets for controlling pyautogit settings.




## SettingsScreen(pyautogit.screen_manager.ScreenManager)

```python
class SettingsScreen(pyautogit.screen_manager.ScreenManager)
```

Class representing settings subscreen for pyautogit




#### Attributes

 Attribute  | Type  | Doc
-----|----------|-----
 current_info_log  |  str | The current settings log text
 show_settings_log  |  bool | Toggle for showing settings log

#### Methods

 Method  | Doc
-----|-----
 initialize_screen_elements | Override of base class, initializes elements, returns widget set
 ask_log_file_path | Prompts user to enter log file path
 get_settings_ascii_art | Gets an ascii art settings title
 toggle_logging | Function that toggles logging for pyautogit
 update_log_file_path | Function that updates the target log file path
 refresh_status | Override of base class refresh function




### __init__

```python
def __init__(self, top_manager)
```

Constructor for SettingsScreen







### initialize_screen_elements

```python
def initialize_screen_elements(self)
```

Override of base class function. Initializes widgets, and returns widget set




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 settings_widget_set  |  py_cui.widget_set.WidgetSet | Widget set object for rsettings screen





### set_initial_values

```python
def set_initial_values(self)
```

Function that sets initial status bar text for settings window







### add_to_settings_log

```python
def add_to_settings_log(self, text)
```

Function that updates the settings info log panel




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 text  |  str | New log item to write to settings info panel





### fetch_about_file

```python
def fetch_about_file(self, file)
```

Function that grabs file from github and displays it in info panel




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 file  |  str | Filename to fetch from github repository





### revert_settings_log

```python
def revert_settings_log(self)
```

Function that resets to showing settings info







### open_web_docs

```python
def open_web_docs(self)
```

Function tasked with open docs in external browser







### show_tutorial

```python
def show_tutorial(self)
```

Function that demonstrates tutorial for using pyautogit







### ask_log_file_path

```python
def ask_log_file_path(self)
```

Prompts user to enter log file path







### get_settings_ascii_art

```python
def get_settings_ascii_art(self)
```

Gets ascii art settings logo




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 settings_message  |  str | Block letter ascii art settings logo





### toggle_editor_type

```python
def toggle_editor_type(self)
```

Function that toggles between internal and external editor







### toggle_logging

```python
def toggle_logging(self)
```

Function that enables/disables logging







### ask_default_editor

```python
def ask_default_editor(self)
```

Function that asks user for editor, and then refreshes







### update_default_editor

```python
def update_default_editor(self, new_editor)
```

Function that updates the new default editor




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 new_editor  |  str | command used to open external editor





### update_log_file_path

```python
def update_log_file_path(self, new_log_file_path, default_path=False)
```

Function that updates log file path if valid




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 new_log_file_path  |  str | Path to new log file





### refresh_status

```python
def refresh_status(self)
```

Override of base class refresh function.










