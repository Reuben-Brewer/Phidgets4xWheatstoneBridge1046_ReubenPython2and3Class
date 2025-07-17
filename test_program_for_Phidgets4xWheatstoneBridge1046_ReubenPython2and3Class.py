# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision E, 07/17/2025

Verified working on: Python 3.11/12 for Windows 10/11 64-bit and Raspberry Pi Bookworm.
'''

__author__ = 'reuben.brewer'

###########################################################
from MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class import *
from MyPrint_ReubenPython2and3Class import *
from Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class import *
###########################################################

###########################################################
import os
import sys
import platform
import time
import datetime
import threading
import collections
import keyboard
###########################################################

###########################################################
if sys.version_info[0] < 3:
    from Tkinter import * #Python 2
    import tkFont
    import ttk
else:
    from tkinter import * #Python 3
    import tkinter.font as tkFont #Python 3
    from tkinter import ttk
###########################################################

###########################################################
import platform
if platform.system() == "Windows":
    import ctypes
    winmm = ctypes.WinDLL('winmm')
    winmm.timeBeginPeriod(1) #Set minimum timer resolution to 1ms so that time.sleep(0.001) behaves properly.
###########################################################

###########################################################################################################
##########################################################################################################
def getPreciseSecondsTimeStampString():
    ts = time.time()

    return ts
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def UpdateFrequencyCalculation():
    global CurrentTime_MainLoopThread
    global LastTime_MainLoopThread
    global DataStreamingFrequency_MainLoopThread
    global DataStreamingDeltaT_MainLoopThread
    global Counter_MainLoopThread

    try:
        DataStreamingDeltaT_MainLoopThread = CurrentTime_MainLoopThread - LastTime_MainLoopThread

        if DataStreamingDeltaT_MainLoopThread != 0.0:
            DataStreamingFrequency_MainLoopThread = 1.0 / DataStreamingDeltaT_MainLoopThread

        LastTime_MainLoopThread = CurrentTime_MainLoopThread
        Counter_MainLoopThread = Counter_MainLoopThread + 1

    except:
        exceptions = sys.exc_info()[0]
        print("UpdateFrequencyCalculation ERROR, Exceptions: %s" % exceptions)
        traceback.print_exc()
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def GUI_update_clock():
    global root
    global EXIT_PROGRAM_FLAG
    global GUI_RootAfterCallbackInterval_Milliseconds
    global USE_GUI_FLAG

    global Phidgets4xWheatstoneBridge1046_Object
    global Phidgets4xWheatstoneBridge1046_OPEN_FLAG
    global SHOW_IN_GUI_Phidgets4xWheatstoneBridge1046_FLAG

    global MyPrint_ReubenPython2and3ClassObject
    global MyPrint_OPEN_FLAG
    global SHOW_IN_GUI_MyPrint_FLAG

    if USE_GUI_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
        #########################################################
        #########################################################

            #########################################################
            if Phidgets4xWheatstoneBridge1046_OPEN_FLAG == 1 and SHOW_IN_GUI_Phidgets4xWheatstoneBridge1046_FLAG == 1:
                Phidgets4xWheatstoneBridge1046_Object.GUI_update_clock()
            #########################################################

            #########################################################
            if MyPrint_OPEN_FLAG == 1 and SHOW_IN_GUI_MyPrint_FLAG == 1:
                MyPrint_ReubenPython2and3ClassObject.GUI_update_clock()
            #########################################################

            root.after(GUI_RootAfterCallbackInterval_Milliseconds, GUI_update_clock)
        #########################################################
        #########################################################

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def ExitProgram_Callback(OptionalArugment = 0):
    global EXIT_PROGRAM_FLAG

    print("Exiting all threads in test_program_for_Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class.py")

    EXIT_PROGRAM_FLAG = 1
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def GUI_Thread():
    global root
    global root_Xpos
    global root_Ypos
    global root_width
    global root_height
    global GUI_RootAfterCallbackInterval_Milliseconds
    global USE_TABS_IN_GUI_FLAG

    ################################################# KEY GUI LINE
    #################################################
    root = Tk()
    #################################################
    #################################################

    #################################################
    #################################################
    global TabControlObject
    global Tab_MainControls
    global Tab_Phidgets4xWheatstoneBridge1046
    global Tab_MyPrint

    if USE_TABS_IN_GUI_FLAG == 1:
        #################################################
        TabControlObject = ttk.Notebook(root)

        Tab_Phidgets4xWheatstoneBridge1046 = ttk.Frame(TabControlObject)
        TabControlObject.add(Tab_Phidgets4xWheatstoneBridge1046, text='   WheatstoneBridge   ')

        Tab_MainControls = ttk.Frame(TabControlObject)
        TabControlObject.add(Tab_MainControls, text='   Main Controls   ')

        Tab_MyPrint = ttk.Frame(TabControlObject)
        TabControlObject.add(Tab_MyPrint, text='   MyPrint Terminal   ')

        TabControlObject.grid(row=0, column=0, sticky='nsew')

        ############# #Set the tab header font
        TabStyle = ttk.Style()
        TabStyle.configure('TNotebook.Tab', font=('Helvetica', '12', 'bold'))
        #############

        #################################################
    else:
        #################################################
        Tab_MainControls = root
        Tab_Phidgets4xWheatstoneBridge1046 = root
        Tab_MyPrint = root
        #################################################

    #################################################
    #################################################

    ################################################# THIS BLOCK MUST COME 2ND-TO-LAST IN def GUI_Thread() IF USING TABS.
    root.protocol("WM_DELETE_WINDOW", ExitProgram_Callback)  # Set the callback function for when the window's closed.
    root.title("test_program_for_Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class")
    root.geometry('%dx%d+%d+%d' % (root_width, root_height, root_Xpos, root_Ypos)) # set the dimensions of the screen and where it is placed
    root.after(GUI_RootAfterCallbackInterval_Milliseconds, GUI_update_clock)
    root.mainloop()
    #################################################

    #################################################  THIS BLOCK MUST COME LAST IN def GUI_Thread() REGARDLESS OF CODE.
    root.quit() #Stop the GUI thread, MUST BE CALLED FROM GUI_Thread
    root.destroy() #Close down the GUI thread, MUST BE CALLED FROM GUI_Thread
    #################################################

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
if __name__ == '__main__':

    ##########################################################################################################
    ##########################################################################################################
    global my_platform

    if platform.system() == "Linux":

        if "raspberrypi" in platform.uname():  # os.uname() doesn't work in windows
            my_platform = "pi"
        else:
            my_platform = "linux"

    elif platform.system() == "Windows":
        my_platform = "windows"

    elif platform.system() == "Darwin":
        my_platform = "mac"

    else:
        my_platform = "other"

    print("The OS platform is: " + my_platform)
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    global USE_GUI_FLAG
    USE_GUI_FLAG = 1

    global USE_TABS_IN_GUI_FLAG
    USE_TABS_IN_GUI_FLAG = 1

    global USE_Phidgets4xWheatstoneBridge1046_FLAG
    USE_Phidgets4xWheatstoneBridge1046_FLAG = 1

    global USE_MyPrint_FLAG
    USE_MyPrint_FLAG = 1

    global USE_MyPlotterPureTkinterStandAloneProcess_FLAG
    USE_MyPlotterPureTkinterStandAloneProcess_FLAG = 1

    global USE_KEYBOARD_FLAG
    USE_KEYBOARD_FLAG = 1
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    global SHOW_IN_GUI_Phidgets4xWheatstoneBridge1046_FLAG
    SHOW_IN_GUI_Phidgets4xWheatstoneBridge1046_FLAG = 1

    global SHOW_IN_GUI_MyPrint_FLAG
    SHOW_IN_GUI_MyPrint_FLAG = 1
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    global GUI_ROW_Phidgets4xWheatstoneBridge1046
    global GUI_COLUMN_Phidgets4xWheatstoneBridge1046
    global GUI_PADX_Phidgets4xWheatstoneBridge1046
    global GUI_PADY_Phidgets4xWheatstoneBridge1046
    global GUI_ROWSPAN_Phidgets4xWheatstoneBridge1046
    global GUI_COLUMNSPAN_Phidgets4xWheatstoneBridge1046
    GUI_ROW_Phidgets4xWheatstoneBridge1046 = 1

    GUI_COLUMN_Phidgets4xWheatstoneBridge1046 = 0
    GUI_PADX_Phidgets4xWheatstoneBridge1046 = 1
    GUI_PADY_Phidgets4xWheatstoneBridge1046 = 1
    GUI_ROWSPAN_Phidgets4xWheatstoneBridge1046 = 1
    GUI_COLUMNSPAN_Phidgets4xWheatstoneBridge1046 = 1

    global GUI_ROW_MyPrint
    global GUI_COLUMN_MyPrint
    global GUI_PADX_MyPrint
    global GUI_PADY_MyPrint
    global GUI_ROWSPAN_MyPrint
    global GUI_COLUMNSPAN_MyPrint
    GUI_ROW_MyPrint = 2

    GUI_COLUMN_MyPrint = 0
    GUI_PADX_MyPrint = 1
    GUI_PADY_MyPrint = 1
    GUI_ROWSPAN_MyPrint = 1
    GUI_COLUMNSPAN_MyPrint = 1
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    global EXIT_PROGRAM_FLAG
    EXIT_PROGRAM_FLAG = 0

    global CurrentTime_MainLoopThread
    CurrentTime_MainLoopThread = -11111.0

    global LastTime_MainLoopThread
    LastTime_MainLoopThread = -11111.0

    global DataStreamingFrequency_MainLoopThread
    DataStreamingFrequency_MainLoopThread = -11111.0

    global DataStreamingDeltaT_MainLoopThread
    DataStreamingDeltaT_MainLoopThread = -11111.0

    global StartingTime_MainLoopThread
    StartingTime_MainLoopThread = -1

    global Counter_MainLoopThread
    Counter_MainLoopThread = 0

    global root

    global root_Xpos
    root_Xpos = 900

    global root_Ypos
    root_Ypos = 0

    global root_width
    root_width = 1920 - root_Xpos

    global root_height
    root_height = 1020 - root_Ypos

    global TabControlObject
    global Tab_MainControls
    global Tab_Phidgets4xWheatstoneBridge1046
    global Tab_MyPrint

    global GUI_RootAfterCallbackInterval_Milliseconds
    GUI_RootAfterCallbackInterval_Milliseconds = 30
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    global Phidgets4xWheatstoneBridge1046_Object

    global Phidgets4xWheatstoneBridge1046_OPEN_FLAG
    Phidgets4xWheatstoneBridge1046_OPEN_FLAG = -1

    global NumberOfWheatstoneBridges
    NumberOfWheatstoneBridges = 4

    global Phidgets4xWheatstoneBridge1046_MostRecentDict
    Phidgets4xWheatstoneBridge1046_MostRecentDict = dict()

    global Phidgets4xWheatstoneBridge1046_MostRecentDict_VoltageRatioInputsList_VoltageRatio_Raw
    Phidgets4xWheatstoneBridge1046_MostRecentDict_VoltageRatioInputsList_VoltageRatio_Raw = [-11111.0] * NumberOfWheatstoneBridges

    global Phidgets4xWheatstoneBridge1046_MostRecentDict_VoltageRatioInputsList_VoltageRatio_Filtered
    Phidgets4xWheatstoneBridge1046_MostRecentDict_VoltageRatioInputsList_VoltageRatio_Filtered = [-11111.0] * NumberOfWheatstoneBridges

    global Phidgets4xWheatstoneBridge1046_MostRecentDict_VoltageRatioInputsList_ErrorCallbackFiredFlag
    Phidgets4xWheatstoneBridge1046_MostRecentDict_VoltageRatioInputsList_ErrorCallbackFiredFlag = [-11111.0] * NumberOfWheatstoneBridges

    global Phidgets4xWheatstoneBridge1046_MostRecentDict_VoltageRatioInputsList_UpdateDeltaTseconds
    Phidgets4xWheatstoneBridge1046_MostRecentDict_VoltageRatioInputsList_UpdateDeltaTseconds = [-11111.0] * NumberOfWheatstoneBridges

    global Phidgets4xWheatstoneBridge1046_MostRecentDict_VoltageRatioInputsList_VoltageRatio_LowPassFilter_Lambda
    Phidgets4xWheatstoneBridge1046_MostRecentDict_VoltageRatioInputsList_VoltageRatio_LowPassFilter_Lambda = [-11111.0] * NumberOfWheatstoneBridges

    global Phidgets4xWheatstoneBridge1046_MostRecentDict_Time
    Phidgets4xWheatstoneBridge1046_MostRecentDict_Time = [-11111.0] * NumberOfWheatstoneBridges
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    global MyPrint_ReubenPython2and3ClassObject

    global MyPrint_OPEN_FLAG
    MyPrint_OPEN_FLAG = -1
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    global MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject

    global MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG
    MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG = -1

    global MyPlotterPureTkinter_MostRecentDict
    MyPlotterPureTkinter_MostRecentDict = dict()

    global MyPlotterPureTkinterStandAloneProcess_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag
    MyPlotterPureTkinterStandAloneProcess_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag = -1

    global LastTime_MainLoopThreadMyPlotterPureTkinterStandAloneProcess_
    LastTime_MainLoopThreadMyPlotterPureTkinterStandAloneProcess_ = -11111.0
    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## KEY GUI LINE
    ##########################################################################################################
    if USE_GUI_FLAG == 1:
        print("Starting GUI thread...")
        GUI_Thread_ThreadingObject = threading.Thread(target=GUI_Thread)
        GUI_Thread_ThreadingObject.setDaemon(True) #Should mean that the GUI thread is destroyed automatically when the main thread is destroyed.
        GUI_Thread_ThreadingObject.start()
        time.sleep(0.5)  #Allow enough time for 'root' to be created that we can then pass it into other classes.
    else:
        root = None
        Tab_MainControls = None
        Tab_Phidgets4xWheatstoneBridge1046 = None
        Tab_MyPrint = None
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    global Phidgets4xWheatstoneBridge1046_GUIparametersDict
    Phidgets4xWheatstoneBridge1046_GUIparametersDict = dict([("USE_GUI_FLAG", USE_GUI_FLAG and SHOW_IN_GUI_Phidgets4xWheatstoneBridge1046_FLAG),
                                                                                        ("root", Tab_Phidgets4xWheatstoneBridge1046),
                                                                                        ("EnableInternal_MyPrint_Flag", 1),
                                                                                        ("NumberOfPrintLines", 10),
                                                                                        ("UseBorderAroundThisGuiObjectFlag", 0),
                                                                                        ("GUI_ROW", GUI_ROW_Phidgets4xWheatstoneBridge1046),
                                                                                        ("GUI_COLUMN", GUI_COLUMN_Phidgets4xWheatstoneBridge1046),
                                                                                        ("GUI_PADX", GUI_PADX_Phidgets4xWheatstoneBridge1046),
                                                                                        ("GUI_PADY", GUI_PADY_Phidgets4xWheatstoneBridge1046),
                                                                                        ("GUI_ROWSPAN", GUI_ROWSPAN_Phidgets4xWheatstoneBridge1046),
                                                                                        ("GUI_COLUMNSPAN", GUI_COLUMNSPAN_Phidgets4xWheatstoneBridge1046)])

    global Phidgets4xWheatstoneBridge1046_SetupDict
    Phidgets4xWheatstoneBridge1046_SetupDict = dict([("GUIparametersDict", Phidgets4xWheatstoneBridge1046_GUIparametersDict),
                                                                                    ("DesiredSerialNumber", -1), #LEAVE AS -1 (FOR ANY BOARD), OR CHANGE THIS TO MATCH YOUR UNIQUE SERIAL NUMBER
                                                                                    ("WaitForAttached_TimeoutDuration_Milliseconds", 5000),
                                                                                    ("NameToDisplay_UserSet", "Reuben's Test Wheatstone Bridge Board"),
                                                                                    ("UsePhidgetsLoggingInternalToThisClassObjectFlag", 1),
                                                                                    ("VoltageRatioInputsList_EnabledStateBoolean", [1, 1, 1, 1]),
                                                                                    ("VoltageRatioInputsList_BridgeGain_ActualIntegerValue", [128, 128, 128, 128]),
                                                                                    ("VoltageRatioInputsList_VoltageRatio_LowPassFilter_Lambda", [0.90, 0.90, 0.90, 0.90]),
                                                                                    ("VoltageRatioInputsList_VoltageRatioChangeTrigger", [0.0, 0.0, 0.0, 0.0]),
                                                                                    ("VoltageRatioInputsList_CallbackUpdateDeltaTmilliseconds", [8, 8, 8, 8]),
                                                                                    ("DataCollectionDurationInSecondsForSnapshottingBridge", 2.0),
                                                                                    ("MainThread_TimeToSleepEachLoop", 0.008)])

    if USE_Phidgets4xWheatstoneBridge1046_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        try:
            Phidgets4xWheatstoneBridge1046_Object = Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class(Phidgets4xWheatstoneBridge1046_SetupDict)
            Phidgets4xWheatstoneBridge1046_OPEN_FLAG = Phidgets4xWheatstoneBridge1046_Object.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("Phidgets4xWheatstoneBridge1046_Object __init__: Exceptions: %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    if USE_Phidgets4xWheatstoneBridge1046_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
            if Phidgets4xWheatstoneBridge1046_OPEN_FLAG != 1:
                print("Failed to open Phidgets4xWheatstoneBridge1046_Object.")
                #ExitProgram_Callback()
    ##########################################################################################################
    ##########################################################################################################

    #################################################
    #################################################
    if USE_MyPrint_FLAG == 1:

        global MyPrint_ReubenPython2and3ClassObject_GUIparametersDict
        MyPrint_ReubenPython2and3ClassObject_GUIparametersDict = dict([("USE_GUI_FLAG", USE_GUI_FLAG and SHOW_IN_GUI_MyPrint_FLAG),
                                                                        ("root", Tab_MyPrint),
                                                                        ("UseBorderAroundThisGuiObjectFlag", 0),
                                                                        ("GUI_ROW", GUI_ROW_MyPrint),
                                                                        ("GUI_COLUMN", GUI_COLUMN_MyPrint),
                                                                        ("GUI_PADX", GUI_PADX_MyPrint),
                                                                        ("GUI_PADY", GUI_PADY_MyPrint),
                                                                        ("GUI_ROWSPAN", GUI_ROWSPAN_MyPrint),
                                                                        ("GUI_COLUMNSPAN", GUI_COLUMNSPAN_MyPrint)])

        global MyPrint_ReubenPython2and3ClassObject_setup_dict
        MyPrint_ReubenPython2and3ClassObject_setup_dict = dict([("NumberOfPrintLines", 10),
                                                                ("WidthOfPrintingLabel", 200),
                                                                ("PrintToConsoleFlag", 1),
                                                                ("LogFileNameFullPath", os.getcwd() + "//TestLog.txt"),
                                                                ("GUIparametersDict", MyPrint_ReubenPython2and3ClassObject_GUIparametersDict)])

        try:
            MyPrint_ReubenPython2and3ClassObject = MyPrint_ReubenPython2and3Class(MyPrint_ReubenPython2and3ClassObject_setup_dict)
            MyPrint_OPEN_FLAG = MyPrint_ReubenPython2and3ClassObject.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("MyPrint_ReubenPython2and3ClassObject __init__: Exceptions: %s" % exceptions)
            traceback.print_exc()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_MyPrint_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
            if MyPrint_OPEN_FLAG != 1:
                print("Failed to open MyPrint_ReubenPython2and3ClassObject.")
                ExitProgram_Callback()
    #################################################
    #################################################

    #################################################
    #################################################
    global MyPlotterPureTkinterStandAloneProcess_GUIparametersDict
    MyPlotterPureTkinterStandAloneProcess_GUIparametersDict = dict([("EnableInternal_MyPrint_Flag", 1),
                                                                    ("NumberOfPrintLines", 10),
                                                                    ("UseBorderAroundThisGuiObjectFlag", 0),
                                                                    ("GraphCanvasWidth", 890),
                                                                    ("GraphCanvasHeight", 700),
                                                                    ("GraphCanvasWindowStartingX", 0),
                                                                    ("GraphCanvasWindowStartingY", 0),
                                                                    ("GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents", 20)])

    global MyPlotterPureTkinterStandAloneProcess_SetupDict
    MyPlotterPureTkinterStandAloneProcess_SetupDict = dict([("GUIparametersDict", MyPlotterPureTkinterStandAloneProcess_GUIparametersDict),
                                                            ("ParentPID", os.getpid()),
                                                            ("WatchdogTimerExpirationDurationSeconds_StandAlonePlottingProcess", 0.0),
                                                            ("MarkerSize", 3),
                                                            ("CurvesToPlotNamesAndColorsDictOfLists", dict([("NameList", ["Channel0", "Channel1", "Channel2", "Channel3"]),
                                                                                                            ("MarkerSizeList", [2, 2, 2, 2]),
                                                                                                            ("LineWidthList", [1, 1, 1, 1]),
                                                                                                            ("IncludeInXaxisAutoscaleCalculationList", [1, 1, 1, 1]),
                                                                                                            ("IncludeInYaxisAutoscaleCalculationList", [1, 1, 1, 1]),
                                                                                                            ("ColorList", ["Red", "Green", "Blue", "Black"])])),
                                                            ("SmallTextSize", 7),
                                                            ("LargeTextSize", 12),
                                                            ("NumberOfDataPointToPlot", 50),
                                                            ("XaxisNumberOfTickMarks", 10),
                                                            ("YaxisNumberOfTickMarks", 10),
                                                            ("XaxisNumberOfDecimalPlacesForLabels", 3),
                                                            ("YaxisNumberOfDecimalPlacesForLabels", 3),
                                                            ("XaxisAutoscaleFlag", 1),
                                                            ("YaxisAutoscaleFlag", 1),
                                                            ("X_min", 0.0),
                                                            ("X_max", 20.0),
                                                            ("Y_min", -0.0015),
                                                            ("Y_max", 0.0015),
                                                            ("XaxisDrawnAtBottomOfGraph", 0),
                                                            ("XaxisLabelString", "Time (sec)"),
                                                            ("YaxisLabelString", "Y-units (units)"),
                                                            ("ShowLegendFlag", 1),
                                                            ("SavePlot_DirectoryPath", os.path.join(os.getcwd(), "SavedImagesFolder"))])

    if USE_MyPlotterPureTkinterStandAloneProcess_FLAG == 1:
        try:
            MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject = MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class(MyPlotterPureTkinterStandAloneProcess_SetupDict)
            MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG = MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject, exceptions: %s" % exceptions)
            traceback.print_exc()
    #################################################
    #################################################

    ##########################################################################################################
    ##########################################################################################################
    if USE_MyPlotterPureTkinterStandAloneProcess_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
            if MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG != 1:
                print("Failed to open MyPlotterPureTkinterClass_Object.")
                #ExitProgram_Callback()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    if USE_KEYBOARD_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        keyboard.on_press_key("esc", ExitProgram_Callback)
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    if EXIT_PROGRAM_FLAG == 0:
        print("$$$$$$$$$$$$$$ Starting test_program_for_Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class.py $$$$$$$$$$$$$$")
        StartingTime_CalculatedFromMainThread = getPreciseSecondsTimeStampString()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    while(EXIT_PROGRAM_FLAG == 0):

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        CurrentTime_MainLoopThread = getPreciseSecondsTimeStampString() - StartingTime_MainLoopThread
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ########################################################################################################## GET's
        ##########################################################################################################
        if Phidgets4xWheatstoneBridge1046_OPEN_FLAG == 1:

            Phidgets4xWheatstoneBridge1046_MostRecentDict = Phidgets4xWheatstoneBridge1046_Object.GetMostRecentDataDict()

            if "Time" in Phidgets4xWheatstoneBridge1046_MostRecentDict:
                Phidgets4xWheatstoneBridge1046_MostRecentDict_VoltageRatioInputsList_VoltageRatio_Raw = Phidgets4xWheatstoneBridge1046_MostRecentDict["VoltageRatioInputsList_VoltageRatio_Raw"]
                Phidgets4xWheatstoneBridge1046_MostRecentDict_VoltageRatioInputsList_VoltageRatio_Filtered = Phidgets4xWheatstoneBridge1046_MostRecentDict["VoltageRatioInputsList_VoltageRatio_Filtered"]
                Phidgets4xWheatstoneBridge1046_MostRecentDict_VoltageRatioInputsList_ErrorCallbackFiredFlag = Phidgets4xWheatstoneBridge1046_MostRecentDict["VoltageRatioInputsList_ErrorCallbackFiredFlag"]
                Phidgets4xWheatstoneBridge1046_MostRecentDict_VoltageRatioInputsList_UpdateDeltaTseconds = Phidgets4xWheatstoneBridge1046_MostRecentDict["VoltageRatioInputsList_UpdateDeltaTseconds"]
                Phidgets4xWheatstoneBridge1046_MostRecentDict_VoltageRatioInputsList_VoltageRatio_LowPassFilter_Lambda = Phidgets4xWheatstoneBridge1046_MostRecentDict["VoltageRatioInputsList_VoltageRatio_LowPassFilter_Lambda"]
                Phidgets4xWheatstoneBridge1046_MostRecentDict_Time = Phidgets4xWheatstoneBridge1046_MostRecentDict["Time"]

                #print("Phidgets4xWheatstoneBridge1046_MostRecentDict_Time: " + str(Phidgets4xWheatstoneBridge1046_MostRecentDict_Time))
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        if MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG == 1:

            ##########################################################################################################
            MyPlotterPureTkinterStandAloneProcess_MostRecentDict = MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject.GetMostRecentDataDict()

            if "StandAlonePlottingProcess_ReadyForWritingFlag" in MyPlotterPureTkinterStandAloneProcess_MostRecentDict:
                MyPlotterPureTkinterStandAloneProcess_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag = MyPlotterPureTkinterStandAloneProcess_MostRecentDict["StandAlonePlottingProcess_ReadyForWritingFlag"]

                if MyPlotterPureTkinterStandAloneProcess_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag == 1:
                    if CurrentTime_MainLoopThread - LastTime_MainLoopThreadMyPlotterPureTkinterStandAloneProcess_ >= 0.030:
                        MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject.ExternalAddPointOrListOfPointsToPlot(["Channel0", "Channel1", "Channel2", "Channel3"], [CurrentTime_MainLoopThread]*NumberOfWheatstoneBridges, Phidgets4xWheatstoneBridge1046_MostRecentDict_VoltageRatioInputsList_VoltageRatio_Filtered)
                        
                        LastTime_MainLoopThreadMyPlotterPureTkinterStandAloneProcess_ = CurrentTime_MainLoopThread
            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        UpdateFrequencyCalculation()
        time.sleep(0.010)
        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## THIS IS THE EXIT ROUTINE!
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    print("Exiting main program test_program_for_Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class.py")

    #################################################
    if Phidgets4xWheatstoneBridge1046_OPEN_FLAG == 1:
        Phidgets4xWheatstoneBridge1046_Object.ExitProgram_Callback()
    #################################################

    #################################################
    if MyPrint_OPEN_FLAG == 1:
        MyPrint_ReubenPython2and3ClassObject.ExitProgram_Callback()
    #################################################

    #################################################
    if MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG == 1:
        MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject.ExitProgram_Callback()
    #################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################