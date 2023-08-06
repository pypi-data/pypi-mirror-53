from wx import ID_CANCEL, DirDialog

from wxwidgets._input_widget import InputWidget


class DirectoryInput(InputWidget):
    """
    Simple widget for opening a directory
    """

    def __init__(self, parent, callback, text_button: str, text_title: str, initial: str = "",
                 reset: bool = False) -> None:
        """
        Builds the widget
        :param parent: Parent wx element
        :param callback: Function, that receives the directory
        :param text_button: Text is displayed on the "open-button"
        :param text_title: Text is displayed in the window title
        :param initial: Initial path
        :param reset: If true, don't show last opened directory
        """
        super().__init__(parent=parent, callback=callback, text_button=text_button, initial=initial, reset=reset)
        self._text_title = text_title

    def button_callback(self, event) -> None:
        """
        Receive selection event after directory is selected, and pass to callback function
        :param event: Event contains directory path
        :return: None
        """
        with DirDialog(parent=self, message=self._text_title, defaultPath="") as dialog:
            if dialog.ShowModal() == ID_CANCEL:
                return  # The user changed their mind
            path = dialog.Path

        # Display path
        if self._reset:
            self._text_input.SetValue("")
        else:
            self._text_input.SetValue(path)
        self._callback(path)
