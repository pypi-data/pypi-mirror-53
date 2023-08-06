#!/usr/bin/env python
'''
This file contains the core functions for the drive test suite.
Functions are placed here for the core setup functions called during the init stage of a test (or CSV parsed test set)


########### VERSION HISTORY ###########

03/01/2019 - Andy Norrie        - First Version

########### INSTRUCTIONS ###########

N/A

####################################
'''

from __future__ import print_function
import sys
import os
import multiprocessing
import pkg_resources
import importlib
from datetime import datetime
import traceback
import xml.etree.ElementTree as cElementTree

from quarchpy.device.scanDevices import *
from quarchpy.device import quarchQPS, quarchDevice

from quarchpy.connection_specific.connection_QPS import QpsInterface

from quarchpy.qps.qpsFuncs import isQpsRunning

from quarchpy.disk_test.testLine import testLine
from quarchpy.disk_test import driveTestConfig
from quarchpy.disk_test.dtsGlobals import dtsGlobals
from quarchpy.disk_test.dtsComms import DTSCommms
from quarchpy.disk_test.hostInformation import HostInformation


# Import zero conf only if available
try:
    import zeroconf
    from zeroconf import ServiceInfo, Zeroconf

    zeroConfAvail = True
except:
    printText("Please install zeroconf using 'pip install zeroconf' ")
    zeroConfAvail = False

myHostInfo = HostInformation()
comms = DTSCommms()


'''
Stores a given string in the test resources dictionary
'''
def storeResourceString(resourceName, resourceValue):
    driveTestConfig.testResources[resourceName] = resourceValue


"""
Checking the user's cmd is with admin privelages
"""

def isUserAdmin():

    if os.name == 'nt':
        import ctypes
        # WARNING: requires Windows XP SP2 or higher!
        try:
            # If == 1, user is running from elevated cmd prompt
            # print(ctypes.windll.shell32.IsUserAnAdmin() == 1)
            return ctypes.windll.shell32.IsUserAnAdmin() == 1
        except:
            traceback.print_exc()
            return False
    elif os.name == 'posix':
        # Check for root on Posix
        return os.getuid() == 0
    else:
        raise RuntimeError("Unsupported operating system for this module: %s" % (os.name,))





'''
Adds a newly defined quarch module to use during the test and stores it as a resource to use later
connection="USB:QTL1743" or "REST:192.168.1.12<7>"
moduleName="myModule1" (unique string to identify the resource later)
'''

def specifyQuarchModule(moduleName, interFaceType = "PY", powerOnDevice = True):
    # allow use to find device, then connect to it
    connection = None

    if "PY" in interFaceType:
        connection = chooseQuarchModule(moduleName)
    elif "QPS" in interFaceType:
        connection = chooseQuarchModuleQPS(moduleName)

    if connection is None:
        print("No item selected, test aborted. Waiting for new test start..")
        return 0

    # If this is an array controller sub module
    strPos = connection.find('<')
    if (strPos != -1):
        print(connection + " : " + moduleName)

        # Get the array part
        arrayConnection = connection[0:strPos]
        # Get the sub module nubmber
        arrayPosition = connection[strPos + 1:]
        arrayPosition = arrayPosition.strip(' >')

        # Create the array controller connection
        myQuarchDevice = quarchDevice(arrayConnection)
        # Promote connection to array type
        myArray = quarchArray(myQuarchDevice)
        # Get access to the sub-device
        mySubDevice = myArray.getSubDevice(arrayPosition)
        moduleResponse = mySubDevice.sendCommand("*TST?")

        # Test the connection
        if (moduleResponse != "OK"):
            notifyTestLogEvent(time.time(), "error", "Quarch module not ready",
                               os.path.basename(__file__) + " - " + sys._getframe().f_code.co_name,
                               {"textDetails": "Module responded: " + moduleResponse})
        else:
            # Add the item to the test resources dictionary
            driveTestConfig.testResources[moduleName] = mySubDevice

    elif "QPS" in interFaceType:

        # Splitting string 'USB::QTL1999-01-001=5v' into connection and output mode
        connection, outputModeValue = connection.split("=")

        # Creating QPS connection with device  --  Uses GUI TCP
        myQuarchDevice = quarchDevice(connection, ConType="QPS:" + dtsGlobals.GUI_TCP_IP + ":9822")

        # Create the device connection, as a QPS connected device
        myQpsDevice = quarchQPS(myQuarchDevice)
        myQpsDevice.openConnection()

        # Add the item to the test resources dictionary
        driveTestConfig.testResources[moduleName] = myQpsDevice

        # Resetting the device prior to stream
        myQuarchDevice.sendCommand("conf:def:state")

        # Making an auto-power up -- Could be changed to specify whether it is to be powered up or not.
        if powerOnDevice:
            powerOnDrive(myQpsDevice, outputMode=outputModeValue)

    else:
        # Create the device connection

        myQuarchDevice = quarchDevice(connection)

        # Test the connection
        moduleResponse = myQuarchDevice.sendCommand("*TST?")
        if (moduleResponse is None or moduleResponse == ""):
            notifyTestLogEvent(time.time(), "error", "Quarch module did not respond",
                               os.path.basename(__file__) + " - " + sys._getframe().f_code.co_name)
            return
        elif (moduleResponse != "OK"):
            notifyTestLogEvent(time.time(), "warning", "Quarch module did not pass self test",
                               os.path.basename(__file__) + " - " + sys._getframe().f_code.co_name,
                               {"textDetails": "Module responded: " + moduleResponse})

        # Add the item to the test resources dictionary
        driveTestConfig.testResources[moduleName] = myQuarchDevice

        # Making an auto-power up -- Could be changed to specify whether it is to be powered up or not.
        if powerOnDevice:
            powerOnDrive(myQuarchDevice)



