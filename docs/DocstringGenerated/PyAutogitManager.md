# Main pyautogit manager class and entry point


Author: Jakub Wlodek
Created: 01-Oct-2019


# PyAutogitManager 

``` python 
 class PyAutogitManager 
```

Main pyautogit manager class. Controls all operations of CU.

| Attributes    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|     root | PyCUI |         The root py_cui window | 
|     target_path | str |         The path to the workspace directory | 
|     save_metadata | bool |         Flag to specify metadata saving or not | 
|     credentials | list of str |         Username and Password for git remote | 
|     current_state | str |         Current state of pyautogit (repo control or repo select) | 
|     default_editor | str |         Command to open external editor | 
|     post_input_callback | no-arg or lambda function |         Function fired after a user input event | 
|     operation_thread | Thread |         A thread for performing async operations. Starts as None, Thread created as needed | 
|     repos | list of str |         List of repositories found in workspace | 
|     repo_select_widget_set | py_cui.widget_set.WidgetSet |         set of py_cui widgets that are parts of the repo select screen | 
|     repo_menu | py_cui.widgets.ScrollMenu |         The repository select menu in the repo select screen | 
|     git_status_box | py_cui.widgets.ScrolledTextBlock |         Main info panel for repo select screen | 
|     current_status_box | py_cui.widgets.ScrolledTextBlock |         Secondary info panel for repo select screen | 
|     clone_new_box | py_cui.widgets.TextBox |         Textbox for cloning new repositories | 
|     create_new_box | py_cui.widgets.TextBox |         Textbox for creating new repositories | 
|     repo_select_manager | RepoSelectManager |         The manager wrapper class for the repo select screen | 
|     repo_control_widget_set | py_cui.widget_set.WidgetSet |         set of py_cui widgets that are parts of the repo control screen | 
|     add_files_menu | py_cui.widgets.ScrollMenu |         Menu for adding/unstaging files | 
|     remotes_menu | py_cui.widgets.ScrollMenu |         Menu for selecting remotes | 
|     branch_menu | py_cui.widgets.ScrollMenu |         Menu for selecting branches | 
|     commits_menu | py_cui.widgets.ScrollMenu |         Menu listing most recent commits | 
|     info_text_block | py_cui.widgets.ScrolledTextBlock |         Main Info text block in repo control screen | 
|     new_branch_textbox | py_cui.widgets.TextBox |         Textbox for creating new branches | 
|     commit_message_box | py_cui.widgets.TextBox |         Textbox for entering new commit messages | 
|     repo_control_manager | RepoControlManager |         Manager wrapper for repo control screen | 


--------- 

## Methods 

 
| method    | Doc             |
|:-------|:----------------|
| close_cleanup | Function fired upon closing pyautogi. | 
| clean_exit | Function that exits the CUI cleanl. | 
| error_exit | Function that exits the CUI with an error cod. | 
| open_not_supported_popup | Function that displays warning for a non-supported operatio. | 
| open_autogit_window | Function that opens the repository control window. | 
| open_autogit_window_target | Function that opens a repo control window given a target locatio. | 
| open_repo_select_window | Opens the repo select window. Fired when the backspace key is pressed in the repo control windo. | 
| open_settings_window | Function for opening the settings windo. | 
| open_editor_window | Function that opens an editor windo. | 
| update_password | Function called once password is entered.. | 
| ask_password | Function that opens popup and asks for password. Also writes username to credentials. | 
| ask_credentials | Function that asks for user credentials and places them in the appropriate variables. | 
| were_credentials_entered | Simple function for checking if credentials were entere. | 
| perform_long_operation | Function that wraps an operation around a loading icon popup. | 
| update_default_editor | Function that sets the default edito. | 
| ask_default_editor | Function that asks user to enter a default text edito. | 
| update_message | Function that is run after user inputs messag. | 
| ask_message | Function that asks the user for input. | 
| get_logo_text | Generates ascii-art version of pyautogit log. | 
| get_about_info | Generates some about me informatio. | 
| get_welcome_message | Function that gets a basic welcome message shown at first ru. | 
 
 

### close_cleanup

``` python 
    close_cleanup() 
```


Function fired upon closing pyautogi.

### clean_exit

``` python 
    clean_exit() 
```


Function that exits the CUI cleanl.

### error_exit

``` python 
    error_exit() 
```


Function that exits the CUI with an error cod.

### open_not_supported_popup

``` python 
    open_not_supported_popup(operation) 
```


Function that displays warning for a non-supported operatio.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         operation | str |             The name of the non-supported operation | 


### open_autogit_window

``` python 
    open_autogit_window() 
```


Function that opens the repository control window.

### open_autogit_window_target

``` python 
    open_autogit_window_target() 
```


Function that opens a repo control window given a target locatio.

### open_repo_select_window

``` python 
    open_repo_select_window() 
```


Opens the repo select window. Fired when the backspace key is pressed in the repo control windo.

### open_settings_window

``` python 
    open_settings_window() 
```


Function for opening the settings windo.

### open_editor_window

``` python 
    open_editor_window() 
```


Function that opens an editor windo.

### update_password

``` python 
    update_password(passwd) 
```


Function called once password is entered..

If necessary, fires the post_input_callback function

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         passwd | str |             The user's password | 


### ask_password

``` python 
    ask_password(user) 
```


Function that opens popup and asks for password. Also writes username to credentials.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         user | str |             The user's username | 


### ask_credentials

``` python 
    ask_credentials(callback=None) 
```


Function that asks for user credentials and places them in the appropriate variables.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         callback | function |             Default None, otherwise function called after credentials are entered. | 


### were_credentials_entered

``` python 
    were_credentials_entered() 
```


Simple function for checking if credentials were entere.

| Returns    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         were_credentials_entered | bool |             True if credentials found, otherwise false | 


### perform_long_operation

``` python 
    perform_long_operation(title, long_operation_function, post_loading_callback) 
```


Function that wraps an operation around a loading icon popup.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         title | str |             title for loading icon | 
|         long_operation_function | function |             operation to perform in the background | 
|         post_loading_callback | function |             Function fired once long operation is finished. | 


### update_default_editor

``` python 
    update_default_editor() 
```


Function that sets the default edito.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         editor | str |             command line call to open the editor | 


### ask_default_editor

``` python 
    ask_default_editor() 
```


Function that asks user to enter a default text edito.

### update_message

``` python 
    update_message(message) 
```


Function that is run after user inputs messag.



| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         message | str |             User returned input | 


### ask_message

``` python 
    ask_message(prompt, callback=None) 
```


Function that asks the user for input.



| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         prompt | str |             Prompt for user input | 
|         callback | function |             Default None, otherwise, function fired after credentials are asked | 


### get_logo_text

``` python 
    get_logo_text() 
```


Generates ascii-art version of pyautogit log.

| Returns    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         logo | str |             ascii-art logo | 


### get_about_info

``` python 
    get_about_info(with_logo=True) 
```


Generates some about me informatio.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         with_logo | bool |             flag to show logo or not.         | 


| Returns    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         about_info | str |             string with about information | 


### get_welcome_message

``` python 
    get_welcome_message() 
```


Function that gets a basic welcome message shown at first ru.



| Returns    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         welcome | str |             welcome message string | 
