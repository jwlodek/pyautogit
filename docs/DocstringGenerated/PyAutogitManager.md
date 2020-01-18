# File containing entry point for pyautogit, as well as a top level class for managing the program


It also contains some helper functions and argument parsing.

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
|     repo_control_manager | RepoControlManager |         Manager wrapper for repo control screen. | 