def powerOnDrive(myQuarchDevice, outputMode = None):
    if outputMode is not None:
        myQuarchDevice.sendCommand("conf:out:mode " + outputMode)
        myQuarchDevice.sendCommand("conf out 12v pull on")

    #print(myQuarchDevice.sendCommand("run:pow?"))
    #print(myQuarchDevice.sendCommand("sig:12v:volt?"))
    powerStatus = myQuarchDevice.sendCommand("run:pow?")
    # hd will reply with off if no power
    if "pulled" in str(powerStatus).lower() or "off" in str(powerStatus).lower():
        myQuarchDevice.sendCommand("run:pow up")


def chooseQuarchModuleQPS(moduleName, myQps = None):

    if not isQpsRunning(dtsGlobals.GUI_TCP_IP):
        comms.sendMsgToGUI("QuarchDTS::StartQPS", None)

    dtsGlobals.choiceResponse = None

    while True:
        try:  # moved this line here
            send_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            send_sock.connect((dtsGlobals.GUI_TCP_IP, 9822))  # no longer throws error
            send_sock.close()
            break
        except socket.error:
            time.sleep(1)

    myQps = QpsInterface(host=dtsGlobals.GUI_TCP_IP)

    status = myQps.sendCmdVerbose("$qis status")
    while "Not Connected" in status:
        status = myQps.sendCmdVerbose("$qis status")
        time.sleep(0.2)

    # Small pause for QIS to start finding devices
    time.sleep(3)

    # Display and choose module from found modules
    qpsDeviceList = myQps.getDeviceList()
    deviceDict = {}

    # specify the module selection header
    comms.sendMsgToGUI("QuarchDTS::header::Choose a Quarch module to connect to", None)

    content = " "
    content = content.join(qpsDeviceList)
    if "No Devices Found" in content:
        # python logic!
        print("No Quarch modules currently detected")
    else:
        for quarchModule in qpsDeviceList:
            # Skip rest modules as we can't stream over rest
            if "rest" in quarchModule:
                continue
            connectionWithoutConType = quarchModule[quarchModule.rindex(":") + 1:]
            # Sending in the form : tcp::QTL1995-05-006
            comms.newNotifyChoiceOption("qpsmodule", quarchModule, connectionWithoutConType )#outputMode=outputModeValue )

    # wait for next response from java
    comms.sendMsgToGUI("QuarchDTS::end-of-data", None)

    while dtsGlobals.choiceResponse is None and dtsGlobals.continueTest is True:
        time.sleep(0.25)

    # order should be choiceResponse::xyz
    choice = bytes.decode(dtsGlobals.choiceResponse)
    print("response from selection was : " + choice)
    selection = choice.split("::", 2)

    if "choice-abort" in choice:
        return None
    elif "rescan" in choice:
        return chooseQuarchModuleQPS(moduleName, myQps)

    # Obtain output from the quarchModule selection
    selection[1] = selection[1].replace(":", "::")
    print("Selection1 is now " + selection[1])

    outMode = myQps.sendCmdVerbose(selection[1] + " conf:out:mode?")
    print("Out mode for selection was " + outMode)
    if "DISABLED" in outMode:
        comms.sendMsgToGUI("QuarchDTS::header::Choose a Quarch module to connect to", None)
        selection[1] = selection[1].replace("::", ":")
        print("changed selection1 back to : " + selection[1] + " for the cmd send")
        connectionWithoutConType = selection[1][selection.rindex(":") + 1:]
        comms.newNotifyChoiceOption("qpsmodule", selection[1], connectionWithoutConType)
        # small wait to gauranteee the frontend deals with parse +  list add before display appears
        time.sleep(0.5)
        comms.sendMsgToGUI("QuarchDTS::end-of-data::true", None)
        while dtsGlobals.choiceResponse is None and dtsGlobals.continueTest is True:
            time.sleep(0.25)
        selection[1] = selection[1].replace(":", "::")
        outMode = selection[2]
        print(outMode)

    selection[1] = selection[1].replace("::", ":")
    selection = selection[1]

    # if user does not select an item, we abort

    return selection.strip() + "=" + outMode


