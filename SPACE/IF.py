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
# Space Simulation - Space Interface                                          *
#******************************************************************************
import string
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import CCSDS.PACKET
import UTIL.SYS

#############
# constants #
#############
ENABLE_ACK = 0
ENABLE_NAK = 1
DISABLE_ACK = 2
ACK_STRS = ["ENABLE_ACK", "ENABLE_NAK", "DISABLE_ACK"]
RPLY_PKT = 0     # replay file TM packet entry
RPLY_RAWPKT = 1  # replay file raw TM packet entry
RPLY_SLEEP = 2   # replay file sleep entry
RPLY_OBT = 3     # replay file onboard time entry
RPLY_ERT = 4     # replay file earth reception time entry
MIL_BUS_PF = 0   # MIL Platform Bus
MIL_BUS_PL = 1   # MIL Payload Bus

###########
# classes #
###########
# =============================================================================
class Configuration(object):
  """Configuration"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    """Initialise the connection relevant informations"""
    self.connected = False
    self.tmPacketData = None
    self.sendCyclic = False
    self.cyclicPeriodMs = int(UTIL.SYS.s_configuration.TM_CYCLIC_PERIOD_MS)
    self.obcAck1 = ENABLE_ACK
    self.obcAck2 = ENABLE_ACK
    self.obcAck3 = ENABLE_ACK
    self.obcAck4 = ENABLE_ACK
    self.obqAck1 = ENABLE_ACK
    self.obqAck2 = ENABLE_ACK
    self.obqAck3 = ENABLE_ACK
    self.obqAck4 = ENABLE_ACK
  # ---------------------------------------------------------------------------
  def dump(self):
    """Dumps the status of the configuration attributes"""
    LOG_INFO("Space segment configuration", "SPACE")
    LOG("Connected = " + str(self.connected), "SPACE")
    if self.tmPacketData == None:
      LOG("No packet defined", "SPACE")
    else:
      LOG("Packet = " + self.tmPacketData.pktName, "SPACE")
      LOG("SPID = " + str(self.tmPacketData.pktSPID), "SPACE")
      LOG("Parameters and values = " + str(self.tmPacketData.parameterValuesList), "SPACE")
    LOG("Send cyclic TM = " + str(self.sendCyclic), "SPACE")
    LOG("TC Ack 1 = " + ACK_STRS[self.obcAck1], "SPACE")
    LOG("TC Ack 2 = " + ACK_STRS[self.obcAck2], "SPACE")
    LOG("TC Ack 3 = " + ACK_STRS[self.obcAck3], "SPACE")
    LOG("TC Ack 4 = " + ACK_STRS[self.obcAck4], "SPACE")
    LOG_INFO("Onboard queue configuration", "OBQ")
    LOG("TC Ack 1 = " + ACK_STRS[self.obqAck1], "OBQ")
    LOG("TC Ack 2 = " + ACK_STRS[self.obqAck2], "OBQ")
    LOG("TC Ack 3 = " + ACK_STRS[self.obqAck3], "OBQ")
    LOG("TC Ack 4 = " + ACK_STRS[self.obqAck4], "OBQ")

# =============================================================================
class TMparamToPkt(object):
  """Contains the data for a single raw value extraction"""
  # ---------------------------------------------------------------------------
  def __init__(self, paramDef, pktDef, plfRecord):
    self.paramDef = paramDef
    self.paramName = plfRecord.plfName
    self.pktDef = pktDef
    self.pktSPID = plfRecord.plfSPID
    self.locOffby = plfRecord.plfOffby
    self.locOffbi =  plfRecord.plfOffbi
    # fields could be empty
    if plfRecord.plfNbocc == "":
      self.locNbocc = 1
    else:
      self.locNbocc = int(plfRecord.plfNbocc)
    if plfRecord.plfLgocc == "":
      self.locLgocc = 0
    else:
      self.locLgocc = int(plfRecord.plfLgocc)
  # ---------------------------------------------------------------------------
  def __str__(self):
    """string representation"""
    retVal = "\n"
    retVal += "   paramName = " + str(self.paramName) + "\n"
    retVal += "   pktSPID = " + str(self.pktSPID) + "\n"
    retVal += "   locOffby = " + str(self.locOffby) + "\n"
    retVal += "   locOffbi = " + str(self.locOffbi) + "\n"
    retVal += "   locNbocc = " + str(self.locNbocc) + "\n"
    retVal += "   locLgocc = " + str(self.locLgocc) + "\n"
    return retVal

# =============================================================================
class TMparamExtraction(object):
  """Defines a dedicated parameter extraction in a packet"""
  # ---------------------------------------------------------------------------
  def __init__(self, bitPos, bitWidth, name, descr, isInteger, piValue=False):
    self.bitPos = bitPos
    self.bitWidth = bitWidth
    self.name = name
    self.descr = descr
    self.isInteger = isInteger
    self.piValue = piValue
  # ---------------------------------------------------------------------------
  def __cmp__(self, other):
    """supports sorting by packet location"""
    if other == None:
      return 1
    if self.bitPos > other.bitPos:
      return 1
    if self.bitPos < other.bitPos:
      return -1
    return 0

# =============================================================================
class TMpktDef(object):
  """Contains the most important definition data of a TM packet"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    self.pktSPID = None
    self.pktName = None
    self.pktDescr = None
    self.pktAPID = None
    self.pktType = None
    self.pktSType = None
    self.pktDFHsize = None
    self.pktHasDFhdr = None
    self.pktCheck = None
    self.pktPI1off = None
    self.pktPI1wid = None
    self.pktPI1val = None
    self.pktPI2off = None
    self.pktPI2wid = None
    self.pktPI2val = None
    self.pktSPsize = None
    self.pktS2Ksize = None
    self.pktSPDFsize = None
    self.pktSPDFdataSize = None
    self.paramLinks = None
  # ---------------------------------------------------------------------------
  def __cmp__(self, other):
    """supports sorting by SPID"""
    if other == None:
      return 1
    if self.pktSPID > other.pktSPID:
      return 1
    if self.pktSPID < other.pktSPID:
      return -1
    return 0
  # ---------------------------------------------------------------------------
  def appendParamLink(self, paramToPacket):
    """used to append later on links to related parameters"""
    paramName = paramToPacket.paramName
    self.paramLinks[paramName] = paramToPacket
  # ---------------------------------------------------------------------------
  def rangeOverlap(self, bitPos1, bitWidth1, bitPos2, bitWidth2):
    """checks if two ranges overlap"""
    if bitPos1 == None or bitPos2 == None:
      return False
    nextBitPos1 = bitPos1 + bitWidth1
    nextBitPos2 = bitPos2 + bitWidth2
    return (nextBitPos1 > bitPos2 and nextBitPos2 > bitPos1)
  # ---------------------------------------------------------------------------
  def getParamExtraction(self, paramName):
    """returns a parameter extraction of a related parameters"""
    if paramName not in self.paramLinks:
      return None
    paramToPacket = self.paramLinks[paramName]
    paramDef = paramToPacket.paramDef
    paramDescr = paramDef.paramDescr
    isInteger = paramDef.isInteger()
    pktSPID = paramToPacket.pktSPID
    locOffby = paramToPacket.locOffby
    locOffbi =  paramToPacket.locOffbi
    locNbocc = paramToPacket.locNbocc
    locLgocc = paramToPacket.locLgocc
    try:
      bitWidth = paramDef.getBitWidth()
    except Exception, ex:
      LOG_WARNING("param " + paramName + ": " + str(ex) + " ---> ignored", "SPACE")
      return None
    bitStartPos = locOffbi + (locOffby * 8)
    # check if a parameter commutation is qualified
    nameElements = paramName.split("#")
    if len(nameElements) == 1:
      # normal parameter
      paramExtraction = TMparamExtraction(bitStartPos, bitWidth, paramName, paramDescr, isInteger)
    else:
      # supercommutated parameter
      commutation = int(nameElements[1])
      if commutation < 1:
        LOG_WARNING("param " + nameElements[0] + " has invalid commutation " + nameElements[1], "SPACE")
        return None
      bitPos = bitStartPos + (locLgocc * (commutation - 1))
      paramExtraction = TMparamExtraction(bitPos, bitWidth, fieldName, paramDescr, isInteger)
    return paramExtraction
  # ---------------------------------------------------------------------------
  def getParamExtractions(self):
    """returns all parameter extractions, ordered by packet location"""
    retVal = []
    # insert PI1 and PI2 (if defined)
    pi1BitPos = None
    pi1BitWidth = None
    if self.pktPI1val != None:
      pi1BitPos = self.pktPI1off * 8
      pi1BitWidth = self.pktPI1wid
      pi1ValueName = self.pktName + "_PI1VAL"
      pi1ValueDescr = "PI1 Value"
      paramExtraction = TMparamExtraction(pi1BitPos, pi1BitWidth, pi1ValueName, pi1ValueDescr, True, True)
      retVal.append(paramExtraction)
    pi2BitPos = None
    pi2BitWidth = None
    if self.pktPI2val != None:
      pi2BitPos = self.pktPI2off * 8
      pi2BitWidth = self.pktPI2wid
      if self.rangeOverlap(pi1BitPos, pi1BitWidth, pi2BitPos, pi2BitWidth):
        LOG_WARNING("PI1 and PI2 overlap ---> PI2 ignored", "SPACE")
      else:
        pi2ValueName = self.pktName + "_PI2VAL"
        pi2ValueDescr = "PI2 Value"
        paramExtraction = TMparamExtraction(pi2BitPos, pi2BitWidth, pi2ValueName, pi2ValueDescr, True, True)
        retVal.append(paramExtraction)
    # insert other parameters
    for paramName, paramToPacket in self.paramLinks.iteritems():
      paramDef = paramToPacket.paramDef
      paramDescr = paramDef.paramDescr
      isInteger = paramDef.isInteger()
      pktSPID = paramToPacket.pktSPID
      locOffby = paramToPacket.locOffby
      locOffbi =  paramToPacket.locOffbi
      locNbocc = paramToPacket.locNbocc
      locLgocc = paramToPacket.locLgocc
      # ignore exceptions in getBitWidth
      try:
        bitWidth = paramDef.getBitWidth()
      except Exception, ex:
        LOG_WARNING("param " + paramName + ": " + str(ex) + " ---> ignored", "SPACE")
        continue
      bitStartPos = locOffbi + (locOffby * 8)
      if paramToPacket.locNbocc == 1:
        # single location of the parameter in the packet
        if self.rangeOverlap(pi1BitPos, pi1BitWidth, bitStartPos, bitWidth):
          LOG_WARNING("param " + paramName + " overlaps PI1 ---> ignored", "SPACE")
          continue
        if self.rangeOverlap(pi2BitPos, pi2BitWidth, bitStartPos, bitWidth):
          LOG_WARNING("param " + paramName + " overlaps PI2 ---> ignored", "SPACE")
          continue
        paramExtraction = TMparamExtraction(bitStartPos, bitWidth, paramName, paramDescr, isInteger)
        retVal.append(paramExtraction)
      else:
        # supercommutated parameter
        for i in range(paramToPacket.locNbocc):
          fieldName = paramDef.getCommutatedParamName(i)
          bitPos = bitStartPos + (locLgocc * i)
          if self.rangeOverlap(pi1BitPos, pi1BitWidth, bitPos, bitWidth):
            LOG_WARNING("param " + fieldName + " overlaps PI1 ---> ignored", "SPACE")
            continue
          if self.rangeOverlap(pi2BitPos, pi2BitWidth, bitPos, bitWidth):
            LOG_WARNING("param " + fieldName + " overlaps PI2 ---> ignored", "SPACE")
            continue
          paramExtraction = TMparamExtraction(bitPos, bitWidth, fieldName, paramDescr, isInteger)
          retVal.append(paramExtraction)
    retVal.sort()
    return retVal
  # ---------------------------------------------------------------------------
  def __str__(self):
    """string representation"""
    retVal = "\n"
    retVal += " pktSPID = " + str(self.pktSPID) + "\n"
    retVal += " pktName = " + str(self.pktName) + "\n"
    retVal += " pktDescr = " + str(self.pktDescr) + "\n"
    retVal += " pktAPID = " + str(self.pktAPID) + "\n"
    retVal += " pktType = " + str(self.pktType) + "\n"
    retVal += " pktSType = " + str(self.pktSType) + "\n"
    retVal += " pktDFHsize = " + str(self.pktDFHsize) + "\n"
    retVal += " pktHasDFhdr = " + str(self.pktHasDFhdr) + "\n"
    retVal += " pktCheck = " + str(self.pktCheck) + "\n"
    retVal += " pktPI1off = " + str(self.pktPI1off) + "\n"
    retVal += " pktPI1wid = " + str(self.pktPI1wid) + "\n"
    retVal += " pktPI1val = " + str(self.pktPI1val) + "\n"
    retVal += " pktPI2off = " + str(self.pktPI2off) + "\n"
    retVal += " pktPI2wid = " + str(self.pktPI2wid) + "\n"
    retVal += " pktPI2val = " + str(self.pktPI2val) + "\n"
    retVal += " pktSPsize = " + str(self.pktSPsize) + "\n"
    retVal += " pktS2Ksize = " + str(self.pktS2Ksize) + "\n"
    retVal += " pktSPDFsize = " + str(self.pktSPDFsize) + "\n"
    retVal += " pktSPDFdataSize = " + str(self.pktSPDFsize) + "\n"
    retVal += " paramLinks =\n"
    for paramToPacket in self.paramLinks.values():
      retVal += "  paramToPacket = " + str(paramToPacket)
    return retVal

