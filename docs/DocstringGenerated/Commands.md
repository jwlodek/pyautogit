# commands

File containing all definitions and functions for git commands used by pyautogit.



This file should remain separate from the CUI interface.

Author: Jakub Wlodek
Created: 01-Oct-2019




### remove_repo_tree

```python
def remove_repo_tree(target)
```

Function that removes repository.



Required since removing git repos on windows require a chmod operation.


#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 target  |  str | Dir path to removed repo





### del_rw

```python
def del_rw(action, name, exc)
```









### handle_credential_command

```python
def handle_credential_command(command, credentials, target_location='.')
```

Function that executes a git command that requires credentials.




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 command  |  str | String command to run
 credentials  |  list of str | The user's entered git remote credentials
 target_location  |  str | Location of repository

#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 out  |  str | Output string from stdout if success, stderr if failure
 err  |  int | Error code if failure, 0 otherwise.





### parse_string_into_executable_command

```python
def parse_string_into_executable_command(command, remove_quotes)
```

Function that takes in a string command, and parses it into a subprocess arg list




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 command  |  str | The command as a string

#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 run_command  |  list of str | The command as a list of subprocess args





### handle_basic_command

```python
def handle_basic_command(command, name, remove_quotes=True)
```

Function that executes any git command given, and returns program output.




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 command  |  str | The command string to run
 name  |  str | The name of the command being run
 remove_quotes  |  bool | Since subprocess takes an array of strings, we split on spaces, however in some cases we want quotes to remain together (ex. commit message)

#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 out  |  str | Output string from stdout if success, stderr if failure
 err  |  int | Error code if failure, 0 otherwise.





### handle_open_external_program_command

```python
def handle_open_external_program_command(command, name)
```

Function used to run commands that open an external program and detatch from pyautogit.




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 command  |  str | Command string to run
 name  |  str | Name of command to run

#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 out  |  str | Output string from stdout if success, stderr if failure
 err  |  int | Error code if failure, 0 otherwise.





### handle_custom_command

```python
def handle_custom_command(command)
```

Function that executes a custom, non-git command



Patameters
----------
command : str
Command string to run


#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 out  |  str | Output string from stdout if success, stderr if failure
 err  |  int | Error code if failure, 0 otherwise.





### open_default_editor

```python
def open_default_editor(default_editor, path)
```

Function used to open the selected default editor in external window.




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 default_editor  |  str | Editor open command. ex: emacs, code
 path  |  str | The path to the file or directory to open

#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 out  |  str | Output string from stdout if success, stderr if failure
 err  |  int | Error code if failure, 0 otherwise.





### git_status_short

```python
def git_status_short(repo_path='.')
```

Function for getting shorthand git status




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 repo_path  |  str | Target repo path

#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 out  |  str | Output string from stdout if success, stderr if failure
 err  |  int | Error code if failure, 0 otherwise.





### git_status

```python
def git_status(repo_path='.')
```

Function for getting git status




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 repo_path  |  str | Target repo path

#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 out  |  str | Output string from stdout if success, stderr if failure
 err  |  int | Error code if failure, 0 otherwise.





### git_tree

```python
def git_tree(branch)
```

Function that gets git log as a tree




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 branch  |  str | branch or tag name to log

#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 out  |  str | Output string from stdout if success, stderr if failure
 err  |  int | Error code if failure, 0 otherwise.





### git_log

```python
def git_log(branch)
```

Function that gets git log information




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 branch  |  str | branch or tag name to log

#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 out  |  str | Output string from stdout if success, stderr if failure
 err  |  int | Error code if failure, 0 otherwise.





### git_diff

```python
def git_diff()
```

Function that gets git diff




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 out  |  str | Output string from stdout if success, stderr if failure
 err  |  int | Error code if failure, 0 otherwise.





### git_diff_file

```python
def git_diff_file(filename)
```

Function that gets git diff for specific file




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 filename  |  str | Name of file to diff

#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 out  |  str | Output string from stdout if success, stderr if failure
 err  |  int | Error code if failure, 0 otherwise.





