"""File containing class that acts as a parent class to all sub-screen managers
"""

from sys import platform
import pyautogit.commands


class ScreenManager:
    """Main parent screen manager class.

    Contains common functionality for showing command results, handling credentials, commands, and long operations.

    Attributes
    ----------
    manager : PyAutogitManager
        Driver engine manager
    message : str
        A variable to store messages accross functions
    status : int
        A variable to store status codes accross functions
    utility_var : obj
        A variable that can be used to store any data across functions
    menu_choices : list of str
        Overriden by children, list of options that pop up in menu
    info_panel : py_cui.widgets.TextBlock
        The main textblock on the screen, used to display status information.

    Methods
    -------
    process_menu_selection()
        Overriden by child, processes based on menu item selection.
    show_command_result()
        Displays the result of running a particular command. If more than one line of output, prints to info panel, otherwise, shows popup.
    show_status_long_op()
        Used instead of show_command_result for long (async) operations
    show_menu()
        Opens the menu for the screen manager object
    refresh_git_status()
        Function called after each git operation by children. Must be overriden
    handle_user_command()
        Processes a custom command from the user
    ask_custom_command()
        Prompts user to enter a custom command
    execute_long_operation()
        Wrapper function that should be used as lambda operation. Allows for performing long async operation while loading icon runs
    """

    def __init__(self, top_manager):
        """Constructor for ScreenManager
        """

        self.manager = top_manager
        self.message = ''
        self.status = 0
        self.utility_var = None
        self.menu_choices = ['About', 'Exit']
        self.info_panel = None


    def process_menu_selection(self, selection):
        """Processes based on selection returned from the menu

        Parameters
        ----------
        selection : str
            An element of the self.menu_choices list selected by user
        """

        if selection == 'Exit':
            exit()


    # TODO: Make this a lambda function
    def show_menu(self):
        """Opens the menu using the menu item list for screen manager instance
        """
        
        self.manager.root.show_menu_popup('Full Control Menu', self.menu_choices, self.process_menu_selection)


    def show_command_result(self, out, err, show_on_success = True, command_name='Command', success_message='Success', error_message='Error'):
        """Function that displays the result of stdout/err for an external command.

        Parameters
        ----------
        out : str
            stdout string from command
        err : str
            stderr string from command
        show_on_success : bool
            Set to false to show no messages on success. (ex. git log doesnt need success message)
        command_name : str
            name of command run.
        success_message : str
            message to show on successful completion
        error_message : str
            message to show on unsuccessful completion
        """

        show_in_box = False
        stripped_output = out.strip()
        if len(out.splitlines()) > 1:
            popup_message = "Check Info Box For {} Output".format(command_name)
            show_in_box = True
        else:
            popup_message = stripped_output
        if err != 0:
            self.manager.root.show_error_popup(error_message, popup_message)
        elif show_on_success:
            self.manager.root.show_message_popup(success_message, popup_message)
        if show_in_box and (err != 0 or show_on_success):
            box_out = out
            if err != 0:
                err_out = '\n'
                temp = out.splitlines()
                for line in temp:
                    err_out = err_out + '- ' + line + '\n'
                box_out = err_out
            self.info_panel.title = '{} Output'.format(command_name)
            self.info_panel.set_text(box_out)


    def show_status_long_op(self, name='Command', succ_message="Success", err_message = "Error"):
        """Shows the status of a long(async) operation on success completion

        Parameters
        ----------
        name : str
            name of command run.
        succ_message : str
            message to show on successful completion
        err_message : str
            message to show on unsuccessful completion
        """

        self.show_command_result(self.message, self.status, command_name=name, success_message=succ_message, error_message=err_message)
        self.message = ''
        self.status = 0


    def refresh_git_status(self):
        """Function that is fired after each git operation. Implement in subclasses.
        """

        pass


    def handle_user_command(self, command):
        """Handles custom user command.

        Parameters
        ----------
        command : str
            The string command entered by the user
        """

        out, err = pyautogit.commands.handle_custom_command(command)
        self.show_command_result(out, err, command_name=command)
        self.refresh_git_status()


    def ask_custom_command(self):
        """Function that prompts user to enter custom command
        """

        shell='Bash'
        if platform == 'win32':
            shell='Batch'
        self.manager.root.show_text_box_popup('Please Enter A {} Command:'.format(shell), self.handle_user_command)

    
    def execute_long_operation(self, loading_messge, long_op_function, credentials_required=False):
        """Wrapper function that allows for executing long operations w/ credential requirements.

        Parameters
        ----------
        loading_message : str
            Message displayed while async op is performed
        long_op_function : no-arg or lambda function
            Function that is fired in an async second thread
        credentials_required : bool
            If true, prompts to enter credentials before starting async op
        """
        
        if credentials_required and not self.manager.were_credentials_entered():
            self.manager.ask_credentials(callback=lambda : self.manager.perform_long_operation(loading_messge, long_op_function, self.show_status_long_op))
        else:
            self.manager.perform_long_operation(loading_messge, long_op_function, self.show_status_long_op)