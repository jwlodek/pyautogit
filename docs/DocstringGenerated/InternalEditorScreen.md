# internal_editor_screen

Pyautogit internal editor, based on snano example from py_cui




#### Classes

 Class  | Doc
-----|-----
 EditorScreenManager | Extension of screenManager, manages editor subscreen




## EditorScreenManager(pyautogit.screen_manager.ScreenManager)

```python
class EditorScreenManager(pyautogit.screen_manager.ScreenManager)
```

Class representing internal editor screen for pyautogit




#### Attributes

 Attribute  | Type  | Doc
-----|----------|-----
 opened_path  |  str | The current opened path for the editor

#### Methods

 Method  | Doc
-----|-----
 initialize_screen_elements | Override of base class. Initializes editor widgets and widget set
 set_initial_values | Function that sets status bar text
 clear_elements | Function for clearing widgets in editor screen
 open_new_directory_external | Opens a new directory given an external target
 open_new_directory | Function that opens a new directory
 add_new_file | Function for creating a new file
 open_file_dir | Function that opens a file/directory from menu
 save_opened_file | Function that saves the opened file
 delete_selected_file_dir | Function that deletes the selected file




### __init__

```python
def __init__(self, top_manager, opened_path)
```

Contructor for the EditorScreenManager







### initialize_screen_elements

```python
def initialize_screen_elements(self)
```

Override of base class. Initializes editor widgets and widget set




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 pyautogit_editor_widget_set  |  py_cui.widget_set.WidgetSet | Widget set for internal editor screen





### refresh_status

```python
def refresh_status(self)
```

Function that refreshes the view of the file menu on new dir or file creation







### set_initial_values

```python
def set_initial_values(self)
```

Function that sets status bar text







### clear_elements

```python
def clear_elements(self)
```

Function for clearing widgets in editor screen







### open_new_directory_external

```python
def open_new_directory_external(self, new_dir_path)
```

Opens a new directory given an external target




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 new_dir_path  |  str | Path of directory to open





### open_new_directory

```python
def open_new_directory(self)
```

Function that opens a new directory







### add_new_file

```python
def add_new_file(self)
```

Function for creating a new file







### add_new_directory

```python
def add_new_directory(self)
```

Function for creating a new directory







### open_file_dir

```python
def open_file_dir(self)
```

Function that opens a file/directory from menu







### save_opened_file

```python
def save_opened_file(self)
```

Function that saves the opened file







### delete_selected_file_dir

```python
def delete_selected_file_dir(self)
```

Function that deletes the selected file










