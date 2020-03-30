"""A subscreen that allows for setting a variety of pyautogit settings.
"""

import os
import webbrowser
import datetime
import py_cui.widget_set
import pyautogit
import pyautogit.screen_manager
import pyautogit.logger as LOGGER
import urllib.request
import urllib.error


class SettingsScreen(pyautogit.screen_manager.ScreenManager):
    """Class representing settings subscreen for pyautogit

    Attributes
    ----------
    current_info_log : str
        The current settings log text
    show_settings_log : bool
        Toggle for showing settings log
    """


    def __init__(self, top_manager):
        """Constructor for SettingsScreen
        """

        super().__init__(top_manager, 'settings screen')
        self.current_info_log = ''
        self.show_settings_log = True


    def initialize_screen_elements(self):
        """Override of base class function. Initializes widgets, and returns widget set

        Returns
        -------
        settings_widget_set : py_cui.widget_set.WidgetSet
            Widget set object for rsettings screen
        """

        # Output widget set
        settings_widget_set = self.manager.root.create_new_widget_set(9, 6)
        settings_widget_set.add_key_command(py_cui.keys.KEY_BACKSPACE, self.manager.open_repo_select_window)

        # Logo and link labels
        logo_label = settings_widget_set.add_block_label(self.get_settings_ascii_art(), 0, 0, row_span=2, column_span=3, center=True)
        logo_label.set_color(py_cui.RED_ON_BLACK)
        link_label = settings_widget_set.add_label('Settings Screen - pyautogit v{}'.format(pyautogit.__version__), 0, 3, row_span=2, column_span=3)
        link_label.add_text_color_rule('Settings Screen*', py_cui.CYAN_ON_BLACK, 'startswith', match_type='line')

        # Logging settings
        debug_log_label = settings_widget_set.add_label('Debug Logging', 2, 0)
        debug_log_label.toggle_border()
        self.debug_log_toggle = settings_widget_set.add_button('Toggle Logs', 2, 1, command=self.toggle_logging)
        self.debug_enter_path_button = settings_widget_set.add_button('Set Log File', 2, 2, command=self.ask_log_file_path)
        self.debug_log_status_label = settings_widget_set.add_label('OFF - {}'.format(LOGGER._LOG_FILE_PATH), 3, 0, column_span=3)

        # Default editor settings
        editor_label = settings_widget_set.add_label('Default Editor', 4, 0)
        editor_label.toggle_border()
        self.external_editor_toggle = settings_widget_set.add_button('External/Internal',   4, 1, command=self.toggle_editor_type)
        self.external_editor_enter  = settings_widget_set.add_button('Select Editor',       4, 2, command=self.ask_default_editor)
        self.editor_status_label = settings_widget_set.add_label('{} - {}'.format(self.manager.editor_type, self.manager.default_editor), 5, 0, column_span=3)
        #self.editor_status_label.toggle_border()

        # Program info settings
        about_label = settings_widget_set.add_label('About', 6, 0)
        about_label.toggle_border()
        self.fetch_readme_file_button   = settings_widget_set.add_button('README',          6, 1, command=lambda : self.fetch_about_file('README.md'))
        self.fetch_authors_button       = settings_widget_set.add_button('Authors',         6, 2,  command=lambda : self.fetch_about_file('AUTHORS'))
        self.fetch_license_button       = settings_widget_set.add_button('License',         7, 1, command=lambda : self.fetch_about_file('LICENSE'))
        self.revert_settings_log_button = settings_widget_set.add_button('Settings Log',    7, 2, command=self.revert_settings_log)

        # Documentation settings
        docs_label = settings_widget_set.add_label('Docs', 8, 0)
        docs_label.toggle_border()
        self.show_tutorial_button = settings_widget_set.add_button('Tutorial', 8, 1, command=self.show_tutorial)
        self.open_web_docs_button = settings_widget_set.add_button('Online Docs', 8, 2, command=self.open_web_docs)

        # Info panel
        self.settings_info_panel = settings_widget_set.add_text_block('Settings Info Log', 2, 3, row_span=7, column_span=3)
        self.settings_info_panel.is_selectable = False
        self.info_panel = self.settings_info_panel

        if not LOGGER._LOG_ENABLED:
            self.update_log_file_path('.pyautogit/{}.log'.format(str(datetime.datetime.today()).split(' ')[0]), default_path=True)
        return settings_widget_set


    def set_initial_values(self):
        """Function that sets initial status bar text for settings window
        """

        self.manager.root.set_status_bar_text('Backspace - Return | Enter - Press Buttons | Arrows - Navigate')


    def add_to_settings_log(self, text):
        """Function that updates the settings info log panel

        Parameters
        ----------
        text : str
            New log item to write to settings info panel
        """

        self.current_info_log = '{}\n{}'.format(text, self.current_info_log)
        if self.show_settings_log:
            self.settings_info_panel.set_text(self.current_info_log)


    def fetch_about_file(self, file):
        """Function that grabs file from github and displays it in info panel

        Parameters
        ----------
        file : str
            Filename to fetch from github repository
        """

        self.info_panel.clear()
        self.info_panel.is_selectable = True
        self.show_settings_log = False

        try:
            file_txt = ''
            for line in urllib.request.urlopen('https://raw.githubusercontent.com/jwlodek/pyautogit/master/{}'.format(file)):
                file_txt = '{}{}'.format(file_txt, line.decode('utf-8'))
            self.info_panel.set_text(file_txt)
        except urllib.error.HTTPError:
            self.revert_settings_log()
            self.manager.root.show_error_popup('Http Error', 'Unable to fetch {} file - not found!'.format(file))
        except:
            self.revert_settings_log()
            self.manager.root.show_error_popup('Unknown Error', 'Unable to fetch {} file!'.format(file))


    def revert_settings_log(self):
        """Function that resets to showing settings info
        """

        self.info_panel.is_selectable = False
        if not self.show_settings_log:
            self.show_settings_log = True
        self.info_panel.clear()
        self.info_panel.set_text(self.current_info_log)


    def open_web_docs(self):
        """Function tasked with open docs in external browser
        """

        try:
            webbrowser.open('https://jwlodek.github.io/pyautogit-docs')
        except:
            self.manager.root.show_error_popup('Unknown Error', 'Unable to open online documentation!')


    def show_tutorial(self):
        """Function that demonstrates tutorial for using pyautogit
        """

        self.manager.root.show_warning_popup('Unimplemented', 'The Tutorial feature has not yet been implemented.')


    def ask_log_file_path(self):
        """Prompts user to enter log file path
        """

        self.manager.root.show_text_box_popup('Please enter a new log file path', self.update_log_file_path)


    def get_settings_ascii_art(self):
        """Gets ascii art settings logo

        Returns
        -------
        settings_message : str
            Block letter ascii art settings logo
        """

        settings_message =                      ' ____  ____  ____  ____  __  __ _   ___   ____  \n '
        settings_message = settings_message +   '/ ___)(  __)(_  _)(_  _)(  )(  ( \ / __) / ___) \n'
        settings_message = settings_message +   '\___ \ ) _)   )(    )(   )( /    /( (_ \ \___ \ \n'
        settings_message = settings_message +   '(____/(____) (__)  (__) (__)\_)__) \___/ (____/ '
        return settings_message


    def toggle_editor_type(self):
        """Function that toggles between internal and external editor
        """

        if self.manager.editor_type == 'Internal':
            self.manager.editor_type = 'External'
        else:
            self.manager.editor_type = 'Internal'
        self.add_to_settings_log('Swapped editor type')
        self.refresh_status()


    def toggle_logging(self):
        """Function that enables/disables logging
        """
        
        LOGGER.toggle_logging()
        self.add_to_settings_log('Toggled logging')
        self.refresh_status()


    def ask_default_editor(self):
        """Function that asks user for editor, and then refreshes
        """

        self.manager.root.show_text_box_popup('Please enter a command to open an external text editor', self.update_default_editor)


    def update_default_editor(self, new_editor):
        """Function that updates the new default editor

        Parameters
        ----------
        new_editor : str
            command used to open external editor
        """

        self.manager.default_editor = new_editor
        if self.manager.editor_type == 'Internal':
            self.toggle_editor_type()
        self.add_to_settings_log('Update default editor to: {}'.format(new_editor))
        self.refresh_status()


    def update_log_file_path(self, new_log_file_path, default_path=False):
        """Function that updates log file path if valid

        Parameters
        ----------
        new_log_file_path : str
            Path to new log file
        """

        if os.path.exists(os.path.dirname(new_log_file_path)) and os.access(os.path.dirname(new_log_file_path), os.W_OK):
            LOGGER.set_log_file_path(new_log_file_path)
            self.add_to_settings_log('Update log file path: {}'.format(new_log_file_path))
            self.refresh_status()
        elif not default_path:
            self.manager.root.show_error_popup('Permission Error', 'The log file path either does not exist, or you do not have write permissions!')


    def refresh_status(self):
        """Override of base class refresh function.
        """

        logging_on_off = 'OFF'
        if LOGGER._LOG_ENABLED:
            logging_on_off = 'ON'
        log_file_path = LOGGER._LOG_FILE_PATH
        self.debug_log_status_label.set_title('{} - {}'.format(logging_on_off, log_file_path))

        self.editor_status_label.set_title('{} - {}'.format(self.manager.editor_type, self.manager.default_editor))