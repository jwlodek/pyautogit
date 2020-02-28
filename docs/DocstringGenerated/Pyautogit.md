# pyautogit

Main pyautogit manager class and entry point



The main driver class contains code for common actions performed by all subscreens such as
credential management, as well as functions for switching between subscreens.

Author: Jakub Wlodek  
Created: 01-Oct-2019

#### Classes

 Class  | Doc
-----|-----
 PyAutogitManager | Main pyautogit manager class. Controls all operations of CUI

#### Functions

 Function  | Doc
-----|-----
 find_repos_in_path | Helper function that finds repositories in the path
 is_git_repo | Simple function that checks if a given path is a git repository
 parse_args | Function that parses user arguments for pyautogit
 main | Entry point for pyautogit. Parses arguments, and initializes the CUI




### find_repos_in_path

```python
def find_repos_in_path(path)
```

Helper function that finds repositories in the path




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 path  |  str | Target path

#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 repos  |  list of str | list of git repositories within target





### is_git_repo

```python
def is_git_repo(path)
```

Simple function that checks if a given path is a git repository




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 path  |  str | path to check

#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 is_repo  |  bool | True if .git exists, False otherwise





### parse_args

```python
def parse_args()
```

Function that parses user arguments for pyautogit




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 target_repo  |  str | The target path for pyautogit
 save_metadata  |  bool | flag to say if metadata should be saved
 credentials  |  list of str | username, password, if entered





### main

```python
def main()
```

Entry point for pyautogit. Parses arguments, and initializes the CUI







## PyAutogitManager

```python
class PyAutogitManager
```

Main pyautogit manager class. Controls all operations of CUI




#### Attributes

 Attribute  | Type  | Doc
-----|----------|-----
 root  |  PyCUI | The root py_cui window
 target_path  |  str | The path to the workspace directory
 save_metadata  |  bool | Flag to specify metadata saving or not
 credentials  |  list of str | Username and Password for git remote
 current_state  |  str | Current state of pyautogit (repo control or repo select)
 default_editor  |  str | Command to open external editor
 post_input_callback  |  no-arg or lambda function | Function fired after a user input event
 operation_thread  |  Thread | A thread for performing async operations. Starts as None, Thread created as needed
 repos  |  list of str | List of repositories found in workspace
 repo_select_widget_set  |  py_cui.widget_set.WidgetSet | set of py_cui widgets that are parts of the repo select screen
 repo_menu  |  py_cui.widgets.ScrollMenu | The repository select menu in the repo select screen
 git_status_box  |  py_cui.widgets.ScrolledTextBlock | Main info panel for repo select screen
 current_status_box  |  py_cui.widgets.ScrolledTextBlock | Secondary info panel for repo select screen
 clone_new_box  |  py_cui.widgets.TextBox | Textbox for cloning new repositories
 create_new_box  |  py_cui.widgets.TextBox | Textbox for creating new repositories
 repo_select_manager  |  RepoSelectManager | The manager wrapper class for the repo select screen
 repo_control_widget_set  |  py_cui.widget_set.WidgetSet | set of py_cui widgets that are parts of the repo control screen
 add_files_menu  |  py_cui.widgets.ScrollMenu | Menu for adding/unstaging files
 remotes_menu  |  py_cui.widgets.ScrollMenu | Menu for selecting remotes
 branch_menu  |  py_cui.widgets.ScrollMenu | Menu for selecting branches
 commits_menu  |  py_cui.widgets.ScrollMenu | Menu listing most recent commits
 info_text_block  |  py_cui.widgets.ScrolledTextBlock | Main Info text block in repo control screen
 new_branch_textbox  |  py_cui.widgets.TextBox | Textbox for creating new branches
 commit_message_box  |  py_cui.widgets.TextBox | Textbox for entering new commit messages
 repo_control_manager  |  RepoControlManager | Manager wrapper for repo control screen

#### Methods

 Method  | Doc