# =============================================================================
class TMparamDef(object):
  """Contains the most important definition data of a TM parameter"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    self.paramName = None
    self.paramDescr = None
    self.paramPtc = None
    self.paramPfc = None
    self.minCommutations = None
    self.maxCommutations = None
  # ---------------------------------------------------------------------------
  def __cmp__(self, other):
    """supports sorting by paramName"""
    if other == None:
      return 1
    if self.paramName > other.paramName:
      return 1
    if self.paramName < other.paramName:
      return -1
    return 0
  # ---------------------------------------------------------------------------
  def getCommutatedParamName(self, commutation):
    """returns the commutated param name"""
    return self.paramName + '_' + ("%04d" % commutation)
  # ---------------------------------------------------------------------------
  def isInteger(self):
    """tells if the parameter is signed or unsigned integer"""
    if (self.paramPtc <= 4) or (self.paramPtc == 6):
      return True
    return False
  # ---------------------------------------------------------------------------
  def getBitWidth(self):
    if self.paramPtc == 1:
      if self.paramPfc == 0:
        # unsigned integer (boolean parameter)
        return 1
    elif self.paramPtc == 2:
      if self.paramPfc <= 32:
        # unsigned integer (enumeration parameter)
        return self.paramPfc
    elif self.paramPtc == 3:
      # unsigned integer
      if self.paramPfc <= 12:
        return self.paramPfc + 4
      elif self.paramPfc == 13:
        return 24
      elif self.paramPfc == 14:
        return 32
      elif self.paramPfc == 15:
        # not supported by SCOS-2000
        return 48
      elif self.paramPfc == 16:
        # not supported by SCOS-2000
        return 64
    elif self.paramPtc == 4:
      # signed integer
      if self.paramPfc <= 12:
        return self.paramPfc + 4
      elif self.paramPfc == 13:
        return 24
      elif self.paramPfc == 14:
        return 32
      elif self.paramPfc == 15:
        # not supported by SCOS-2000
        return 48
      elif self.paramPfc == 16:
        # not supported by SCOS-2000
        return 64
    elif self.paramPtc == 5:
      # floating point
      if self.paramPfc == 1:
        # simple precision real (IEEE)
        return 32
      elif self.paramPfc == 2:
        # double precision real (IEEE)
        return 64
      elif self.paramPfc == 3:
        # simple precision real (MIL 1750A)
        return 32
      elif self.paramPfc == 4:
        # extended precision real (MIL 1750a)
        return 48
    elif self.paramPtc == 6:
      # bit string
      if self.paramPfc == 0:
        # variable bit string, not supported by SCOS-2000
        pass
      elif self.paramPfc <= 32:
        # fixed length bit strings, unsigned integer in SCOS-2000
        return self.paramPfc
    elif self.paramPtc == 7:
      # octet string
      if self.paramPfc == 0:
        # variable octet string, not supported by SCOS-2000 TM
        pass
      else:
        # fixed length octet strings
        return self.paramPfc * 8
    elif self.paramPtc == 8:
      # ASCII string
      if self.paramPfc == 0:
        # variable ASCII string, not supported by SCOS-2000 TM
        pass
      else:
        # fixed length ASCII strings
        return self.paramPfc * 8
    elif self.paramPtc == 9:
      # absolute time
      if self.paramPfc == 0:
        # variable length, not supported by SCOS-2000 TM
        pass
      elif self.paramPfc == 1:
        # CDS format, without microseconds
        return 48
      elif self.paramPfc == 2:
        # CDS format, with microseconds
        return 64
      elif self.paramPfc <= 6:
        # CUC format, 1st octet coarse time, 2nd - n-th octet for fine time
        return (self.paramPfc - 2) * 8
      elif self.paramPfc <= 10:
        # CUC format, 1st & 2nd octet coarse time, 3rd - n-th octet for fine time
        return (self.paramPfc - 5) * 8
      elif self.paramPfc <= 14:
        # CUC format, 1st - 3rd octet coarse time, 4rd - n-th octet for fine time
        return (self.paramPfc - 8) * 8
      elif self.paramPfc <= 18:
        # CUC format, 1st - 4th octet coarse time, 5rd - n-th octet for fine time
        return (self.paramPfc - 11) * 8
    elif self.paramPtc == 10:
      # relative time
      if self.paramPfc <= 2:
        # not used
        pass
      elif self.paramPfc <= 6:
        # CUC format, 1st octet coarse time, 2nd - n-th octet for fine time
        return (self.paramPfc - 2) * 8
      elif self.paramPfc <= 10:
        # CUC format, 1st & 2nd octet coarse time, 3rd - n-th octet for fine time
        return (self.paramPfc - 5) * 8
      elif self.paramPfc <= 14:
        # CUC format, 1st - 3rd octet coarse time, 4rd - n-th octet for fine time
        return (self.paramPfc - 8) * 8
      elif self.paramPfc <= 18:
        # CUC format, 1st - 4th octet coarse time, 5rd - n-th octet for fine time
        return (self.paramPfc - 11) * 8
    elif self.paramPtc == 11:
      # deduced parameter, N/A
      pass
    elif self.paramPtc == 13:
      # saved synthetic parameter, N/A
      pass
    # illegal ptc/pfc combination
    raise Exception("ptc/pfc combination " + str(self.paramPtc) + "/" + str(self.paramPfc) + " not supported")
  # ---------------------------------------------------------------------------
  def __str__(self):
    """string representation"""
    retVal = "\n"
    retVal += " paramName = " + str(self.paramName) + "\n"
    retVal += " paramDescr = " + str(self.paramDescr) + "\n"
    retVal += " paramPtc = " + str(self.paramPtc) + "\n"
    retVal += " paramPfc = " + str(self.paramPfc) + "\n"
    # These lines have been commented due to problems with pickling and
    # unpickling (errornous unpickling of the whole definition data).
    # This backward reference from parameters to packets is not needed
    # in the existing implementation.
    #retVal += " pktLinks =\n"
    #for paramToPacket in self.pktLinks.values():
    #  retVal += "  paramToPacket = " + str(paramToPacket)
    retVal += " minCommutations = " + str(self.minCommutations) + "\n"
    retVal += " maxCommutations = " + str(self.maxCommutations) + "\n"
    return retVal

# =============================================================================
class TMpacketInjectData(object):
  """Data of a TM packet that can be injected"""
  # ---------------------------------------------------------------------------
  def __init__(self,
               pktSPID,
               pktMnemonic,
               params,
               values,
               dataField,
               segmentationFlags):
    """Initialisation with default data"""
    self.pktName = pktMnemonic.upper()
    self.pktSPID = pktSPID
    self.parameterValuesList = []
    self.dataField = dataField
    self.segmentationFlags = segmentationFlags
    if params == "" or values == "":
      return
    # there are parameter-names and parameter-values
    paramsLst = string.split(params, ",")
    valuesLst = string.split(values, ",")
    # both parts must match
    if len(paramsLst) != len(valuesLst):
      LOG_WARNING("parameter-names or parameter-values have different size")
      return
    # create the return list
    for i in range(len(valuesLst)):
      param = paramsLst[i].strip().strip("{").strip("}").upper()
      value = valuesLst[i].strip().strip("{").strip("}")
      if (len(param) > 0) and (len(value) > 0):
        self.parameterValuesList.append([param,value])

##############
# interfaces #
##############
# =============================================================================
class Definitions(object):
  """Interface for definition data"""
  # ---------------------------------------------------------------------------
  def createDefinitions(self):
    """creates the definition data"""
    pass
  # ---------------------------------------------------------------------------
  def initDefinitions(self):
    """initialise the definition data from file or MIB"""
    pass
  # ---------------------------------------------------------------------------
  def getTMpktDefByIndex(self, index):
    """returns a TM packet definition"""
    pass
  # ---------------------------------------------------------------------------
  def getTMpktDefBySPID(self, spid):
    """returns a TM packet definition"""
    pass
  # ---------------------------------------------------------------------------
  def getSPIDbyPktName(self, name):
    """returns the packet SPID for a packet name"""
    pass
  # ---------------------------------------------------------------------------
  def getTMpktDefs(self):
    """returns the TM packet definitions"""
    pass
  # ---------------------------------------------------------------------------
  def getTMparamDefs(self):
    """returns the TM parameter definitions"""
    pass
  # ---------------------------------------------------------------------------
  def getTMpacketInjectData(self,
                            pktMnemonic,
                            params,
                            values,
                            dataField=None,
                            segmentationFlags=CCSDS.PACKET.UNSEGMENTED):
    """returns the data that are used for packet injection"""
    pass
  # ---------------------------------------------------------------------------
  def getTMpacketInjectDataBySPID(self,
                                  spid,
                                  params,
                                  values,
                                  dataField=None,
                                  segmentationFlags=CCSDS.PACKET.UNSEGMENTED):
    """returns the data that are used for packet injection"""
    pass

# =============================================================================
class OnboardComputer(object):
  """Interface of the onboard computer"""
  # ---------------------------------------------------------------------------
  def pushTCpacket(self, tcPacketDu):
    """consumes a telecommand packet from the uplink"""
    # shall return True for successful processing, otherwise False
    return True
  # ---------------------------------------------------------------------------
  def processTCpacket(self, tcPacketDu, ack1, ack2, ack3, ack4):
    """processes a telecommand packet"""
    # shall return True for successful processing, otherwise False
    return True
  # ---------------------------------------------------------------------------
  def generateEmptyTMpacket(self, pktMnemonic):
    """generates an empty TM packet (all parameters are zero)"""
    # shall return True for successful processing, otherwise False
    return True
  # ---------------------------------------------------------------------------
  def generateEmptyTMpacketBySPID(self, spid):
    """generates an empty TM packet (all parameters are zero)"""
    # shall return True for successful processing, otherwise False
    return True
  # ---------------------------------------------------------------------------
  def generateTMpacket(self, tmPacketData, obtUTC=None, ertUTC=None):
    """generates a TM packet"""
    # shall return True for successful processing, otherwise False
    return True
  # ---------------------------------------------------------------------------
  def generateAcksFromTCpacket(self, tcPacketDu, ack1, ack2, ack3, ack4):
    """generates TC acknowledgements according to PUS service 1"""
    # shall return True for successful processing, otherwise False
    return True
  # ---------------------------------------------------------------------------
  def generateAck(self, tcAPID, tcSSC, ackType):
    """generates a TC acknowledgement according to PUS service 1"""
    # shall return True for successful processing, otherwise False
    return True
  # ---------------------------------------------------------------------------
  def pushTMpacket(self, tmPacketDu, ertUTC):
    """sends TM packet DU to CCS or downlink"""
    # shall return True for successful processing, otherwise False
    return True
  # ---------------------------------------------------------------------------
  def replayPackets(self, replayFileName):
    """sends TM packet from a replay file"""
    pass
  # ---------------------------------------------------------------------------
  def startCyclicTM(self):
    """start sending of cyclic TM"""
    pass
  # ---------------------------------------------------------------------------
  def stopCyclicTM(self):
    """stops sending of cyclic TM"""
    pass

# =============================================================================
class OnboardQueue(object):
  """Interface of the onboard queue"""
  # ---------------------------------------------------------------------------
  def getQueue(self):
    """returns the onboard queue"""
    pass
  # ---------------------------------------------------------------------------
  def pushMngPacket(self, tcPacketDu):
    """consumes a management telecommand packet"""
    pass
  # ---------------------------------------------------------------------------
  def pushExecPacket(self, tcPacketDu):
    """consumes a telecommand packet that shall be executed immediately"""

# =============================================================================
class ApplicationSoftware(object):
  """Interface of the spacecraft's application software"""
  # ---------------------------------------------------------------------------
  def processTCpacket(self, tcPacketDu):
    """processes a telecommand C&C packet from the CCS"""
    # shall return True for successful processing, otherwise False
    return True
  # ---------------------------------------------------------------------------
  # shall be overloaded in derived classes
  def getBcPfAPID(self):
    pass
  def getBcPlAPID(self):
    pass
  def getRtPfAPID(self):
    pass
  def getRtPlAPID(self):
    pass
  # ---------------------------------------------------------------------------
  def notifyMILdatablockDistribution(self, rtAddress, dataBlock):
    """The mRT has received on the MIL Bus a data block from the BC"""
    pass
  # ---------------------------------------------------------------------------
  def notifyMILdatablockAcquisition(self, rtAddress, dataBlock):
    """The BC has received on the MIL Bus a data block from a RT"""
    pass
  # ---------------------------------------------------------------------------
  def notifyMILdatablockDistribution(self, rtAddress, dataBlock):
    """The mRT has received on the MIL Bus a data block from the BC"""
    pass

