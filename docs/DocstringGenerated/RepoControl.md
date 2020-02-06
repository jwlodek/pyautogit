# File containing functions used by the repository specific CUI screen


This file is meant to handle the intermediate considerations between the 
CUI and the underlying git commands found in pyautogit.commands

Author: Jakub Wlodek
Created: 01-Oct-2019


# RepoControlManager 

``` python 
 class RepoControlManager(pyautogit.screen_manager.ScreenManager) 
```

Class responsible for managing functions for the repository control screen.

This class contains functions that are used by pyautogit for individual repository control.
It provides the interface between the CUI widgets for the repository control screen and
the pyautogit.commands module.

| Attributes    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|     menu_choices | list of str |         Overriden list of menu choices accessible from the repository control menu | 


--------- 

## Methods 

 
| method    | Doc             |
|:-------|:----------------|
| process_menu_selection | Override of base class, executes based on user menu selectio. | 
| initialize_screen_elements | Function that initializes the widgets for the repo control screen. Override of base class functio. | 
| clear_elements | Function that clears elements of repo control windo. | 
| set_initial_values | Function that initializes status bar and info text for repo control windo. | 
| refresh_status | Function that refreshes a git repository statu. | 
| get_repo_status_short | Gets shorthand repository statu. | 
| get_repo_remotes | Gets list of repository remote. | 
| show_branches | Function that swaps to showing branche. | 
| get_repo_branches | Gets list of repository branche. | 
| show_tags | Function that swaps to showing tag. | 
| get_repo_tags | Gets list of repository tag. | 
| show_remote_info | Gets info about remot. | 
| show_commit_info | Gets info about a particular commi. | 
| get_recent_commits | Gets list of recent commits to branc. | 
| create_new_tag | Creates a new ta. | 
| show_log | Displays the git lo. | 
| show_tree | Displays git log as a tre. | 
| stash_all_changes | Stashes all repo change. | 
| unstash_all_changes | Pops the stas. | 
| open_git_diff | Opens current git diff stat. | 
| open_git_diff_file | Gets the diff for a selected fil. | 
| open_editor | Opens an external editor if selecte. | 
| open_editor_file | Opens an external editor for a selected fil. | 
| add_all_changes | Adds all changes to stagin. | 
| add_revert_file | Adds/Reverts single file from stagin. | 
| ask_new_remote_name | Opens text box to enter new remote nam. | 
| ask_new_remote_url | Opens text box to ask new remote ur. | 
| add_remote | Adds remote to git rep. | 
| delete_remote | Deletes selected remote from local rep. | 
| rename_remote | Renames selected remote from local rep. | 
| commit | Commits currently staged item. | 
| pull_repo_branch | Pulls from remot. | 
| push_repo_branch | Pushes to remot. | 
| create_new_branch | Creates new branch for repositor. | 
| delete_branch | Deletes selected branc. | 
| checkout_branch | Checks out specified branc. | 
| merge_branches | Merges selected branch into the currently checked out branc. | 
| revert_merge | Undos the merge that was just performe. | 
| checkout_commit | Checks out specified commi. | 
| show_help_overview | Function that displays help message for overview mode. | 
| show_help_add_files_menu | Function that displays help message for the add files menu. | 
| show_help_remotes_menu | Function that displays help message for the add files menu. | 
| show_help_branch_menu | Function that displays help message for the add files menu. | 
| show_help_commits_menu | Function that displays help message for the add files menu. | 
 
 

### process_menu_selection

``` python 
    process_menu_selection(selection) 
```


Override of base class, executes based on user menu selectio.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         selection | str |             User selection from menu | 


### initialize_screen_elements

``` python 
    initialize_screen_elements() 
```


Function that initializes the widgets for the repo control screen. Override of base class functio.

| Returns    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         repo_control_widget_set | py_cui.widget_set.WidgetSet |             Widget set object for repo control screen | 


### clear_elements

``` python 
    clear_elements() 
```


Function that clears elements of repo control windo.

### set_initial_values

``` python 
    set_initial_values() 
```


