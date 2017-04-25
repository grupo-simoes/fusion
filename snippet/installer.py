import os
from pywinauto.application import Application as app

fsv = app.Start("FSViewerSetup46.exe")

fsv.InstallDialog.NextButton.Wait('ready', timeout=30).ClickInput()
fsv.InstallDialog.IAgreeRadioButton.Wait('ready', timeout=30).ClickInput()
fsv.InstallDialog.Edit.Wait('ready', timeout=30).TypeKeys(os.getcwd() + "\FastStone Image Viewer", with_spaces=True)
fsv.InstallDialog.InstallButton.Wait('ready', timeout=30).ClickInput()
fsv.InstallDialog.FinishButton.Wait('ready', timeout=30).ClickInput()lsls