def chooseQuarchModule(moduleName):
    dtsGlobals.choiceResponse = None

    # scan for quarch devices
    scanDictionary = scanDevices()

    # specify the module selection header
    comms.sendMsgToGUI("QuarchDTS::header::Choose a Quarch module to connect to", None)

    # Print the provided list of devices with a numbered prefix
    for connection in scanDictionary:
        # need to replace before and after send
        #connection = connection.replace("::", ":")
        #comms.notifyChoiceOption(connection, scanDictionary[connection])
        comms.newNotifyChoiceOption("module", connection, scanDictionary[connection])
    if not scanDictionary:
        # python logic!
        print("ERROR - No quarch modules found to display")

    # wait for next response from java
    comms.sendMsgToGUI("QuarchDTS::end-of-data", None)

    while dtsGlobals.choiceResponse is None and dtsGlobals.continueTest is True:
        time.sleep(0.25)

    choice = bytes.decode(dtsGlobals.choiceResponse)
    selection = choice.split("::")
    # order should be choiceResponse::xyz
    selection = selection[1]
    selection = selection.replace(":", "::")

    # if user does not select an item, we abort
    if "choice-abort" in selection:
        return None
    elif "rescan" in selection:
        return chooseQuarchModule(moduleName)
    else:
        return selection.strip()


'''
Parses and executes all the tests specified within the given CSV file
testCallbacks=Dictionary of callback function for the tests
filePath=Full path to CSV file containing the tests
'''


