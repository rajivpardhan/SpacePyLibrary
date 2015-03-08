#******************************************************************************
# (C) 2014, Stefan Korner, Austria                                            *
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
# NCTRS TC server                                                             *
#******************************************************************************
import sys
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import GRND.IF, GRND.NCTRS
import SPACE.OBC
import UTIL.SYS, UTIL.TASK

###########
# classes #
###########
# =============================================================================
class TMsender(GRND.NCTRS.TMsender, GRND.IF.TMmcsLink):
  """Subclass of GRND.NCTRS.TMsender and SPACE.OBC.TMsender"""
  # ---------------------------------------------------------------------------
  def __init__(self, portNr, nctrsTMfields):
    """Initialise attributes only"""
    GRND.NCTRS.TMsender.__init__(self, portNr, nctrsTMfields)
  # ---------------------------------------------------------------------------
  def clientAccepted(self):
    """Overloaded from GRND.NCTRS.TMsender"""
    LOG_INFO("NCTRS TM receiver (client) accepted", "GRND")
    # notify the status change
    UTIL.TASK.s_processingTask.setTMconnected()
  # ---------------------------------------------------------------------------
  def pushTMframe(self, tmFrameDu):
    """
    consumes a telemetry frame:
    implementation of GROUND.IF.TMmcsLink.pushTMframe
    """
    self.sendFrame(tmFrameDu.getBufferString())
  # ---------------------------------------------------------------------------
  def notifyError(self, errorMessage, data):
    """error notification"""
    LOG_ERROR(errorMessage)
    try:
      LOG(str(data))
    except Exception, ex:
      LOG_WARNING("data passed to notifyError are invalid: " + str(ex))

#############
# functions #
#############
def createTMsender(hostName=None):
  """create the NCTRS TM sender"""
  nctrsTMfields = GRND.NCTRS.NCTRStmFields()
  nctrsTMfields.spacecraftId = int(UTIL.SYS.s_configuration.SPACECRAFT_ID)
  GRND.IF.s_tmMcsLink = TMsender(
    portNr=int(UTIL.SYS.s_configuration.NCTRS_TM_SERVER_PORT),
    nctrsTMfields=nctrsTMfields)
  if not GRND.IF.s_tmMcsLink.openConnectPort(hostName):
    sys.exit(-1)
