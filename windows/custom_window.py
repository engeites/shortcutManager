from loader import sg, BG_COLOR


class MyWindow(sg.Window):
    """extend_layout method from base PySimpleGUI.Window class behaviour is unsuitable for this project,
     so we have to overload it with this one. Changes are minor, we simply create column variable slightly
     different way (give background_color and element_justification)

     In future main window will be an instance of MyWindow class, not sg.Window. Other windows still
     created the old way"""

    def extend_layout(self, container,  rows):
        """
        Adds new rows to an existing container element inside of this window
        If the container is a scrollable Column, you need to also call the contents_changed() method

        :param container: The container Element the layout will be placed inside of
        :type container: Frame | Column | Tab
        :param rows: The layout to be added
        :type rows: (List[List[Element]])
        :return: (Window) self so could be chained
        :rtype: (Window)
        """
        column = sg.Column(rows, pad=(0,0), background_color=BG_COLOR, element_justification="right")
        if self == container:
            frame = self.TKroot
        elif isinstance(container.Widget, sg.TkScrollableFrame):
            frame = container.Widget.TKFrame
        else:
            frame = container.Widget
        sg.PackFormIntoFrame(column, frame, self)
        # sg.PackFormIntoFrame(col, window.TKroot, window)
        self.AddRow(column)
        self.AllKeysDict = self._BuildKeyDictForWindow(self, column, self.AllKeysDict)
        return self
