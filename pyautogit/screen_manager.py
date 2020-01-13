class ScreenManager:


    def __init__(self, top_manager):
        self.manager = top_manager
        self.message = ''
        self.status = 0
        self.utility_var = None
        self.menu_choices = ['About', 'Exit']
        self.info_panel = None

    def process_menu_selection(self, selection):
        if selection == 'Exit':
            exit()


    def show_command_result(self, out, err, show_on_success = True, command_name='Command', success_message='Success', error_message='Error'):
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
        self.show_command_result(self.message, self.status, command_name=name, success_message=succ_message, error_message=err_message)
        self.message = ''
        self.status = 0


    # TODO: Make this a lambda function
    def show_menu(self):
        self.manager.root.show_menu_popup('Full Control Menu', self.menu_choices, self.process_menu_selection)


    def refresh_git_status(self):
        pass

    def handle_user_command(self, command):
        out, err = pyautogit.commands.handle_custom_command(command)
        self.show_command_result(out, err, command_name=command)
        self.refresh_git_status()

    def ask_custom_command(self):
        shell='Bash'
        if platform == 'win32':
            shell='Batch'
        self.manager.root.show_text_box_popup('Please Enter A {} Command:'.format(shell), self.handle_user_command)

    
    def execute_long_operation(self, loading_messge, long_op_function, credentials_required=False):
        if credentials_required and not self.manager.were_credentials_entered():
            self.manager.ask_credentials(callback=lambda : self.manager.perform_long_operation(loading_messge, long_op_function, self.show_status_long_op))
        else:
            self.manager.perform_long_operation(loading_messge, long_op_function, self.show_status_long_op)