def executeCsvTestFile(testCallbacks, filePath, delimitor="\t"):
    # Open the test file for parsing
    with open(filePath, 'r') as scriptFile:
        # Iterate through each line in the file
        for fileLine in scriptFile:
            # Comment lines
            if (fileLine.find("#") == 0):
                # Ignore file comment lines
                continue
            # Config line - for setting up modules and test elements
            elif (fileLine.find("Config") == 0):
                # Split the line into sections
                lineSections = fileLine.split(delimitor)
                # Get the module that the setup function is in
                moduleName = lineSections[1]
                # Get the name of the setup function
                testName = lineSections[2]

                # Build up the paramenter string for the python function call
                funcParams = ""
                for x in range(3, len(lineSections)):
                    # Skip any params that have no data (CSV file can generate empty params here)
                    if (len(lineSections[x].strip()) > 0):
                        funcParams = funcParams + lineSections[x].strip() + ","
                # Strip the last comma off the end
                funcParams = funcParams.strip(',')

                # Parse the string into a dictionary of parameters
                parsedArgs = dict(e.split('=') for e in funcParams.split(','))
                modulePointer = sys.modules[moduleName]
                # Call the function, using module.function(parameters)
                getattr(modulePointer, testName)(**parsedArgs)
            # Standard test line - for running a defined test
            elif (fileLine.find("Test") == 0):
                # Split the line into sections
                lineSections = fileLine.split(delimitor)
                # Get the module that the setup function is in
                moduleName = lineSections[1]
                # Get the name of the setup function
                testName = lineSections[2]

                # Build up the paramenter string for the python function call
                funcParams = ""
                for x in range(3, len(lineSections)):
                    # Skip any params that have no data (CSV file can generate empty params here)
                    if (len(lineSections[x].strip()) > 0):
                        funcParams = funcParams + lineSections[x].strip() + ","
                # Strip the last comma off the end
                funcParams = funcParams.strip(',')

                # Parse the string into a dictionary of parameters
                parsedArgs = dict(e.split('=') for e in funcParams.split(','))

                # Get the module pointer for the required test module
                modulePointer = sys.modules[moduleName]
                # Call the function, using module.function(parameters)
                getattr(modulePointer, testName)(**parsedArgs)
            # Skip line - used to mark test for temporary bypass
            elif (fileLine.find("Skip") == 0):
                continue
            # Ignore blank lines
            elif (len(fileLine.strip()) == 0):
                continue
            # Undefined line type
            else:
                # Split the line into sections
                lineSections = fileLine.split(delimitor)
                # Log the error of the unknown line type
                driveTestConfig.testCallbacks["TEST_LOG"](time.time(), "error",
                                                          "Unknown test line type: " + lineSections[0],
                                                          os.path.basename(
                                                              __file__) + " - " + sys._getframe().f_code.co_name)


'''
Adds a newly defined disk drive to use during the test
driveId="PCI:0:00.0"
driveName="myDrive1"
'''


def specifyDriveById(driveId, driveName):
    # Add the item to the test resources dictionary
    driveTestConfig.testResources[driveName] = driveId


'''
Callback function allowing tests to request a specific 'test resource' item
This could be a quarch module connection, setup string or any other object.
These resources are created during the 'Config' phase

resourceName=Name of the resource to return
'''


def getTestResource(resourceName):
    if (resourceName in driveTestConfig.testResources):
        return driveTestConfig.testResources[resourceName]
    else:
        notifyTestLogEvent(time.time(), "error", "Unknown resource item requested:" + resourceName,
                           os.path.basename(__file__) + " - " + sys._getframe().f_code.co_name,
                           {"textDetails": "The given resource name was not found"})
        return None


'''
Callback function allowing tests to store a specific 'test resource' item
This could be a quarch module connection, setup string or any other object.
These resources are created during the 'Config' phase

resourceName = Unique name of resource
resourceValue = Value for resource
'''


def setTestResource(resourceName, resourceValue):
    driveTestConfig.testResources[resourceName] = resourceValue


def resetTestResources():
    # python booleanness logic - if true there's something here
    if driveTestConfig.testResources:
        driveTestConfig.testResources.clear()

    # resetting test variable
    dtsGlobals.continueTest = True
    dtsGlobals.validVersion = True


'''
Callback: Run when a test invokes UTILS_VISUALSLEEP.  This allows user feedback when a delay function is required. Specified
delay time is in seconds
'''


def checkDriveState(driveObject, deviceState, waitTime):
    # DeviceState 0 : Wait for device to be cleared from list
    # DeviceState 1 : Wait for device to appear in list

    start = time.time()
    loop = 0
    end = time.time() - start
    toFind = ""
    # if deviceState is 0:
    #     print ("looking for device to be off")
    # if deviceState is 1:
    #     print ("Looking for device to be detected")

    while (end < float(waitTime)):
        end = time.time() - start
        # Should be the only time that we don't want to check lane speeds
        if driveTestConfig.testCallbacks["TEST_GETDISKSTATUS"]("", driveObject, deviceState, checkLanes=False):
            #print("device new state after " + str(end) + " seconds" )
            return

        time.sleep(0.1)
        loop += 1
        if loop == 5:
            loop = 0
            comms.sendMsgToGUI("testing>")


def visualSleep(delayTime):
    # Print header for delay
    # print("Delay:" + str(delayTime) + "S:", end="")
    # Tick through each second
    for x in range(0, int(delayTime)):
        time.sleep(1)
        # print(".", end="")
        # Send msg every second ( 5 seconds allow for disconnect and reconnect + continue test )
        if x % 1 == 0:
            #sending across a message to show it's still alive
            comms.sendMsgToGUI("testing>")
    # Force a new line
    # print("")


