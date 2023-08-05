#!/usr/bin/env python3
"""
Name: gtk-datetime-popover

Description: This datetime popover allows for the

Usage

License

# todo add module level docstrings
"""

import pathlib
from datetime import datetime
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# todo update test cases


# Helper functions #####################################################################################################
def _enlarge_spinbox_font(spinbutton):
    """Increases the font size of the provided gtk spinbutton by 400%."""
    css = b'''spinbutton {font-size: 400%;}'''
    style_provider = Gtk.CssProvider()
    style_provider.load_from_data(css)
    spinbox_style_context = spinbutton.get_style_context()
    spinbox_style_context.add_provider(style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)


def _show_leading_zeros(spinbutton):
    """Adds leading zeros to the given gtk spinbutton"""
    adjustment = spinbutton.get_adjustment()
    value = int(adjustment.get_value())
    spinbutton.set_text(f'{value:02d}')
    return True


# DateTimePicker Class ################################################################################################
class DateTimePicker:
    """This class implements a python gtk datetime picker. The values can be accessed via the given year, month, day,
    hour and minute properties as well as the datetime property. There are also methods available to raise the popover,
    set its relativity to another widget, connect callbacks to the closing of the popover or changing of the datetime
    values as well as to set or clear the date and time."""

    def __init__(self):
        """Initializes the picker object by locating and connecting to the glade file, fetching all the relevant
        widgets, setting up the spin buttons and initializing the datetime to none"""
        # gtk builder setup
        glade_file_path = str(pathlib.Path(__file__).resolve().parent / "datetime_popover.glade")
        gtk_builder = Gtk.Builder()
        gtk_builder.add_from_file(glade_file_path)
        gtk_builder.connect_signals(self)
        # Widget Fetching
        self._popover = gtk_builder.get_object('popover')
        self._stack_switcher = gtk_builder.get_object('stack_switcher')
        self._stack = gtk_builder.get_object('stack')
        self._calendar = gtk_builder.get_object('calendar')
        self._current_date_button = gtk_builder.get_object('current_date_button')
        self._clear_date_button = gtk_builder.get_object('clear_date_button')
        self._outer_time_grid = gtk_builder.get_object('outer_time_grid')
        self._hour_spinbox = gtk_builder.get_object('hour_spinbox')
        self._minute_spinbox = gtk_builder.get_object('minute_spinbox')
        self._clear_time_button = gtk_builder.get_object('clear_time_button')
        self._current_time_button = gtk_builder.get_object('current_time_button')
        # Spinbox setup
        for spinbox in [self._hour_spinbox, self._minute_spinbox]:
            _enlarge_spinbox_font(spinbox)
            spinbox.connect('output', _show_leading_zeros)
        # date initialization
        self.datetime = None

    # element handlers -------------------------------------------------------------------------------------------------
    def _on_calendar_day_selected(self, *_):
        """This handler is triggered whenever a day is selected on the calendar and is used to update the sensitivity of
        the clear date button and the sensitivity of the stack switcher"""
        self._update_clear_date_button()
        self._update_stack_switcher_sensitivity()

    def _on_time_spinboxes_changed(self, *_):
        """This handler is triggered whenever the hour or minute spinbuttons change and is used to update the clear
        time button"""
        self._update_clear_time_button()

    def _on_current_date_button_clicked(self, *_):
        """This handler is called when the  current date button is clicked and is used to select the current date"""
        self.select_current_date()

    def _on_clear_date_button_clicked(self, *_):
        """This handler is called when the clear date button is clicked and is used to unset the date"""
        self.clear_date()

    def _on_current_time_button_clicked(self, *_):
        """This handler is called when the current time button is clicked and is used to select the current time"""
        self.select_current_time()

    def _on_clear_time_button_clicked(self, *_):
        """This handler is called when the clear time button is clicked and is used to unset the time"""
        self.clear_time()

    #  Update Methods --------------------------------------------------------------------------------------------------
    def _update_clear_date_button(self):
        """Sets the clear date button sensitive if a day is selected and vice versa"""
        self._clear_date_button.set_sensitive(True if self.day else False)

    def _update_clear_time_button(self):
        """Sets the clear time button to sensitive if either the hour or minute is set to a non zero value"""
        hour = self._hour_spinbox.get_value_as_int()
        minute = self._minute_spinbox.get_value_as_int()
        sensitive = True if hour or minute else False
        self._clear_time_button.set_sensitive(sensitive)

    def _update_stack_switcher_sensitivity(self):
        """Sets the stack switcher to sensitive if a day is set on the calendar and vice versa"""
        self._stack_switcher.set_sensitive(True if self.day else False)

    # popover methods --------------------------------------------------------------------------------------------------
    def raise_popover(self):
        """Raises the popup"""
        self._popover.popup()
        self._popover.show_all()

    def set_relative_to(self, widget):
        """Sets the popover relative to another widget"""
        self._popover.set_relative_to(widget)

    def connect_popover_closed_signal(self, function):
        """Connects the given function to the popover closed signal handler. The passed function will run
        when the popover is closed"""
        self._popover.connect('closed', function)

    # Changed handler connection ---------------------------------------------------------------------------------------
    def connect_month_changed_signal(self, function):
        """Connects the given function to the changed signal handler for the year and month. The passed function will
        run when the year or month changes"""
        self._calendar.connect('month-changed', function)

    def connect_day_changed_signal(self, function):
        """Connects the given function to the changed signal handlers for the day. The passed function will run whenever
         the day changes"""
        self._calendar.connect('day-selected', function)

    def connect_hour_changed_signal(self, function):
        """Connects the given function to the changed signal handlers for the hour. The passed function will run
        whenever the hour changes"""
        self._hour_spinbox.connect('value-changed', function)

    def connect_minute_changed_signal(self, function):
        """Connects the given function to the changed signal handlers for the minute. The passed function will run
        whenever the minute changes"""
        self._minute_spinbox.connect('value-changed', function)

    #  Selection Functions ---------------------------------------------------------------------------------------------
    def select_current_date(self):
        """Sets the calendar to the current date. The time picker is not affected"""
        current_date = datetime.now()
        self.year = current_date.year
        self.month = current_date.month
        self.day = current_date.day

    def clear_date(self):
        """Selects the current date then deselects the day, clearing the date for the gtk widget. The time picker is
        not affected"""
        self.select_current_date()
        self.day = 0

    def select_current_time(self):
        """This handler sets the hour and minute spinboxes to the current time. The date is not affected"""
        current_time = datetime.now()
        self.hour = current_time.hour
        self.minute = current_time.minute

    def clear_time(self):
        """This handler clears the hour and minute spinboxes by setting both to 0 (which represents midnight).
        The date is not affected"""
        self.hour = 0
        self.minute = 0

    # datetime properties ----------------------------------------------------------------------------------------------
    @property
    def year(self):
        """This property returns the year of the picker as a  4 digit integer"""
        return self._calendar.get_date().year

    @year.setter
    def year(self, year):
        """Sets the calendar to the given year which must be an integer"""
        self._calendar.select_month(self.month - 1, year)

    @property
    def month(self):
        """Returns the selected month as an integer starting at one"""
        return self._calendar.get_date().month + 1

    @month.setter
    def month(self, month):
        """Sets the calendar to the given month, which should be an integer starting at one"""
        self._calendar.select_month(month - 1, self.year)

    @property
    def day(self):
        """Returns the day of the month as an integer starting from one. If zero is returned it means that no day is
        selected"""
        return self._calendar.get_date().day

    @day.setter
    def day(self, day):
        """Sets the calendars day of month to the given integer which starts at zero. Setting this value to zero
        deselects the day for the calendar"""
        self._calendar.select_day(day)
        self._update_clear_date_button()

    @property
    def hour(self):
        """Returns the hour of the day as a 24 hour format integer (0-23)"""
        return self._hour_spinbox.get_value_as_int()

    @hour.setter
    def hour(self, hour):
        """Sets the hour spinbutton to the given 23 hour format integer ranging (0-23)"""
        self._hour_spinbox.set_value(hour)
        self._update_clear_time_button()

    @property
    def minute(self):
        """Returns the minute of the hour as an integer (0-59)"""
        return self._minute_spinbox.get_value_as_int()

    @minute.setter
    def minute(self, minute):
        """Sets the minute spinbutton to the given integer ranging (0-59)"""
        self._minute_spinbox.set_value(minute)
        self._update_clear_time_button()

    @property
    def datetime(self):
        """Returns a python datetime instance set to the current date and time of the picker. If the calendar day is
        unselected, None is returned instead"""
        if self._calendar.get_date().day:
            return datetime(self.year, self.month, self.day, self.hour, self.minute)

    @datetime.setter
    def datetime(self, datetime_object):
        """Sets the year, month, day, hour and minute from the given python datetime instance. If None is  passed, then
        the date will be set to the current date, the time will be set to midnight and then the calendar day will be
        deselected"""
        if datetime_object:
            self.year = datetime_object.year
            self.month = datetime_object.month
            self.day = datetime_object.day
            self.hour = datetime_object.hour
            self.minute = datetime_object.minute
        else:
            self.clear_date()
            self.clear_time()


