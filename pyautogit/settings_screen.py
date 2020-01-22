"""A subscreen that allows for setting a variety of pyautogit settings.
"""

import os
import datetime
import py_cui.widget_set
import pyautogit
import pyautogit.screen_manager
import pyautogit.logger as LOGGER


class SettingsScreen(pyautogit.screen_manager.ScreenManager):


    def __init__(self, top_manager):
        super().__init__(top_manager)


    def initialize_screen_elements(self):
        settings_widget_set = py_cui.widget_set.WidgetSet(12, 6)
        settings_widget_set.add_key_command(py_cui.keys.KEY_BACKSPACE, lambda : self.manager.open_repo_select_window(from_settings=True))
        logo_label = settings_widget_set.add_block_label(self.get_settings_ascii_art(), 0, 0, row_span=2, column_span=3, center=True)
        logo_label.set_standard_color(py_cui.RED_ON_BLACK)
        link_label = settings_widget_set.add_label('Settings Screen - pyautogit v{}'.format(pyautogit.__version__), 0, 3, row_span=2, column_span=3)
        link_label.add_text_color_rule('https://.*', py_cui.CYAN_ON_BLACK, 'contains', match_type='regex')

        debug_log_label = settings_widget_set.add_label('Debug Logging', 2, 0)
        debug_log_label.toggle_border()
        self.debug_log_toggle = settings_widget_set.add_button('Toggle Logs', 2, 1, command=self.toggle_logging)
        self.debug_enter_path_button = settings_widget_set.add_button('Set Log File', 2, 2, command = self.ask_log_file_path)
        self.debug_log_status_label = settings_widget_set.add_label('OFF - {}'.format(LOGGER._LOG_FILE_PATH), 2, 3, column_span=3)
        self.debug_log_status_label.toggle_border()


        self.settings_info_panel = settings_widget_set.add_text_block('Settings Info Panel', 4, 3, row_span=3, column_span=3)
        self.settings_info_panel.is_selectable = False
        self.info_panel = self.settings_info_panel
        return settings_widget_set


    def ask_log_file_path(self):
        self.manager.root.show_text_box_popup('Please enter a new log file path', self.update_log_file_path)


    def get_settings_ascii_art(self):
        settings_message = ' ____  ____  ____  ____  __  __ _   ___   ____  \n '
        settings_message = settings_message + '/ ___)(  __)(_  _)(_  _)(  )(  ( \ / __) / ___) \n'
        settings_message = settings_message + '\___ \ ) _)   )(    )(   )( /    /( (_ \ \___ \ \n'
        settings_message = settings_message + '(____/(____) (__)  (__) (__)\_)__) \___/ (____/ '
        return settings_message


    def toggle_logging(self):
        
        LOGGER.toggle_logging()
        self.refresh_status()


    def update_log_file_path(self, new_log_file_path):

        if os.path.exists(os.path.dirname(new_log_file_path)) and os.access(os.path.dirname(new_log_file_path), os.W_OK):
            LOGGER.set_log_file_path(new_log_file_path)
            self.refresh_status()
        else:
            self.manager.root.show_error_popup('Permission Error', 'The log file path either does not exist, or you do not have write permissions!')


    def refresh_status(self):
        logging_on_off = 'OFF'
        if LOGGER._LOG_ENABLED:
            logging_on_off = 'ON'
        log_file_path = LOGGER._LOG_FILE_PATH
        self.debug_log_status_label.title = '{} - {}'.format(logging_on_off, log_file_path)