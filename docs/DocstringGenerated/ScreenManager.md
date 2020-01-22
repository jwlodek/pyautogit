# File containing class that acts as a parent class to all sub-screen manager


# ScreenManager 

``` python 
 class ScreenManager 
```

Main parent screen manager class.

Contains common functionality for showing command results, handling credentials, commands, and long operations.

| Attributes    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|     manager | PyAutogitManager |         Driver engine manager | 
|     message | str |         A variable to store messages accross functions | 
|     status | int |         A variable to store status codes accross functions | 
|     utility_var | obj |         A variable that can be used to store any data across functions | 
|     menu_choices | list of str |         Overriden by children, list of options that pop up in menu | 
|     info_panel | py_cui.widgets.TextBlock |         The main textblock on the screen, used to display status information. | 


--------- 

## Methods 

 
| method    | Doc             |
|:-------|:----------------|
| initialize_screen_elements | Function that must be overridden by subscreen. Creates py_cui_widgets, returns widget set object. | 
| process_menu_selection | Processes based on selection returned from the men. | 
| show_menu | Opens the menu using the menu item list for screen manager instanc. | 
| show_command_result | Function that displays the result of stdout/err for an external command. | 
| show_status_long_op | Shows the status of a long(async) operation on success completio. | 
| refresh_status | Function that is fired after each git operation. Implement in subclasses. | 
| clear_elements | Function that clears entries from widgets for reus. | 
| set_initial_values | Function that sets initial values for widgets in scree. | 
| handle_user_command | Handles custom user command. | 
| ask_custom_command | Function that prompts user to enter custom comman. | 
| execute_long_operation | Wrapper function that allows for executing long operations w/ credential requirements. | 
 
 

### initialize_screen_elements

``` python 
    initialize_screen_elements() 
```


Function that must be overridden by subscreen. Creates py_cui_widgets, returns widget set object.

### process_menu_selection

``` python 
    process_menu_selection(selection) 
```


Processes based on selection returned from the men.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         selection | str |             An element of the self.menu_choices list selected by user | 


### show_menu

``` python 
    show_menu() 
```


Opens the menu using the menu item list for screen manager instanc.

### show_command_result

``` python 
    show_command_result(out, err, show_on_success = True, command_name='Command', success_message='Success', error_message='Error') 
```


Function that displays the result of stdout/err for an external command.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         out | str |             stdout string from command | 
|         err | str |             stderr string from command | 
|         show_on_success | bool |             Set to false to show no messages on success. (ex. git log doesnt need success message) | 
|         command_name | str |             name of command run. | 
|         success_message | str |             message to show on successful completion | 
|         error_message | str |             message to show on unsuccessful completion | 


### show_status_long_op

``` python 
    show_status_long_op(name='Command', succ_message="Success", err_message = "Error") 
```


Shows the status of a long(async) operation on success completio.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         name | str |             name of command run. | 
|         succ_message | str |             message to show on successful completion | 
|         err_message | str |             message to show on unsuccessful completion | 


### refresh_status

``` python 
    refresh_status() 
```


Function that is fired after each git operation. Implement in subclasses.

### clear_elements

``` python 
    clear_elements() 
```


Function that clears entries from widgets for reus.

### set_initial_values

``` python 
    set_initial_values() 
```


Function that sets initial values for widgets in scree.

### handle_user_command

``` python 
    handle_user_command(command) 
```


Handles custom user command.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         command | str |             The string command entered by the user | 


### ask_custom_command

``` python 
    ask_custom_command() 
```


Function that prompts user to enter custom comman.

### execute_long_operation

``` python 
    execute_long_operation(loading_messge, long_op_function, credentials_required=False) 
```


Wrapper function that allows for executing long operations w/ credential requirements.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         loading_message | str |             Message displayed while async op is performed | 
|         long_op_function | no-arg or lambda function |             Function that is fired in an async second thread | 
|         credentials_required | bool |             If true, prompts to enter credentials before starting async op | 