'''
Callback: Run whenever a TEST_LOG event ocurrs, allowing the script to direct the various forms
of output from tests to one or more locations (terminal, results database and similar)
'''
logFilePath = os.path.join(os.getcwd(), "LogFile" + str(datetime.now()).replace(':', '_') + ".txt")


def notifyTestLogEvent(timeStamp, logType, logText, logSource, logDetails=None):
    # Build up log string
    logString = datetime.utcfromtimestamp(timeStamp).strftime(
        '%Y-%m-%d %H:%M:%S') + "\t" + logType + "\t" + logText + "\t" + logSource
    # Append details
    if (logDetails != None):
        for k, v in logDetails.items():
            logString = logString + "\t" + k + "=" + str(v)
    # Print to terminal, skipping debug if not required
    # if (not (driveTestConfig.logDebugMessagesOnTerminal == False and logType == 'debug')):
        # print(logString)
    # Write to log file, skipping debug if not required
    if (not (driveTestConfig.logDebugMessagesInFile == False and logType == 'debug')):
        with open(logFilePath, 'a') as logFile:
            logFile.write(logString + "\n")





'''
Simple debug function for collating terminal print requests for debug purposes.
Use this rather than a direct print for all debug messages
'''
def debugTerminalPrint(message):
    if (driveTestConfig.logTerminalDebug == True):
        print(message)
    return


'''
Callback: Run when a test invokes TEST_GETDISKSTATUS (Check the status of the drive).  This can use lspci or
be expanded to use any form of internal test tool
'''
def DiskStatusCheck(uniqueID, driveId, expectedState, checkLanes=True):

    # PCIE drive type
    if "PCIE" in str(driveId).upper() and driveId.index('PCIE:') == 0:
        # Get pcieMappingMode resource if set
        # Check to see if the pcieMappingMode resource string is set
        mappingMode = getTestResource("pcieMappingMode")
        if (mappingMode == None):
            mappingMode = False

        # Get the PCIe address
        pcieAddress = driveId[5:]
        driveState = myHostInfo.isDevicePresent(pcieAddress, mappingMode, "pcie")

        # If drive should be plugged, verify the speed and link width
        if (expectedState):
            if driveState:
                # Moving this so it's not checked on every search for device
                if checkLanes:
                    return myHostInfo.verifyDriveStats(uniqueID, pcieAddress, mappingMode)
                #print("device was discovered - PASS")
                return True
            else:
                #print("device was not discovered - FAIL")
                return False
        else:
            if (driveState == False):
                #print("device was undiscovered - PASS")
                return True
            else:
                #print("device was discovered - FAIL")
                return False

        return driveState
        # PCIE drive type
    elif "SAS" in str(driveId).upper() and driveId.index('SAS:') == 0:
        # Get pcieMappingMode resource if set
        # Check to see if the pcieMappingMode resource string is set

        mappingMode = getTestResource("pcieMappingMode")
        if (mappingMode == None):
            mappingMode = False

        sasDriveName = driveId[4:]
        driveState = myHostInfo.isDevicePresent(sasDriveName, mappingMode, "sas")

        # If drive should be plugged, verify the speed and link width
        if (expectedState):  # if true, device is plugged and should be found
            if driveState:
                #print("device was discovered - PASS")
                return True
            else:
                #print("device was not discovered - FAIL")
                return False
        else:
            if (driveState == False):
                #print("device was undiscovered - PASS")
                return True
            else:
                #print("device was discovered - FAIL")
                return False

        return driveState
    # Unknown device type
    else:
        notifyTestLogEvent(time.time(), "error", "Unknown drive type: " + driveId,
                           os.path.basename(__file__) + " - " + sys._getframe().f_code.co_name,
                           {"textDetails": "Unable to check status of the drive"})
        return False


