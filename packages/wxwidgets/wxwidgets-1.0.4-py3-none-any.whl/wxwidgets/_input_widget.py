from wx import Panel, TextCtrl, HORIZONTAL, EVT_BUTTON, TOP, EVT_TEXT_ENTER, TE_PROCESS_ENTER
from ._simple_button import SimpleButton

from ._simple_sizer import SimpleSizer


class InputWidget(Panel):
    """
    Widget for text input
    """
    _text_input = None
    _callback = None
    _reset = False

    def __init__(self, parent,  callback, text_button:str, initial:str="", reset:bool=False) -> None:
        super().__init__(parent)
        self._reset = reset
        self._callback = callback

        with SimpleSizer(self, HORIZONTAL) as sizer:
            self._text_input = TextCtrl(self, size=(400, 20), style=TE_PROCESS_ENTER)
            self._text_input.SetValue(initial)
            self._text_input.Bind(EVT_TEXT_ENTER, self.button_callback)
            sizer.Add(self._text_input, 1, flag=TOP, border=1)

            button = SimpleButton(parent=self, callback=self.button_callback, text_button=text_button, size=(200, 22))

            sizer.Add(button)

    def button_callback(self, event):
        """
        Receive event after text input, and pass text to callback function
        :param event: Event
        :return: None
        """
        self._callback(self._text_input.GetValue())
        if self._reset:
            self._text_input.SetValue("")