Function that initializes status bar and info text for repo control windo.

### refresh_status

``` python 
    refresh_status() 
```


Function that refreshes a git repository statu.

### get_repo_status_short

``` python 
    get_repo_status_short() 
```


Gets shorthand repository statu.

### get_repo_remotes

``` python 
    get_repo_remotes() 
```


Gets list of repository remote.

### show_branches

``` python 
    show_branches() 
```


Function that swaps to showing branche.

### get_repo_branches

``` python 
    get_repo_branches() 
```


Gets list of repository branche.

### show_tags

``` python 
    show_tags() 
```


Function that swaps to showing tag.

### get_repo_tags

``` python 
    get_repo_tags() 
```


Gets list of repository tag.

### show_remote_info

``` python 
    show_remote_info() 
```


Gets info about remot.

### show_commit_info

``` python 
    show_commit_info() 
```


Gets info about a particular commi.

### get_recent_commits

``` python 
    get_recent_commits() 
```


Gets list of recent commits to branc.

### create_new_tag

``` python 
    create_new_tag() 
```


Creates a new ta.

### show_log

``` python 
    show_log() 
```


Displays the git lo.

### show_tree

``` python 
    show_tree() 
```


Displays git log as a tre.

### stash_all_changes

``` python 
    stash_all_changes() 
```


Stashes all repo change.

### unstash_all_changes

``` python 
    unstash_all_changes() 
```


Pops the stas.

### open_git_diff

``` python 
    open_git_diff() 
```


Opens current git diff stat.

### open_git_diff_file

``` python 
    open_git_diff_file() 
```


Gets the diff for a selected fil.

### open_editor

``` python 
    open_editor(file=None) 
```


Opens an external editor if selecte.

### open_editor_file

``` python 
    open_editor_file() 
```


Opens an external editor for a selected fil.

### add_all_changes

``` python 
    add_all_changes() 
```


Adds all changes to stagin.

### add_revert_file

``` python 
    add_revert_file() 
```


Adds/Reverts single file from stagin.

### ask_new_remote_name

``` python 
    ask_new_remote_name() 
```


Opens text box to enter new remote nam.

### ask_new_remote_url

``` python 
    ask_new_remote_url(remote_name) 
```


Opens text box to ask new remote ur.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         remote_name | str |             Remote name entered in previous textbox | 


### add_remote

``` python 
    add_remote(remote_url) 
```


Adds remote to git rep.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         remote_url | str |             URL entered by user | 


### delete_remote

``` python 
    delete_remote() 
```


Deletes selected remote from local rep.

### rename_remote

``` python 
    rename_remote() 
```


Renames selected remote from local rep.

### commit

``` python 
    commit() 
```


Commits currently staged item.

### pull_repo_branch

``` python 
    pull_repo_branch() 
```


Pulls from remot.

### push_repo_branch

``` python 
    push_repo_branch() 
```


Pushes to remot.

### create_new_branch

``` python 
    create_new_branch() 
```


Creates new branch for repositor.

### delete_branch

``` python 
    delete_branch() 
```


Deletes selected branc.

### checkout_branch

``` python 
    checkout_branch() 
```


Checks out specified branc.

### merge_branches

``` python 
    merge_branches() 
```


Merges selected branch into the currently checked out branc.

### revert_merge

``` python 
    revert_merge() 
```


Undos the merge that was just performe.

### checkout_commit

``` python 
    checkout_commit() 
```


Checks out specified commi.

### show_help_overview

``` python 
    show_help_overview() 
```


Function that displays help message for overview mode.

### show_help_add_files_menu

``` python 
    show_help_add_files_menu() 
```


Function that displays help message for the add files menu.

### show_help_remotes_menu

``` python 
    show_help_remotes_menu() 
```


Function that displays help message for the add files menu.

### show_help_branch_menu

``` python 
    show_help_branch_menu() 
```


Function that displays help message for the add files menu.

### show_help_commits_menu

``` python 
    show_help_commits_menu() 
```


Function that displays help message for the add files menu.