# =============================================================================
class TMpacketGenerator(object):
  """Interface of the generator for telemetry packets"""
  # ---------------------------------------------------------------------------
  def getIdlePacket(self, packetSize):
    """
    creates an idle packet for filling space in a parent container
    (e.g. a CCSDS TM frame)
    """
    pass
  # ---------------------------------------------------------------------------
  def getTMpacket(self,
                  spid,
                  parameterValues=[],
                  dataField=None,
                  segmentationFlags=CCSDS.PACKET.UNSEGMENTED,
                  obtTimeStamp=None,
                  reuse=True):
    """creates a CCSDS TM packet with optional parameter values"""
    pass

# =============================================================================
class TMpacketReplayer(object):
  """Interface of the replayer for telemetry packets"""
  # ---------------------------------------------------------------------------
  def readReplayFile(self, replayFileName):
    """
    reads TM packets and directives from a replay file
    """
    pass
  # ---------------------------------------------------------------------------
  def getItems(self):
    """returns items from the replay list"""
    pass
  # ---------------------------------------------------------------------------
  def getNextItem(self):
    """returns next item from the replay list or None"""
    pass

# =============================================================================
class MILbus(object):
  """Interface of the MIL Bus"""
  # ---------------------------------------------------------------------------
  def bcWriteSubAddress(self, rtAddress, subAddress, data):
    """Bus Controller: writes data to a sub-address"""
    pass
  # ---------------------------------------------------------------------------
  def bcReadSubAddress(self, rtAddress, subAddress):
    """Bus Controller: reads data from a sub-address"""
    pass
  # ---------------------------------------------------------------------------
  def bcDatablockDistribtionRequest(self, rtAddress, dataBlock):
    """Bus Controller: initiate a datablock distribution"""
    pass
  # ---------------------------------------------------------------------------
  def rtWriteSubAddress(self, rtAddress, subAddress, data):
    """Remote Terminal: writes data to a sub-address"""
    pass
  # ---------------------------------------------------------------------------
  def rtReadSubAddress(self, rtAddress, subAddress):
    """Remote Terminal: reads data from a sub-address"""
    pass
  # ---------------------------------------------------------------------------
  def rtDatablockAcquisitionRequest(self, rtAddress, dataBlock):
    """Remote Terminal: initiate a datablock acquisition"""
    pass