### git_get_remotes

```python
def git_get_remotes()
```

Function for returning git remotes list




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 out  |  str | Output string from stdout if success, stderr if failure
 err  |  int | Error code if failure, 0 otherwise.





### git_get_remote_info

```python
def git_get_remote_info(remote)
```

Function that gets information about a remote




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 remote  |  str | Name of target remote

#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 out  |  str | Output string from stdout if success, stderr if failure
 err  |  int | Error code if failure, 0 otherwise.





### git_add_remote

```python
def git_add_remote(remote_name, remote_url)
```

Function that adds a new remote to the repository




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 remote_name  |  str | Name of the new remote
 remote_url  |  str | URL of the new remote

#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 out  |  str | Output string from stdout if success, stderr if failure
 err  |  int | Error code if failure, 0 otherwise.





### git_remove_remote

```python
def git_remove_remote(remote_name)
```

Function that removes a remote from the repository




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 remote_name  |  str | Name of the remote

#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 out  |  str | Output string from stdout if success, stderr if failure
 err  |  int | Error code if failure, 0 otherwise.





### git_rename_remote

```python
def git_rename_remote(remote, new_name)
```

Function that renames a remote in the repository




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 remote  |  str | Old name of the remote
 new_name  |  str | New name of the new remote

#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 out  |  str | Output string from stdout if success, stderr if failure
 err  |  int | Error code if failure, 0 otherwise.





### git_get_commit_info

```python
def git_get_commit_info(commit_hash)
```

Function that gets info about a particular commit.




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 commit_hash  |  str | Hash code for target commit

#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 out  |  str | Output string from stdout if success, stderr if failure
 err  |  int | Error code if failure, 0 otherwise.





### git_checkout_commit

```python
def git_checkout_commit(commit_hash)
```

Function that checks out a particular commit.




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 commit_hash  |  str | Hash code for target commit

#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 out  |  str | Output string from stdout if success, stderr if failure
 err  |  int | Error code if failure, 0 otherwise.





### git_commit_changes

```python
def git_commit_changes(commit_message)
```

Function that commits added changes




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 commit_message  |  str | Message attached to target commit

#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 out  |  str | Output string from stdout if success, stderr if failure
 err  |  int | Error code if failure, 0 otherwise.





### git_create_tag

```python
def git_create_tag(tag_name)
```

Function that creates a new tag




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 tag_name  |  str | The name of the new tag

#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 out  |  str | Output string from stdout if success, stderr if failure
 err  |  int | Error code if failure, 0 otherwise.





### git_get_tags

```python
def git_get_tags()
```

Function that gets list of git tags in repo




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 out  |  str | Output string from stdout if success, stderr if failure
 err  |  int | Error code if failure, 0 otherwise.





### git_get_branches

```python
def git_get_branches()
```

Function that gets a list of the repo branches.




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 out  |  str | Output string from stdout if success, stderr if failure
 err  |  int | Error code if failure, 0 otherwise.





### git_get_recent_commits

```python
def git_get_recent_commits(branch)
```

Gets recent commits made to the branch




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 branch  |  str | Name of current branch

#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 out  |  str | Output string from stdout if success, stderr if failure
 err  |  int | Error code if failure, 0 otherwise.





### git_create_new_branch

```python
def git_create_new_branch(branch, checkout=True)
```

Creates anew branch for the repo




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 branch  |  str | Name of new branch
 checkout  |  bool | If true, checkout branch after creation.

#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 out  |  str | Output string from stdout if success, stderr if failure
 err  |  int | Error code if failure, 0 otherwise.





### git_delete_branch

```python
def git_delete_branch(branch)
```

Deletes existing git branch




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 branch  |  str | Name of branch to delete

#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 out  |  str | Output string from stdout if success, stderr if failure
 err  |  int | Error code if failure, 0 otherwise.





### git_checkout_branch

```python
def git_checkout_branch(branch)
```

Checks out given branch




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 branch  |  str | Name of target branch