-----|-----
 close_cleanup | Function fired upon closing pyautogit
 clean_exit | Function that exits the CUI cleanly
 error_exit | Function that exits the CUI with an error code
 open_not_supported_popup | Function that displays warning for a non-supported operation
 open_autogit_window | Function that opens the repository control window.
 open_autogit_window_target | Function that opens a repo control window given a target location
 open_repo_select_window | Opens the repo select window. Fired when the backspace key is pressed in the repo control window
 open_settings_window | Function for opening the settings window
 open_editor_window | Function that opens an editor window
 update_password | Function called once password is entered.
 ask_password | Function that opens popup and asks for password. Also writes username to credentials.
 ask_credentials | Function that asks for user credentials and places them in the appropriate variables.
 were_credentials_entered | Simple function for checking if credentials were entered
 perform_long_operation | Function that wraps an operation around a loading icon popup.
 update_default_editor | Function that sets the default editor
 ask_default_editor | Function that asks user to enter a default text editor
 update_message | Function that is run after user inputs message
 ask_message | Function that asks the user for input.
 get_logo_text | Generates ascii-art version of pyautogit logo
 get_about_info | Generates some about me information
 get_welcome_message | Function that gets a basic welcome message shown at first run




### __init__

```python
def __init__(self, root, target_path, current_state, save_metadata, credentials)
```

Constructor for PyAutogitManager







### close_cleanup

```python
def close_cleanup(self)
```

Function fired upon closing pyautogit







### clean_exit

```python
def clean_exit(self)
```

Function that exits the CUI cleanly







### error_exit

```python
def error_exit(self)
```

Function that exits the CUI with an error code







### open_not_supported_popup

```python
def open_not_supported_popup(self, operation)
```

Function that displays warning for a non-supported operation




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 operation  |  str | The name of the non-supported operation





### open_autogit_window

```python
def open_autogit_window(self)
```

Function that opens the repository control window.







### open_autogit_window_target

```python
def open_autogit_window_target(self)
```

Function that opens a repo control window given a target location







### open_repo_select_window

```python
def open_repo_select_window(self)
```

Opens the repo select window. Fired when the backspace key is pressed in the repo control window







### open_settings_window

```python
def open_settings_window(self)
```

Function for opening the settings window







### open_editor_window

```python
def open_editor_window(self)
```

Function that opens an editor window







### update_password

```python
def update_password(self, passwd)
```

Function called once password is entered.



If necessary, fires the post_input_callback function


#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 passwd  |  str | The user's password





### ask_password

```python
def ask_password(self, user)
```

Function that opens popup and asks for password. Also writes username to credentials.




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 user  |  str | The user's username





### ask_credentials

```python
def ask_credentials(self, callback=None)
```

Function that asks for user credentials and places them in the appropriate variables.




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 callback  |  function | Default None, otherwise function called after credentials are entered.





### were_credentials_entered

```python
def were_credentials_entered(self)
```

Simple function for checking if credentials were entered




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 were_credentials_entered  |  bool | True if credentials found, otherwise false





### perform_long_operation

```python
def perform_long_operation(self, title, long_operation_function, post_loading_callback)
```

Function that wraps an operation around a loading icon popup.




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 title  |  str | title for loading icon
 long_operation_function  |  function | operation to perform in the background
 post_loading_callback  |  function | Function fired once long operation is finished.





### update_default_editor

```python
def update_default_editor(self)
```

Function that sets the default editor




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 editor  |  str | command line call to open the editor





### ask_default_editor

```python
def ask_default_editor(self)
```

Function that asks user to enter a default text editor







### update_message

```python
def update_message(self, message)
```

Function that is run after user inputs message




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 message  |  str | User returned input





### ask_message

```python
def ask_message(self, prompt, callback=None)
```

Function that asks the user for input.




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 prompt  |  str | Prompt for user input
 callback  |  function | Default None, otherwise, function fired after credentials are asked





### get_logo_text

```python
def get_logo_text(self)
```

Generates ascii-art version of pyautogit logo




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 logo  |  str | ascii-art logo





### get_about_info

```python
def get_about_info(self, with_logo=True)
```

Generates some about me information




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 with_logo  |  bool | flag to show logo or not.

#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 about_info  |  str | string with about information





### get_welcome_message

```python
def get_welcome_message(self)
```

Function that gets a basic welcome message shown at first run




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 welcome  |  str | welcome message string








