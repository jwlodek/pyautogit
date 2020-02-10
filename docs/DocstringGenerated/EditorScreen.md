# Pyautogit internal editor, based on snano example from py_cu


# EditorScreenManager 

``` python 
 class EditorScreenManager(pyautogit.screen_manager.ScreenManager) 
```

Class representing internal editor screen for pyautogi.

| Attributes    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|     opened_path | str |         The current opened path for the editor | 


--------- 

## Methods 

 
| method    | Doc             |
|:-------|:----------------|
| initialize_screen_elements | Override of base class. Initializes editor widgets and widget se. | 
| set_initial_values | Function that sets status bar tex. | 
| clear_elements | Function for clearing widgets in editor scree. | 
| open_new_directory_external | Opens a new directory given an external targe. | 
| open_new_directory | Function that opens a new director. | 
| add_new_file | Function for creating a new fil. | 
| open_file_dir | Function that opens a file/directory from men. | 
| save_opened_file | Function that saves the opened fil. | 
| delete_selected_file | Function that deletes the selected fil. | 
 
 

### initialize_screen_elements

``` python 
    initialize_screen_elements() 
```


Override of base class. Initializes editor widgets and widget se.

| Returns    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         pyautogit_editor_widget_set | py_cui.widget_set.WidgetSet |             Widget set for internal editor screen | 


### set_initial_values

``` python 
    set_initial_values() 
```


Function that sets status bar tex.

### clear_elements

``` python 
    clear_elements() 
```


Function for clearing widgets in editor scree.

### open_new_directory_external

``` python 
    open_new_directory_external(new_dir_path) 
```


Opens a new directory given an external targe.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         new_dir_path | str |             Path of directory to open | 


### open_new_directory

``` python 
    open_new_directory() 
```


Function that opens a new director.

### add_new_file

``` python 
    add_new_file() 
```


Function for creating a new fil.

### open_file_dir

``` python 
    open_file_dir() 
```


Function that opens a file/directory from men.

### save_opened_file

``` python 
    save_opened_file() 
```


Function that saves the opened fil.

### delete_selected_file

``` python 
    delete_selected_file() 
```


Function that deletes the selected fil.