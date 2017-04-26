#!/usr/bin/python

# spreadsheet.py

from wx.lib import sheet
import wx


class MySheet(sheet.CSheet):
    def __init__(self, parent):
        sheet.CSheet.__init__(self, parent)
        self.row = self.col = 0
        self.SetNumberRows(55)
        self.SetNumberCols(25)

        for i in range(55):
            self.SetRowSize(i, 20)

    def OnGridSelectCell(self, event):
        self.row, self.col = event.GetRow(), event.GetCol()
        control = self.GetParent().GetParent().position
        value =  self.GetColLabelValue(self.col) + self.GetRowLabelValue(self.row)
        control.SetValue(value)
        event.Skip()

class Newt(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, -1, title, size = (550, 500))

        box = wx.BoxSizer(wx.VERTICAL)

        notebook = wx.Notebook(self, -1, style=wx.RIGHT)

        sheet1 = MySheet(notebook)
        sheet2 = MySheet(notebook)
        sheet3 = MySheet(notebook)
        sheet1.SetFocus()

        notebook.AddPage(sheet1, 'Sheet1')
        notebook.AddPage(sheet2, 'Sheet2')
        notebook.AddPage(sheet3, 'Sheet3')

        box.Add(notebook, 1, wx.EXPAND)

        self.CreateStatusBar()
        self.Centre()
        self.Show(True)

app = wx.App()
Newt(None, -1, 'SpreadSheet')
app.MainLoop()