# =============================================================================
class MILbusController(object):
  """Interface of the MIL Bus Controller"""
  # ---------------------------------------------------------------------------
  # external methods that are invoked via telecommands,
  # shall return True for successful processing, otherwise False
  def identify(self, bus):
    return True
  def selfTest(self, bus):
    return True
  def getSelfTestReport(self, bus):
    return True
  def reset(self, bus):
    return True
  def configure(self, bus):
    return True
  def configureFrame(self, bus):
    return True
  def addInterrogation(self, bus):
    return True
  def discover(self, bus):
    return True
  def setupDistDatablock(self, bus):
    return True
  def start(self, bus):
    return True
  def stop(self, bus):
    return True
  def forceFrameSwitch(self, bus):
    return True
  def send(self, bus):
    return True
  def setData(self, bus):
    return True
  def forceBusSwitch(self, bus):
    return True
  def injectError(self, bus):
    return True
  def clearError(self, bus):
    return True
  def activate(self, bus):
    return True
  def deactivate(self, bus):
    return True
  def dtd(self, bus):
    return True
  # ---------------------------------------------------------------------------
  def notifyWriteSubAddress(self, rtAddress, subAddress, data):
    """A Remote Terminal has writen data to a sub-address"""
    pass
  # ---------------------------------------------------------------------------
  def notifyDatablockAcquisition(self, rtAddress, dataBlock):
    """A Remote Terminal has performed a datablock acquisition"""
    pass

