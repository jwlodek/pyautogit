# repo_select_screen

Manager implementation for CUI screen for selecting different repositories.






## RepoSelectManager(pyautogit.screen_manager.ScreenManager)

```python
class RepoSelectManager(pyautogit.screen_manager.ScreenManager)
```

Class representing the manager for the repo select screen




#### Attributes

 Attribute  | Type  | Doc
-----|----------|-----
 menu_choices  |  list of str | Overriden attribute from base class with expanded menu choices.

#### Methods

 Method  | Doc
-----|-----
 process_menu_selection | Override of base class, executes depending on menu selection
 refresh_status | Function that refreshes the repositories in the selection screen
 ask_delete_repo | Function that asks user for confirmation for repo deletion
 delete_repo | Function that deletes a repo
 show_repo_status | Function that displays git status info for current repo
 clone_new_repo | Function that clones new repo from given URL
 create_new_repo | Function that creates a new repo with a given name




### __init__

```python
def __init__(self, top_manager)
```

Constructor for repo select manager







### process_menu_selection

```python
def process_menu_selection(self, selection)
```

Override of base class, executes depending on menu selection





#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 selection  |  str | The user's menu selection





### initialize_screen_elements

```python
def initialize_screen_elements(self)
```

Override of base function. Initializes widgets, returns screen widget set




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 repo_select_widget_set  |  py_cui.widget_set.WidgetSet | Widget set object for repo select screen





### clear_elements

```python
def clear_elements(self)
```

Override of base class function, clears text fields







### set_initial_values

```python
def set_initial_values(self)
```

Override of base function. Sets some initial text for the widgets







### refresh_status

```python
def refresh_status(self)
```

Function that refreshes the repositories in the selection screen







### ask_delete_repo

```python
def ask_delete_repo(self)
```

Function that asks user for confirmation for repo deletion







### delete_repo

```python
def delete_repo(self, to_delete)
```

Function that deletes a repo




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 to_delete  |  bool | User's response of request for confirmation of deletion





### show_repo_status

```python
def show_repo_status(self)
```

Function that shows the current repository status







### clone_new_repo

```python
def clone_new_repo(self)
```

Function that clones new repo from given URL







### create_new_repo

```python
def create_new_repo(self)
```

Function that creates a new repo with a given name