#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 out  |  str | Output string from stdout if success, stderr if failure
 err  |  int | Error code if failure, 0 otherwise.





### git_checkout_tag

```python
def git_checkout_tag(tag)
```

Checks out given tag




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 tag  |  str | Name of tag to check out

#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 out  |  str | Output string from stdout if success, stderr if failure
 err  |  int | Error code if failure, 0 otherwise.





### git_merge_branches

```python
def git_merge_branches(merge_branch)
```

Merges checked out branch with given branch




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 merge_branch  |  str |

#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 out  |  str | Output string from stdout if success, stderr if failure
 err  |  int | Error code if failure, 0 otherwise.





### git_revert_branch_merge

```python
def git_revert_branch_merge()
```

Undos merge between two branches




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 out  |  str | Output string from stdout if success, stderr if failure
 err  |  int | Error code if failure, 0 otherwise.





### git_init_new_repo

```python
def git_init_new_repo(new_dir_target)
```

Function that creates a new git repository




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 new_dir_target  |  str | Name of new repo

#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 out  |  str | Output string from stdout if success, stderr if failure
 err  |  int | Error code if failure, 0 otherwise.





### git_clone_new_repo

```python
def git_clone_new_repo(new_repo_url, credentials)
```

Function that clones a new git repository




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 new_repo_url  |  str | URL of new repo
 credentials  |  list of str | Username and Password for git remote

#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 out  |  str | Output string from stdout if success, stderr if failure
 err  |  int | Error code if failure, 0 otherwise.





### git_add_all

```python
def git_add_all()
```

Function that stages all files in repo for commit.




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 out  |  str | Output string from stdout if success, stderr if failure
 err  |  int | Error code if failure, 0 otherwise.





### git_reset_all

```python
def git_reset_all()
```

Function that unstages all files in repo for commit.




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 out  |  str | Output string from stdout if success, stderr if failure
 err  |  int | Error code if failure, 0 otherwise.





### git_add_file

```python
def git_add_file(filename)
```

Function that stages single file in repo for commit.




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 filename  |  str | Name of file to stage

#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 out  |  str | Output string from stdout if success, stderr if failure
 err  |  int | Error code if failure, 0 otherwise.





### git_reset_file

```python
def git_reset_file(filename)
```

Function that unstages single file in repo for commit.




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 filename  |  str | Name of file to unstage

#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 out  |  str | Output string from stdout if success, stderr if failure
 err  |  int | Error code if failure, 0 otherwise.





### git_stash_all

```python
def git_stash_all()
```

Function that stashes all changes in repo.




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 out  |  str | Output string from stdout if success, stderr if failure
 err  |  int | Error code if failure, 0 otherwise.





### git_unstash_all

```python
def git_unstash_all()
```

Function that unstashes all changes in repo.




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 out  |  str | Output string from stdout if success, stderr if failure
 err  |  int | Error code if failure, 0 otherwise.





### git_stash_file

```python
def git_stash_file(filename)
```

Function that stashes single file in repo.




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 filename  |  str | Name of file to stash

#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 out  |  str | Output string from stdout if success, stderr if failure
 err  |  int | Error code if failure, 0 otherwise.





### git_pull_branch

```python
def git_pull_branch(branch, remote, credentials)
```

Function that pulls a branch from the remote repo




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 branch  |  str | Name of current branch
 remote  |  str | Name of remote
 credentials  |  list of str | Username and Password of user for remoe

#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 out  |  str | Output string from stdout if success, stderr if failure
 err  |  int | Error code if failure, 0 otherwise.





### git_push_to_branch

```python
def git_push_to_branch(branch, remote, credentials, repo_path='.')
```

Function that pushes a branch to the remote repo




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 branch  |  str | Name of current branch
 remote  |  str | Name of remote
 credentials  |  list of str | Username and Password of user for remote
 repo_path  |  str | The repository path

#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 out  |  str | Output string from stdout if success, stderr if failure
 err  |  int | Error code if failure, 0 otherwise.





