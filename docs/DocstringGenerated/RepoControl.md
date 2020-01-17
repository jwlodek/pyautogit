# File containing functions used by the repository specific CUI screen


This file is meant to handle the intermediate considerations between the 
CUI and the underlying git commands found in pyautogit.commands

Author: Jakub Wlodek
Created: 01-Oct-2019


# RepoControlManager 

``` python 
 class RepoControlManager(SM.ScreenManager) 
```

Class responsible for managing functions for the repository control screen.

This class contains functions that are used by pyautogit for individual repository control.
It provides the interface between the CUI widgets for the repository control screen and
the pyautogit.commands module.

| Attributes    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|     manager | PyAutogitManager |         The master PyAutogitManager object | 
|     message | str |         A helper attribute for sending messages between functions | 
|     status | int |         A helper attribute for sending status codes between functions | 
|     utility_var | obj |         A helper attribute for sending objects between functions | 
|     menu_choices | list of str |         A list of menu choices accessible from the repository control menu | 


--------- 

## Methods 

 
| method    | Doc             |
|:-------|:----------------|
| process_menu_selection | Function that refreshes a git repository statu. | 
| get_repo_status_short |  | 
| ask_new_remote_url | Opens text box to ask new remote ur. | 
| add_remote | Adds remote to git rep. | 
| delete_remote | Deletes selected remote from local rep. | 
| rename_remote | Renames selected remote from local rep. | 
 
 

### process_menu_selection

``` python 
    process_menu_selection(selection) 
```


Function that refreshes a git repository statu.

### get_repo_status_short

``` python 
    get_repo_status_short() 
```




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