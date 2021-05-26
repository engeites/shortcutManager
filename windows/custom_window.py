from loader import sg, BG_COLOR, TXT_COLOR


class MyWindow(sg.Window):
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
