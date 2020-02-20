"""Pyautogit internal editor, based on snano example from py_cui
"""

import os
import shutil
import py_cui.widget_set
import pyautogit.screen_manager

class EditorScreenManager(pyautogit.screen_manager.ScreenManager):
    """Class representing internal editor screen for pyautogit

    Attributes
    ----------
    opened_path : str
        The current opened path for the editor

    Methods
    -------
    initialize_screen_elements()
        Override of base class. Initializes editor widgets and widget set
    set_initial_values()
        Function that sets status bar text
    clear_elements()
        Function for clearing widgets in editor screen
    open_new_directory_external()
        Opens a new directory given an external target
    open_new_directory()
        Function that opens a new directory
    add_new_file()
        Function for creating a new file
    open_file_dir()
        Function that opens a file/directory from menu
    save_opened_file()
        Function that saves the opened file
    delete_selected_file()
        Function that deletes the selected file
    """

    def __init__(self, top_manager, opened_path):
        """Contructor for the EditorScreenManager
        """

        super().__init__(top_manager, 'editor')
        if os.path.isdir(opened_path):
            self.opened_path = opened_path
        else:
            self.opened_path = os.dirname(opened_path)

        self.new_file_open = False


    def initialize_screen_elements(self):
        """Override of base class. Initializes editor widgets and widget set

        Returns
        -------
        pyautogit_editor_widget_set : py_cui.widget_set.WidgetSet
            Widget set for internal editor screen
        """

        pyautogit_editor_widget_set = py_cui.widget_set.WidgetSet(7, 8)

        self.current_dir_textbox = pyautogit_editor_widget_set.add_text_box('Current Directory', 6, 0, column_span=8)
        self.current_dir_textbox.add_key_command(py_cui.keys.KEY_ENTER, self.open_new_directory)
        self.current_dir_textbox.set_text(self.opened_path)
        self.current_dir_textbox.set_focus_text('Open Directory - Enter | Cancel - Esc')

        self.edit_text_block = pyautogit_editor_widget_set.add_text_block('Open file', 0, 2, row_span=6, column_span=6)
        self.edit_text_block.set_focus_text('Save - Esc + S | Return - Esc')

        self.new_dir_textbox = pyautogit_editor_widget_set.add_text_box('Add New Directory', 4, 0, column_span=2)
        self.new_dir_textbox.add_key_command(py_cui.keys.KEY_ENTER, self.add_new_directory)
        self.new_dir_textbox.set_focus_text('Create Directory - Enter | Cancel - Esc')

        self.new_file_textbox = pyautogit_editor_widget_set.add_text_box('Add New File', 5, 0, column_span=2)
        self.new_file_textbox.add_key_command(py_cui.keys.KEY_ENTER, self.add_new_file)
        self.new_file_textbox.set_focus_text('Create File - Enter | Cancel - Esc')

        self.file_menu = pyautogit_editor_widget_set.add_scroll_menu('Directory Files', 0, 0, row_span=4, column_span=2)
        self.file_menu.add_key_command(py_cui.keys.KEY_ENTER,   self.open_file_dir)
        self.file_menu.add_key_command(py_cui.keys.KEY_DELETE,  self.delete_selected_file_dir)
        self.file_menu.add_key_command(py_cui.keys.KEY_F_LOWER, lambda : self.manager.root.move_focus(self.new_file_textbox))
        self.file_menu.add_key_command(py_cui.keys.KEY_D_LOWER, lambda : self.manager.root.move_focus(self.new_dir_textbox))
        self.file_menu.add_key_command(py_cui.keys.KEY_R_LOWER, self.refresh_status)
        self.file_menu.add_key_command(py_cui.keys.KEY_BACKSPACE, self.manager.open_autogit_window_target)
        self.file_menu.add_text_color_rule('<DIR>', py_cui.GREEN_ON_BLACK, 'startswith', match_type='region', region=[5,1000])
        self.file_menu.set_focus_text('Return -Bcksp | Open - Enter | New File - f | New Dir - d | Refresh - r | Delete - Del | Return - Esc')

        self.info_panel = self.edit_text_block

        pyautogit_editor_widget_set.add_key_command(py_cui.keys.KEY_S_LOWER, self.save_opened_file)
        pyautogit_editor_widget_set.add_key_command(py_cui.keys.KEY_M_LOWER, lambda : self.manager.root.move_focus(self.file_menu))
        pyautogit_editor_widget_set.add_key_command(py_cui.keys.KEY_BACKSPACE, self.manager.open_autogit_window_target)

        self.open_new_directory()

        return pyautogit_editor_widget_set


    def refresh_status(self):
        """Function that refreshes the view of the file menu on new dir or file creation
        """

        self.open_new_directory_external(self.current_dir_textbox.get())


    def set_initial_values(self):
        """Function that sets status bar text
        """

        self.manager.root.set_status_bar_text('Return - Bcksp | Save Open File - s | Open File Menu - m | Navigate - Arrows')


    def clear_elements(self):
        """Function for clearing widgets in editor screen
        """

        self.info_panel.clear()
        self.info_panel.title = 'Open file'
        self.current_dir_textbox.clear()
        self.new_file_textbox.clear()
        self.file_menu.clear()


    def open_new_directory_external(self, new_dir_path):
        """Opens a new directory given an external target

        Parameters
        ----------
        new_dir_path : str
            Path of directory to open
        """

        self.current_dir_textbox.set_text(new_dir_path)
        self.open_new_directory()


    def open_new_directory(self):
        """Function that opens a new directory
        """

        target = self.current_dir_textbox.get()
        if len(target) == 0:
            target = '.'
        elif not os.path.exists(target):
            self.manager.root.show_error_popup('Does not exist', 'ERROR - {} path does not exist'.format(target))
            return
        elif not os.path.isdir(target):
            self.manager.root.show_error_popup('Not a Dir', 'ERROR - {} is not a directory'.format(target))
            return
        target = os.path.abspath(target)
        self.current_dir_textbox.set_text(target)
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
        """Function for creating a new file
        """

        if os.path.exists(os.path.join(self.current_dir_textbox.get(), self.new_file_textbox.get())):
            self.manager.root.show_error_popup('File Exists', 'File exists with name {}!'.format(self.new_file_textbox.get()))
        else:
            self.edit_text_block.title = 'Open file - ' + self.new_file_textbox.get() + ' - (Unsaved)'
            self.edit_text_block.clear()
            self.new_file_textbox.clear()
            self.manager.root.move_focus(self.edit_text_block)


    def add_new_directory(self):
        """Function for creating a new directory
        """

        try:
            os.mkdir(self.new_dir_textbox.get())
            self.new_dir_textbox.clear()
            self.refresh_status()
            self.manager.root.move_focus(self.file_menu)
        except OSError:
            self.manager.root.show_error_popup('OS ERROR', 'Failed to create new directory!')


    def open_file_dir(self):
        """Function that opens a file/directory from menu
        """

        filename = self.file_menu.get()
        if filename.startswith('<DIR>'):
            self.current_dir_textbox.set_text(os.path.join(self.opened_path, filename[6:]))
            self.open_new_directory()
        else:
            try:
                self.edit_text_block.text_color_rules = []
                fp = open(os.path.join(self.opened_path, filename), 'r')
                text = fp.read()
                fp.close()
                self.edit_text_block.set_text(text)
                self.edit_text_block.title = 'Open file - {}'.format(filename)
            except:
                self.manager.root.show_warning_popup('Not a text file', 'The selected file could not be opened - not a text file')


    def save_opened_file(self):
        """Function that saves the opened file
        """

        if self.edit_text_block.title.startswith('Open file - '):
            filename = self.edit_text_block.title.split('-', 1)[1].strip()
            fp = open(os.path.join(self.opened_path, filename), 'w')
            fp.write(self.edit_text_block.get())
            fp.close()
            self.refresh_status()
            self.manager.root.move_focus(self.edit_text_block)
            self.edit_text_block.title = 'Open file - {}'.format(filename)
        else:
            self.manager.root.show_error_popup('No File Opened', 'Please open a file before saving it.')


    def delete_selected_file_dir(self):
        """Function that deletes the selected file
        """

        if not self.file_menu.get().startswith('<DIR>'):
            target = os.path.join(self.current_dir_textbox.get(), self.file_menu.get())
            try:
                os.remove(target)
            except:
                self.manager.root.show_error_popup('Delete Error', 'Failed to delete the target file!')
        else:
            target = os.path.join(self.current_dir_textbox.get(), self.file_menu.get()[6:])
            try:
                shutil.rmtree(target)
            except:
                self.manager.root.show_error_popup('Delete Error', 'Could not remove target directory!')

        self.refresh_status()