# CurrentTest = "starting"
# def alivePulse():
#     counter = 0
#     quarchidentifier = "QuarchDTS"
#     separator = "::"
#     current_time = time.time()
#
#     while True:
#         # QuarchDTS::currentTest::1
#         quarchstringtosend = quarchidentifier + separator + CurrentTest + separator + str(counter)
#
#         # print("time is " + str(time.time() - current_time))
#
#         if (time.time() - current_time) > 1:
#             # send item to gui and reset function variables
#
#             try:
#                 sendMsgToGUI(quarchstringtosend)
#                 counter += 1
#             except Exception as e:
#                 print("server not up")
#                 print(e)
#                 pass
#             current_time = time.time()
#
#         # as to not clutter cpu
#         time.sleep(.1)
'''
Callback: Run whenever a TEST_LOG event ocurrs, allowing the script to direct the various forms
of output from tests to one or more locations (terminal, results database and similar)

This version logs to a remote TCP server
'''

def notifyTestLogEventXml(uniqueId, timeStamp, logType, logText, logSource, logDetails=None):

    if uniqueId is "" or uniqueId is None:
        # quick check in place just to ensure the unique id of an object is not sent incorrectly
        uniqueId = " "

    # Build main XML structure
    xmlObject = cElementTree.Element("object")
    cElementTree.SubElement(xmlObject, "uniqueID").text = uniqueId
    cElementTree.SubElement(xmlObject, "timestamp").text = datetime.utcfromtimestamp(timeStamp).strftime(
        '%Y-%m-%d %H:%M:%S')
    cElementTree.SubElement(xmlObject, "logType").text = logType
    cElementTree.SubElement(xmlObject, "text").text = logText
    cElementTree.SubElement(xmlObject, "messageSource").text = logSource
    # Add details dictionary if present
    if (logDetails != None):
        xmlDetails = cElementTree.SubElement(xmlObject, "logDetails")
        for k, v in logDetails.items():
            xmlEntry = cElementTree.SubElement(xmlDetails, "entry")
            cElementTree.SubElement(xmlEntry, "key").text = str(k)
            cElementTree.SubElement(xmlEntry, "value").text = str(v)

    xmlstr = str(cElementTree.tostring(xmlObject), "UTF-8").replace("\n", "")
    # Send to GUI server
    comms.sendMsgToGUI(xmlstr)

'''
Tries to get the local/network IP address of the server
'''
def getLocalIpAddress(first = True):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
        if IP is "127.0.0.1" and first is True:
            s.close()
            getLocalIpAddress(first = False)

    except:
        IP = None
    finally:
        s.close()
    return IP


'''
Activates a remote server at the given port number.  This function will not return until the server connection is closed

This is intended for use with a remote client (generally running a compliance test script).  This server takes in XML format command requests and executes local
test functions based on this.
'''


def attemptRestart(conn, sock):
    print("Java connection closed, attempting to recover ")
    conn.close()
    sock.close()
    # time.sleep(1)
    resetTestResources()
    ActivateRemoteServer(localHost=False)


