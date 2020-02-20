# screen_manager

File containing class that acts as a parent class to all sub-screen managers



The base screen manager is responsible for defining how CUI elements are assigned to screens,
as well as what the screen must do to refresh its status. Also supports performing long (async)
operations, and running custom commands


#### Classes

 Class  | Doc
-----|-----
 ScreenManager | Main parent screen manager class for all subscreens




## ScreenManager

```python
class ScreenManager
```

Main parent screen manager class.



Contains common functionality for showing command results, handling credentials, commands, and long operations.


#### Attributes

 Attribute  | Type  | Doc
-----|----------|-----
 manager  |  PyAutogitManager | Driver engine manager
 message  |  str | A variable to store messages accross functions
 status  |  int | A variable to store status codes accross functions
 utility_var  |  obj | A variable that can be used to store any data across functions
 menu_choices  |  list of str | Overriden by children, list of options that pop up in menu
 info_panel  |  py_cui.widgets.TextBlock | The main textblock on the screen, used to display status information.

#### Methods

 Method  | Doc
-----|-----
 process_menu_selection | Overriden by child, processes based on menu item selection.
 show_command_result | Displays the result of running a particular command. If more than one line of output, prints to info panel, otherwise, shows popup.
 show_status_long_op | Used instead of show_command_result for long (async) operations
 show_menu | Opens the menu for the screen manager object
 refresh_git_status | Function called after each git operation by children. Must be overriden
 handle_user_command | Processes a custom command from the user
 ask_custom_command | Prompts user to enter a custom command
 execute_long_operation | Wrapper function that should be used as lambda operation. Allows for performing long async operation while loading icon runs




### __init__

```python
def __init__(self, top_manager, screen_type)
```

Constructor for ScreenManager







### initialize_screen_elements

```python
def initialize_screen_elements(self)
```

Function that must be overridden by subscreen. Creates py_cui_widgets, returns widget set object.







### process_menu_selection

```python
def process_menu_selection(self, selection)
```

Processes based on selection returned from the menu




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 selection  |  str | An element of the self.menu_choices list selected by user





### show_menu

```python
def show_menu(self)
```

Opens the menu using the menu item list for screen manager instance







### show_command_result

```python
def show_command_result(self, out, err, show_on_success = True, command_name='Command', success_message='Success', error_message='Error')
```

Function that displays the result of stdout/err for an external command.




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 out  |  str | stdout string from command
 err  |  str | stderr string from command
 show_on_success  |  bool | Set to false to show no messages on success. (ex. git log doesnt need success message)
 command_name  |  str | name of command run.
 success_message  |  str | message to show on successful completion
 error_message  |  str | message to show on unsuccessful completion





### show_status_long_op

```python
def show_status_long_op(self, name='Command', succ_message="Success", err_message = "Error")
```

Shows the status of a long(async) operation on success completion




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 name  |  str | name of command run.
 succ_message  |  str | message to show on successful completion
 err_message  |  str | message to show on unsuccessful completion





### refresh_status

```python
def refresh_status(self)
```

Function that is fired after each git operation. Implement in subclasses.







### clear_elements

```python
def clear_elements(self)
```

Function that clears entries from widgets for reuse







### set_initial_values

```python
def set_initial_values(self)
```

Function that sets initial values for widgets in screen







### handle_user_command

```python
def handle_user_command(self, command)
```

Handles custom user command.




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 command  |  str | The string command entered by the user





### ask_custom_command

```python
def ask_custom_command(self)
```

Function that prompts user to enter custom command







### execute_long_operation

```python
def execute_long_operation(self, loading_messge, long_op_function, credentials_required=False)
```

Wrapper function that allows for executing long operations w/ credential requirements.




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 loading_message  |  str | Message displayed while async op is performed
 long_op_function  |  no-arg or lambda function | Function that is fired in an async second thread
 credentials_required  |  bool | If true, prompts to enter credentials before starting async op








