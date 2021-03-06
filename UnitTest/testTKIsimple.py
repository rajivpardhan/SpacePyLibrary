#!/usr/bin/env python
#******************************************************************************
# (C) 2016, Stefan Korner, Austria                                            *
#                                                                             *
# The Space Python Library is free software; you can redistribute it and/or   *
# modify it under the terms of the GNU Lesser General Public License as       *
# published by the Free Software Foundation; either version 2.1 of the        *
# License, or (at your option) any later version.                             *
#                                                                             *
# The Space Python Library is distributed in the hope that it will be useful, *
# but WITHOUT ANY WARRANTY; without even the implied warranty of              *
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser     *
# General Public License for more details.                                    *
#******************************************************************************
# TASK + TKI framework - Unit Test: empty Model Task with TKinter GUI         *
#******************************************************************************
import Tkinter
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import UI.TKI
import UTIL.TASK

#############
# functions #
#############
# -----------------------------------------------------------------------------
def initConfiguration():
  """initialise the system configuration"""
  UTIL.SYS.s_configuration.setDefaults([
  ["SYS_APP_MNEMO", "GUI"],
  ["SYS_APP_NAME", "Test GUI"],
  ["SYS_APP_VERSION", "1.0"]])

###########
# classes #
###########
# =============================================================================
class GUIview(UI.TKI.GUIwinView):
  """Implementation of the SCOE EGSE GUI layer"""
  # ---------------------------------------------------------------------------
  def __init__(self, master):
    """Initialise all GUI elements"""
    UI.TKI.GUIwinView.__init__(self, master, "GUI", "Test GUI")
    # log messages (default logger)
    self.messageLogger = UI.TKI.MessageLogger(self)
    self.appGrid(self.messageLogger, row=0, columnspan=2)
    # message line
    self.messageline = Tkinter.Message(self, relief=Tkinter.GROOVE)
    self.appGrid(self.messageline,
                 row=1,
                 columnspan=2,
                 rowweight=0,
                 columnweight=0,
                 sticky=Tkinter.EW)
    self.grid(row=0, column=0, sticky=Tkinter.EW+Tkinter.NS)
    self.master.rowconfigure(0, weight=1)
    self.master.columnconfigure(0, weight=1)
  # ---------------------------------------------------------------------------
  def fillCommandMenuItems(self):
    """
    fill the command menu bar,
    implementation of UI.TKI.GUIwinView.fillCommandMenuItems
    """
    pass
  # ---------------------------------------------------------------------------
  def notifyStatus(self, status):
    """Generic callback when something changes in the model"""
    pass

########
# main #
########
if __name__ == "__main__":
  # initialise the system configuration
  initConfiguration()
  # initialise the console handler
  consoleHandler = UTIL.TASK.ConsoleHandler()
  # initialise the model and the GUI
  # keep the order: tasks must exist before the gui views are created
  UI.TKI.createGUI()
  guiTask = UI.TKI.GUItask()
  modelTask = UTIL.TASK.ProcessingTask(isParent=False)
  win0 = UI.TKI.createWindow()
  gui0view = GUIview(win0)
  UI.TKI.finaliseGUIcreation()
  # register the console handler
  modelTask.registerConsoleHandler(consoleHandler)
  # start the tasks
  print "start modelTask..."
  modelTask.start()
  print "start guiTask..."
  guiTask.start()
  print "guiTask terminated"
  modelTask.join()
  print "modelTask terminated"
