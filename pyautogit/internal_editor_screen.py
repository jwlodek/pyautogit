"""Pyautogit internal editor, based on snano example from py_cui
"""

import os
import py_cui.widget_set
import pyautogit.screen_manager

class EditorScreenManager(pyautogit.screen_manager.ScreenManager):
    """Class representing internal editor screen for pyautogit
    """

    def __init__(self, top_manager, opened_path):

        super().__init__(top_manager, 'editor')
        if os.path.isdir(opened_path):
            self.opened_path = opened_path
        else:
            self.opened_path = os.dirname(opened_path)


    def initialize_screen_elements(self):

        pyautogit_editor_widget_set = py_cui.widget_set.WidgetSet(7, 8)

        pyautogit_editor_widget_set.add_key_command(py_cui.keys.KEY_S_LOWER, self.save_opened_file)
        pyautogit_editor_widget_set.add_key_command(py_cui.keys.KEY_BACKSPACE, self.manager.open_autogit_window_target)

        self.file_menu = pyautogit_editor_widget_set.add_scroll_menu('Directory Files', 0, 0, row_span=5, column_span=2)

        self.file_menu.add_key_command(py_cui.keys.KEY_ENTER, self.open_file_dir)
        self.file_menu.add_key_command(py_cui.keys.KEY_DELETE, self.delete_selected_file)
        self.file_menu.add_text_color_rule('<DIR>', py_cui.GREEN_ON_BLACK, 'startswith', match_type='region', region=[5,1000])



        self.new_dir_box = pyautogit_editor_widget_set.add_text_box('Current Directory', 6, 0, column_span=2)
        self.new_dir_box.set_text(self.opened_path)


        self.open_new_directory()

        self.edit_text_block = pyautogit_editor_widget_set.add_text_block('Open file', 0, 2, row_span=7, column_span=6)

        self.new_dir_box.add_key_command(py_cui.keys.KEY_ENTER, self.open_new_directory)

        self.new_file_textbox = pyautogit_editor_widget_set.add_text_box('Add New File', 5, 0, column_span=2)
        self.new_file_textbox.add_key_command(py_cui.keys.KEY_ENTER, self.add_new_file)

        self.info_panel = self.edit_text_block
        return pyautogit_editor_widget_set

    
    def open_new_directory_external(self, new_dir_path):
        self.new_dir_box.set_text(new_dir_path)
        self.open_new_directory()
    


    def open_new_directory(self):
        target = self.new_dir_box.get()
        if len(target) == 0:
            target = '.'
        elif not os.path.exists(target):
            self.manager.root.show_error_popup('Does not exist', 'ERROR - {} path does not exist'.format(target))
            return
        elif not os.path.isdir(target):
            self.manager.root.show_error_popup('Not a Dir', 'ERROR - {} is not a directory'.format(target))
            return
        target = os.path.abspath(target)
        self.new_dir_box.set_text(target)
        self.opened_path = target

        files = []
        files.append('<DIR> ..')
        dir_contents = os.listdir(self.opened_path)
        for elem in dir_contents:
            if os.path.isfile(os.path.join(self.opened_path, elem)):
                files.append(elem)
            else:
                files.append('<DIR> ' + elem)

        self.file_menu.clear()
        self.file_menu.add_item_list(files)
        

    def add_new_file(self):
        self.file_menu.add_item(self.new_file_textbox.get())
        self.file_menu.selected_item = len(self.file_menu.get_item_list()) - 1
        self.new_file_textbox.selected = False
        self.manager.root.set_selected_widget(self.edit_text_block.id)
        self.edit_text_block.title = self.new_file_textbox.get()
        self.edit_text_block.clear()
        self.new_file_textbox.clear()


    def open_file_dir(self):
        filename = self.file_menu.get()
        if filename.startswith('<DIR>'):
            self.new_dir_box.set_text(os.path.join(self.opened_path, filename[6:]))
            self.open_new_directory()
        else:
            try:
                self.edit_text_block.text_color_rules = []
                fp = open(os.path.join(self.opened_path, filename), 'r')
                text = fp.read()
                fp.close()
                self.edit_text_block.set_text(text)
                self.edit_text_block.title = filename
            except:
                self.manager.root.show_warning_popup('Not a text file', 'The selected file could not be opened - not a text file')


    def save_opened_file(self):
        if self.edit_text_block.title != 'Open file':
            fp = open(os.path.join(self.opened_path, self.edit_text_block.title), 'w')
            fp.write(self.edit_text_block.get())
            fp.close()
            self.manager.root.show_message_popup('Saved', 'Your file has been saved as {}'.format(self.edit_text_block.title))
        else:
            self.manager.root.show_error_popup('No File Opened', 'Please open a file before saving it.')


    def delete_selected_file(self):
        if self.edit_text_block.title != 'Open file':
            try:
                os.remove(os.path.join(self.opened_path, self.edit_text_block.title))
                self.edit_text_block.clear()
                self.edit_text_block.title = 'Open file'
                self.file_menu.remove_selected_item()
            except OSError:
                self.manager.root.show_error_popup('OS Error', 'Operation could not be completed due to an OS error.')
        else:
            self.manager.root.show_error_popup('No File Opened', 'Please open a file before deleting it.')

