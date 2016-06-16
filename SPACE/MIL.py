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
# MIL Bus Simulation                                                          *
#******************************************************************************
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import SPACE.IF

###########
# classes #
###########

# =============================================================================
class MILbusImpl(SPACE.IF.MILbus):
  """Implementation of the MIL Bus"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    """Initialise attributes only"""
    pass
  # ---------------------------------------------------------------------------
  def bcWriteSubAddress(self, rtAddress, subAddress, data):
    """
    Bus Controller: writes data to a sub-address
    implementation of SPACE.IF.MILbus.bcWriteSubAddress
    """
    pass
  # ---------------------------------------------------------------------------
  def bcReadSubAddress(self, rtAddress, subAddress):
    """
    Bus Controller: reads data from a sub-address
    implementation of SPACE.IF.MILbus.bcReadSubAddress
    """
    pass
  # ---------------------------------------------------------------------------
  def bcDatablockDistribtionRequest(self, rtAddress, dataBlock):
    """
    Bus Controller: initiate a datablock distribution
    implementation of SPACE.IF.MILbus.bcDatablockDistribtionRequest
    """
    pass
  # ---------------------------------------------------------------------------
  def rtWriteSubAddress(self, rtAddress, subAddress, data):
    """
    Remote Terminal: writes data to a sub-address
    implementation of SPACE.IF.MILbus.rtWriteSubAddress
    """
    pass
  # ---------------------------------------------------------------------------
  def rtReadSubAddress(self, rtAddress, subAddress):
    """
    Remote Terminal: reads data from a sub-address
    implementation of SPACE.IF.MILbus.rtReadSubAddress
    """
    pass
  # ---------------------------------------------------------------------------
  def rtDatablockAcquisitionRequest(self, rtAddress, dataBlock):
    """
    Remote Terminal: initiate a datablock acquisition
    implementation of SPACE.IF.MILbus.rtDatablockAcquisitionRequest
    """
    pass

# =============================================================================
class MILbusControllerImpl(SPACE.IF.MILbusController):
  """Implementation of the MIL Bus Controller"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    """Initialise attributes only"""
    pass
  # ---------------------------------------------------------------------------
  def processTCpacket(self, tcPacketDu):
    """
    consumes a telecommand C&C packet from the CCS
    implementation of SPACE.IF.MILbusController.processTCpacket
    """
    # shall return True for successful processing, otherwise False
    return False
  # ---------------------------------------------------------------------------
  def notifyWriteSubAddress(self, rtAddress, subAddress, data):
    """
    A Remote Terminal has writen data to a sub-address
    implementation of SPACE.IF.MILbusController.notifyWriteSubAddress
    """
    pass
  # ---------------------------------------------------------------------------
  def notifyDatablockAcquisition(self, rtAddress, dataBlock):
    """
    A Remote Terminal has performed a datablock acquisition
    implementation of SPACE.IF.MILbusController.notifyDatablockAcquisition
    """
    pass

# =============================================================================
class MILbusRemoteTerminalsImpl(SPACE.IF.MILbusRemoteTerminals):
  """Implementation of the MIL Bus Remote Terminals"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    """Initialise attributes only"""
    pass
  # ---------------------------------------------------------------------------
  def processTCpacket(self, tcPacketDu):
    """
    consumes a telecommand C&C packet from the CCS
    implementation of SPACE.IF.MILbusRemoteTerminalsImpl.processTCpacket
    """
    # shall return True for successful processing, otherwise False
    return False
  # ---------------------------------------------------------------------------
  def notifyWriteSubAddress(self, rtAddress, subAddress, data):
    """
    The Bus Controller has writen data to a sub-address
    implementation of SPACE.IF.MILbusRemoteTerminals.notifyWriteSubAddress
    """
    pass
  # ---------------------------------------------------------------------------
  def notifyDatablockDistribution(self, rtAddress, dataBlock):
    """
    The Bus Controller has performed a datablock distribution
    implementation of SPACE.IF.MILbusRemoteTerminals.notifyDatablockDistribution
    """
    pass

#############
# functions #
#############
def init():
  # initialise singleton(s)
  SPACE.IF.s_milBus = MILbusImpl()
  SPACE.IF.s_milBusController = MILbusControllerImpl()
  SPACE.IF.s_milBusRemoteTerminals = MILbusRemoteTerminalsImpl()