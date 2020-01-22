# Usage

Once `pyautogit` is installed, open a command line client (note that Windows Terminal is not supported), then navigate to a directory and type:
```
pyautogit
```
You can also specify an external directory:
```
pyautogit -w /home/jwlodek/repos
```
If you open `pyautogit` in a directory that contains a `.git` folder, it will treat it as a repository, while if it cannot find said folder, the target location will be treated as a workspace.

### Repository Screen


From the repository screen, you manage the local opened repository. You may create commits, tags, push and pull, and manage branches. For more detailed information on using the Repository Screen, please check the documentation. 

### Workspace Screen

The workspace screen allows for managing multiple `git` repositories at once. From here, all subdirectories that are identified as git repositories are listed, and you may open their respectiver repository screens. Also, you may clone new repositories, as well as create new blank repositories.

### Credential Management

When an action is performed that requires credentials (ex. git push), `pyautogit` will ask for your git remote username and password. These are then stored as environment variables for the running process, and are used with `git askpass` to perform operations. As a result, if you open an editor after credentials are entered (ex. VSCode), and use the integrated terminal to process `git` commands, you will not have to enter credentials again. Credentials are stored only for the duration the window is open, and must be re-entered after each restart.