# =============================================================================
class MILbusRemoteTerminals(object):
  """Interface of the MIL Bus Remote Terminals"""
  # ---------------------------------------------------------------------------
  # external methods that are invoked via telecommands,
  # shall return True for successful processing, otherwise False
  def identify(self, bus):
    return True
  def selfTest(self, bus):
    return True
  def getSelfTestReport(self, bus):
    return True
  def configure(self, bus):
    return True
  def addResponse(self, bus):
    return True
  def reset(self, bus):
    return True
  def saEnable(self, bus):
    return True
  def setupAcquDatablock(self, bus):
    return True
  def start(self, bus):
    return True
  def stop(self, bus):
    return True
  def injectError(self, bus):
    return True
  def clearError(self, bus):
    return True
  def activate(self, bus):
    return True
  def deactivate(self, bus):
    return True
  def atr(self, bus):
    return True
  # ---------------------------------------------------------------------------
  def notifyWriteSubAddress(self, rtAddress, subAddress, data):
    """The Bus Controller has writen data to a sub-address"""
    pass
  # ---------------------------------------------------------------------------
  def notifyDatablockDistribution(self, rtAddress, dataBlock):
    """The Bus Controller has performed a datablock distribution"""
    pass

####################
# global variables #
####################
# to force behaviour for testing
s_testMode = 0
# configuration is a singleton
s_configuration = None
# definitions is a singleton
s_definitions = None
# onboard computer is a singleton
s_onboardComputer = None
# onboard queue is a singleton
s_onboardQueue = None
# application software is a singleton
s_applicationSoftware = None
# telemetry packet generator is a singleton
s_tmPacketGenerator = None
# telemetry packet replayer is a singelton
s_tmPacketReplayer = None
# MIL Bus is a singelton
s_milBus = None
# MIL Bus Controller is a singelton
s_milBusController = None
# MIL Bus Remote Terminals is a singelton
s_milBusRemoteTerminals = None
