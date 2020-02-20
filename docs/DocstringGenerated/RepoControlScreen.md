# repo_control_screen

File containing functions used by the repository specific CUI screen.



This file is meant to handle the intermediate considerations between the 
CUI and the underlying git commands found in pyautogit.commands

Author: Jakub Wlodek  
Created: 01-Oct-2019


#### Classes

 Class  | Doc
-----|-----
 RepoControlManager | Extension of ScreenManager, manages repository control actions




## RepoControlManager(pyautogit.screen_manager.ScreenManager)

```python
class RepoControlManager(pyautogit.screen_manager.ScreenManager)
```

Class responsible for managing functions for the repository control screen.



This class contains functions that are used by pyautogit for individual repository control.
It provides the interface between the CUI widgets for the repository control screen and
the pyautogit.commands module.


#### Attributes

 Attribute  | Type  | Doc
-----|----------|-----
 menu_choices  |  list of str | Overriden list of menu choices accessible from the repository control menu

#### Methods

 Method  | Doc
-----|-----
 process_menu_selection | Override of base class, executes based on user menu selection
 refresh_status | Function that refreshes a git repository status
 get_repo_status_short | Gets shorthand repository status
 get_repo_remotes | gets list of repository remotes
 get_repo_branches | gets list of repository branches
 show_remote_info | gets info about remote
 show_commit_info | gets info about a particular commit
 get_recent_commits | gets list of recent commits to branch
 create_new_tag | Creates a new tag
 show_log | Displays the git log
 stash_all_changes | Stashes all repo changes
 unstash_all_changes | Pops the stash
 open_git_diff | Opens current git diff state
 open_git_diff_file | Gets the diff for a selected file
 open_editor | Opens an external editor if selected
 open_editor_file | Opens an external editor for a selected file
 add_all_changes | Adds all changes to staging
 add_revert_file | Adds/Reverts single file from staging
 ask_new_remote_name | Asks user for new remote name
 ask_new_remote_url | Asks user for new remote url
 add_remote | Adds a new remote to repo
 delete_remote | Deletes selected remote from local repo
 rename_remote | Renames selected remote from local repo
 commit | Commits currently staged items
 pull_repo_branch | pulls from remote
 push_repo_branch | pushes to remote
 create_new_branch | Creates new branch for repository
 checkout_branch | Checks out specified branch
 checkout_commit | Checks out specified commit




### __init__

```python
def __init__(self, top_manager)
```

Constructor for the RepoControlManager class







### process_menu_selection

```python
def process_menu_selection(self, selection)
```

Override of base class, executes based on user menu selection




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 selection  |  str | User selection from menu





### initialize_screen_elements

```python
def initialize_screen_elements(self)
```

Function that initializes the widgets for the repo control screen. Override of base class function




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 repo_control_widget_set  |  py_cui.widget_set.WidgetSet | Widget set object for repo control screen





### clear_elements

```python
def clear_elements(self)
```

Function that clears elements of repo control window







### set_initial_values

```python
def set_initial_values(self)
```

Function that initializes status bar and info text for repo control window







### refresh_status

```python
def refresh_status(self)
```

Function that refreshes a git repository status







### get_repo_status_short

```python
def get_repo_status_short(self)
```

Gets shorthand repository status







### get_repo_remotes

```python
def get_repo_remotes(self)
```

Gets list of repository remotes







### show_branches

```python
def show_branches(self)
```

Function that swaps to showing branches







### get_repo_branches

```python
def get_repo_branches(self)
```

Gets list of repository branches







### show_tags

```python
def show_tags(self)
```

Function that swaps to showing tags







### get_repo_tags

```python
def get_repo_tags(self)
```

Gets list of repository tags







### show_remote_info

```python
def show_remote_info(self)
```

Gets info about remote







### show_commit_info

```python
def show_commit_info(self)
```

Gets info about a particular commit







### get_recent_commits

```python
def get_recent_commits(self)
```

Gets list of recent commits to branch







### create_new_tag

```python
def create_new_tag(self)
```

Creates a new tag







### show_log

```python
def show_log(self)
```

Displays the git log







### show_tree

```python
def show_tree(self)
```

Displays git log as a tree







### stash_all_changes

```python
def stash_all_changes(self)
```

Stashes all repo changes







### unstash_all_changes

```python
def unstash_all_changes(self)
```

Pops the stash







### open_git_diff

```python
def open_git_diff(self)
```

Opens current git diff state







### open_git_diff_file

```python
def open_git_diff_file(self)
```

Gets the diff for a selected file







### open_editor

```python
def open_editor(self, file=None)
```

Opens an external editor if selected







### open_editor_file

```python
def open_editor_file(self)
```

Opens an external editor for a selected file







### add_all_changes

```python
def add_all_changes(self)
```

Adds all changes to staging







### add_revert_file

```python
def add_revert_file(self)
```

Adds/Reverts single file from staging







### ask_new_remote_name

```python
def ask_new_remote_name(self)
```

Opens text box to enter new remote name







### ask_new_remote_url

```python
def ask_new_remote_url(self, remote_name)
```

Opens text box to ask new remote url




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 remote_name  |  str | Remote name entered in previous textbox





### add_remote

```python
def add_remote(self, remote_url)
```

Adds remote to git repo




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 remote_url  |  str | URL entered by user





### delete_remote

```python
def delete_remote(self)
```

Deletes selected remote from local repo







### rename_remote

```python
def rename_remote(self)
```

Renames selected remote from local repo







### commit

```python
def commit(self)
```

Commits currently staged items







### pull_repo_branch

```python
def pull_repo_branch(self)
```

Pulls from remote







### push_repo_branch

```python
def push_repo_branch(self)
```

Pushes to remote







### create_new_branch

```python
def create_new_branch(self)
```

Creates new branch for repository







### delete_branch

```python
def delete_branch(self)
```

Deletes selected branch







### checkout_branch

```python
def checkout_branch(self)
```

Checks out specified branch







### merge_branches

```python
def merge_branches(self)
```

Merges selected branch into the currently checked out branch







### revert_merge

```python
def revert_merge(self)
```

Undos the merge that was just performed







### checkout_commit

```python
def checkout_commit(self)
```

Checks out specified commit







### show_help_overview

```python
def show_help_overview(self)
```

Function that displays help message for overview mode.







### show_help_add_files_menu

```python
def show_help_add_files_menu(self)
```

Function that displays help message for the add files menu.







### show_help_remotes_menu

```python
def show_help_remotes_menu(self)
```

Function that displays help message for the add files menu.







### show_help_branch_menu

```python
def show_help_branch_menu(self)
```

Function that displays help message for the add files menu.







### show_help_commits_menu

```python
def show_help_commits_menu(self)
```

Function that displays help message for the add files menu.










