# Manager implementation for CUI screen for selecting different repositories


# RepoSelectManager 

``` python 
 class RepoSelectManager(pyautogit.screen_manager.ScreenManager) 
```

Class representing the manager for the repo select scree.

| Attributes    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|     menu_choices | list of str |         Overriden attribute from base class with expanded menu choices. | 


--------- 

## Methods 

 
| method    | Doc             |
|:-------|:----------------|
| process_menu_selection | Override of base class, executes depending on menu selectio. | 
| initialize_screen_elements | Override of base function. Initializes widgets, returns screen widget se. | 
| clear_elements | Override of base class function, clears text field. | 
| set_initial_values | Override of base function. Sets some initial text for the widget. | 
| refresh_status | Function that refreshes the repositories in the selection scree. | 
| ask_delete_repo | Function that asks user for confirmation for repo deletio. | 
| delete_repo | Function that deletes a rep. | 
| show_repo_status | Function that shows the current repository statu. | 
| clone_new_repo | Function that clones new repo from given UR. | 
| create_new_repo | Function that creates a new repo with a given nam. | 
 
 

### process_menu_selection

``` python 
    process_menu_selection(selection) 
```


Override of base class, executes depending on menu selectio.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         selection | str |             The user's menu selection | 


### initialize_screen_elements

``` python 
    initialize_screen_elements() 
```


Override of base function. Initializes widgets, returns screen widget se.

| Returns    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         repo_select_widget_set | py_cui.widget_set.WidgetSet |             Widget set object for repo select screen | 


### clear_elements

``` python 
    clear_elements() 
```


Override of base class function, clears text field.

### set_initial_values

``` python 
    set_initial_values() 
```


Override of base function. Sets some initial text for the widget.

### refresh_status

``` python 
    refresh_status() 
```


Function that refreshes the repositories in the selection scree.

### ask_delete_repo

``` python 
    ask_delete_repo() 
```


Function that asks user for confirmation for repo deletio.

### delete_repo

``` python 
    delete_repo(to_delete) 
```


Function that deletes a rep.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         to_delete | bool |             User's response of request for confirmation of deletion | 


### show_repo_status

``` python 
    show_repo_status() 
```


Function that shows the current repository statu.

### clone_new_repo

``` python 
    clone_new_repo() 
```


Function that clones new repo from given UR.

### create_new_repo

``` python 
    create_new_repo() 
```


Function that creates a new repo with a given nam.