class DateTimeButton:
    """This class acts as a convenience widget for the datetime picker. The picker is connected to a button and
    callbacks have been added to set the label of the button to the date and time of the picker whenever it changes.

    The date_format_string property  is a python datetime format string that determines the datetime format the
    button label will be set with. The datetime_format_string is an optional python datetime format string that
    is used when the time is set to any other value that midnight. The no date string is used when there is no date
    present.
    """

    def __init__(
            self, date_format_string='%Y-%m-%d', datetime_format_string='%Y-%m-%d at %H:%M',
            no_date_string='Select Date'):
        """This initializes the datetime button instance. The date format string, datetime_format_string and
        no_date_string are explained above in the class docstring
        """

        self.date_format_string = date_format_string
        self.datetime_format_string = datetime_format_string
        self.no_date_string = no_date_string
        self.button = Gtk.Button()
        self.button.show()
        self.button.connect('clicked', self._on_button_clicked)
        self.picker = DateTimePicker()
        self.picker.set_relative_to(self.button)
        self.picker.connect_popover_closed_signal(self._on_popover_closed)
        self.picker.connect_month_changed_signal(self._on_datetime_changed)
        self.picker.connect_day_changed_signal(self._on_datetime_changed)
        self.picker.connect_hour_changed_signal(self._on_datetime_changed)
        self.picker.connect_minute_changed_signal(self._on_datetime_changed)
        self.set_date_button_label()

    def _on_button_clicked(self, *_):
        """This handler is called when the button is clicked and will raise the popover"""
        self.picker.raise_popover()

    def _on_popover_closed(self, *_):
        """This handler is called when the popover is closed  and will update the button's label"""
        self.set_date_button_label()

    def _on_datetime_changed(self, *_):
        """This handler is called when datetime properties are changed  and will update the button's label"""
        self.set_date_button_label()

    def set_date_button_label(self):
        """This method sets the buttons label to the date and time of the picker. If the datetime_format_string is
        present and the time is set to a non midnight value, then that string will be used over the date_format_string.
        If no datetime is present at all, the no_date_string is used.
        """
        if self.picker.datetime:
            use_datetime_format_string = (self.picker.minute or self.picker.hour) and self.datetime_format_string
            format_string = self.datetime_format_string if use_datetime_format_string else self.date_format_string
            final_date_string = self.picker.datetime.strftime(format_string)
            self.button.set_label(final_date_string)
        else:
            self.button.set_label(self.no_date_string)