def ActivateRemoteServer(portNumber=9742, localHost=False):

    # Creating the callbacks for future use
    driveTestConfig.testCallbacks = {"TEST_LOG": notifyTestLogEventXml,
                                     "TEST_GETDISKSTATUS": DiskStatusCheck,
                                     "UTILS_VISUALSLEEP": visualSleep,
                                     "TEST_GETRESOURCE": getTestResource,
                                     "TEST_SETRESOURCE": setTestResource,
                                     "TEST_NEWSLEEP": checkDriveState}

    TCP_PORT = portNumber
    portNumber = 1024
    BUFFER_SIZE = 4096
    mDnsInfo = None

    serverName = None
    # Get the sensible server name
    if (serverName is None):
        try:
            serverName = socket.gethostname()
        except:
            serverName = "no-name-server"

    try:
        # Setup and open the socket for connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Making the socket allow connections from any connection available...?
        # sock.bind((TCP_IP, TCP_PORT))
        sock.bind(('', TCP_PORT))
        sock.listen(1)
        print("----Remote Server Activated----")
        TCP_IP = '127.0.0.1'
        if not localHost:
            # Conditional strings
            TCP_IP = '{address}'.format(address = "127.0.0.1" if getLocalIpAddress() is None else getLocalIpAddress())
        print("\tServer IP: " + str(TCP_IP))

        # Activates mDNS registration for the server, so it can be located remotely
        if (zeroConfAvail):
            try:
                # Register the service
                mDnsIp = TCP_IP
                mDnsDesc = {'version': '1.0', 'server-name': serverName}
                mDnsInfo = ServiceInfo("_http._tcp.local.", "quarchCS._http._tcp.local.", socket.inet_aton(mDnsIp),
                                       TCP_PORT, 0, 0, mDnsDesc)
                zeroConf = Zeroconf()
                zeroConf.register_service(mDnsInfo)

                # Print registration results
                print("----mDNS Registered----")
                print("\tServer Name: " + serverName)
            except:
                print("mDNS error, Service not registered")
        else:
            zeroConf = None

        # Wait for a connection
        # sock.setblocking(0)
        conn, addr = sock.accept()
        print("----Remote Server connection opened from: " + str(addr))

        # layout = :<'x.x.x.x',xx>
        item = str(addr).split('\'')
        dtsGlobals.GUI_TCP_IP = item[1]

        continueScript = True

        # processObject = multiprocessing.Process(target=alivePulse())
        # doesn't matter if the process terminates mid - completion
        # processObject.daemon = True
        # processObject.start()
        
        comms.sendMsgToGUI("QuarchPy Version: " + pkg_resources.get_distribution("quarchpy").version)
        if not dtsGlobals.validVersion:
            print (pkg_resources.get_distribution("quarchpy").version)
            print("QCS incompatible with this QuarchPy version. Restarting server")
            attemptRestart(conn, sock)



        try:
            # Loop while the server is to be active
            while continueScript:
                # Get data from the connection
                data = conn.recv(BUFFER_SIZE)
                if not data: pass

                data = data.replace(str.encode("\r\n"), b"")
                # print("Data Received = " + bytes.decode(data))
                if (len(data) == 0):
                    # 0 data length means socket was closed by java
                    attemptRestart(conn,sock)

                if "Alive?" in bytes.decode(data):
                    # Java poll to ensure responsiveness
                    toSend = str.encode("ok >")
                    conn.sendall(toSend + b"\n")
                    continue

                try:
                    # parse command passed
                    myobj = testLine()

                    xmlRoot = cElementTree.fromstring(bytes.decode(data))
                    myobj.initFromXml(xmlRoot)

                    # Get the module pointer for the required test module
                    if myobj.moduleName == "driveTestCore":
                        modulePointer = sys.modules[__name__]
                    elif myobj.moduleName == "hostInformation":
                        modulePointer = myHostInfo
                    else:
                        modulePointer = importlib.import_module("." + myobj.moduleName, "quarchpy.disk_test")

                    # print(dtsGlobals.GUI_TCP_IP)
                    # print(bytes.decode(data))

                    # Call the requested function, using module.function(parameters)
                    getattr(modulePointer, myobj.testName)(**myobj.paramList)

                    # print("Sending Data : ok >")
                    finishedString = "ok >"
                    conn.sendall(str.encode(finishedString) + b"\n")

                    pass

                except ValueError as err:
                    traceback.print_tb(err.__traceback__)
                    print("ERROR - Bad remote command format")

                except AttributeError as e:
                    print(AttributeError)
                except ConnectionRefusedError as err:
                    print("Could not send response to Java, aborting")
                    attemptRestart(conn, sock)
                except Exception as e:
                    print(e)
                    print("ERROR - Unexpected failure in command parser")
                    raise
        except KeyboardInterrupt:
            print("---Remote server shutdown request, user CTRL-C received")
    except ConnectionResetError:
        attemptRestart(conn,sock)
    except Exception as ex:
        print("----Remote server process exited with an exception")
        print(ex)
        traceback.print_tb(ex.__traceback__)
    finally:
        # processObject.terminate()
        # processObject.join()
        if conn is not None:
            conn.close()
        # sock.shutdown()
        sock.close()
        print("----Remote server shutdown complete")

def main(argstring):
    print("\n################################################################################")
    print("\n                           QUARCH TECHNOLOGY                        \n\n  ")
    print("Automated Drive/Host test suite.   ")
    print("\n################################################################################\n")

    if (isUserAdmin() is False):
        print("Quarch Compliance Suite must be run from an elevated command prompt.")
        print("Please restart with administrator privelages")
        sys.exit()

    ActivateRemoteServer()

if __name__ == "__main__":
    main(sys.argv)



