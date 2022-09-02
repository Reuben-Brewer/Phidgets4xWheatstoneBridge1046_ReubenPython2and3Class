# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision B, 08/29/2022

Verified working on: Python 2.7, 3.8 for Windows 8.1, 10 64-bit and Raspberry Pi Buster (no Mac testing yet).
'''

__author__ = 'reuben.brewer'

###########################################################
from LowPassFilter_ReubenPython2and3Class import *
###########################################################

###########################################################
import os
import sys
import platform
import time
import datetime
import math
import collections
from copy import * #for deepcopy
import inspect #To enable 'TellWhichFileWereIn'
import threading
import traceback
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
if sys.version_info[0] < 3:
    import Queue  # Python 2
else:
    import queue as Queue  # Python 3
###########################################################

###########################################################
if sys.version_info[0] < 3:
    from builtins import raw_input as input
else:
    from future.builtins import input as input
###########################################################"sudo pip3 install future" (Python 3) AND "sudo pip install future" (Python 2)

###########################################################
import platform
if platform.system() == "Windows":
    import ctypes
    winmm = ctypes.WinDLL('winmm')
    winmm.timeBeginPeriod(1) #Set minimum timer resolution to 1ms so that time.sleep(0.001) behaves properly.
###########################################################

###########################################################
import Phidget22
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Devices.Log import *
from Phidget22.LogLevel import *
from Phidget22.Devices.VoltageRatioInput import *
###########################################################

class Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class(Frame): #Subclass the Tkinter Frame

    #######################################################################################################################
    #######################################################################################################################
    def __init__(self, setup_dict): #Subclass the Tkinter Frame

        print("#################### Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class __init__ starting. ####################")

        #########################################################
        #########################################################
        self.EXIT_PROGRAM_FLAG = 0
        self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 0
        self.EnableInternal_MyPrint_Flag = 0
        self.MainThread_still_running_flag = 0

        self.CurrentTime_CalculatedFromMainThread = -11111.0
        self.StartingTime_CalculatedFromMainThread = -11111.0
        self.LastTime_CalculatedFromMainThread = -11111.0
        self.DataStreamingFrequency_CalculatedFromMainThread = -11111.0
        self.DataStreamingDeltaT_CalculatedFromMainThread = -11111.0

        self.DetectedDeviceName = "default"
        self.DetectedDeviceID = "default"
        self.DetectedDeviceVersion = "default"
        self.DetectedDeviceSerialNumber = "default"

        self.VoltageRatioInputsList_PhidgetsVoltageRatioInputObjects = list()

        self.NumberOfWheatstoneBridges = 4

        self.VoltageRatioInputsList_AttachedAndOpenFlag = [0.0] * self.NumberOfWheatstoneBridges
        self.VoltageRatioInputsList_UpdateDeltaTseconds = [0.0] * self.NumberOfWheatstoneBridges
        self.VoltageRatioInputsList_UpdateFrequencyHz = [0.0] * self.NumberOfWheatstoneBridges
        self.VoltageRatioInputsList_ErrorCallbackFiredFlag = [0.0] * self.NumberOfWheatstoneBridges

        self.VoltageRatioInputsList_VoltageRatio_Raw = [-11111.0] * self.NumberOfWheatstoneBridges
        self.VoltageRatioInputsList_VoltageRatio_Filtered = [-11111.0] * self.NumberOfWheatstoneBridges

        self.VoltageRatioInputsList_VoltageRatio_LowPassFilter_ReubenPython2and3ClassObject = list()

        self.VoltageRatioInputsList_VoltageRatio_Raw_ZeroOffsetValue = [0.0] * self.NumberOfWheatstoneBridges
        self.VoltageRatioInputsList_VoltageRatio_Filtered_ZeroOffsetValue = [0.0] * self.NumberOfWheatstoneBridges
        self.VoltageRatioInputsList_NeedsToBeZeroedFlag = [0] * self.NumberOfWheatstoneBridges

        self.VoltageRatioInputsList_NeedsToBeSnapshottedFlag = [0] * self.NumberOfWheatstoneBridges
        self.VoltageRatioInputsList_DataForSnapshottingBridge_EnableCollectionFlag = [0] * self.NumberOfWheatstoneBridges
        self.VoltageRatioInputsList_VoltageRatio_Raw_SnapshottedValue = [0.0] * self.NumberOfWheatstoneBridges
        self.VoltageRatioInputsList_VoltageRatio_Filtered_SnapshottedValue = [0.0] * self.NumberOfWheatstoneBridges

        ####
        #self.VoltageRatioInputsList_VoltageRatio_Raw_DataForSnapshottingBridgeQueue = [Queue.Queue()] * self.NumberOfWheatstoneBridges #THIS LINE DOESN'T WORK AS IT COUPLE ALL QUEUE VALUES TOGETHER ACROSS DIFFERENT CHANNELS
        self.VoltageRatioInputsList_VoltageRatio_Raw_DataForSnapshottingBridgeQueue = list()
        for VoltageRatioInputChannel in range(0, self.NumberOfWheatstoneBridges):
            self.VoltageRatioInputsList_VoltageRatio_Raw_DataForSnapshottingBridgeQueue.append(Queue.Queue())
        ####
        
        ####
        #self.VoltageRatioInputsList_VoltageRatio_Filtered_DataForSnapshottingBridgeQueue = [Queue.Queue()] * self.NumberOfWheatstoneBridges #THIS LINE DOESN'T WORK AS IT COUPLE ALL QUEUE VALUES TOGETHER ACROSS DIFFERENT CHANNELS
        self.VoltageRatioInputsList_VoltageRatio_Filtered_DataForSnapshottingBridgeQueue = list()
        for VoltageRatioInputChannel in range(0, self.NumberOfWheatstoneBridges):
            self.VoltageRatioInputsList_VoltageRatio_Filtered_DataForSnapshottingBridgeQueue.append(Queue.Queue())
        ####
        
        self.VoltageRatioInputsList_OnVoltageRatioChangeCallback_CurrentTime = [-11111.0] * self.NumberOfWheatstoneBridges
        self.VoltageRatioInputsList_OnVoltageRatioChangeCallback_StartingTime = [-11111.0] * self.NumberOfWheatstoneBridges
        self.VoltageRatioInputsList_OnVoltageRatioChangeCallback_LastTime = [-11111.0] * self.NumberOfWheatstoneBridges
        self.VoltageRatioInputsList_OnVoltageRatioChangeCallback_DataStreamingFrequency = [-11111.0] * self.NumberOfWheatstoneBridges
        self.VoltageRatioInputsList_OnVoltageRatioChangeCallback_DataStreamingDeltaT = [-11111.0] * self.NumberOfWheatstoneBridges

        self.VoltageRatioInputsList_EnabledStateBoolean_ReceivedFromBoard = [-11111.0] * self.NumberOfWheatstoneBridges
        self.VoltageRatioInputsList_BridgeGain_ActualIntegerValue_ReceivedFromBoard = [-11111.0] * self.NumberOfWheatstoneBridges
        self.VoltageRatioInputsList_BridgeGain_PhidgetsConstant_ReceivedFromBoard = [-11111.0] * self.NumberOfWheatstoneBridges
        self.VoltageRatioInputsList_CallbackUpdateDeltaTmilliseconds_ReceivedFromBoard = [-11111.0] * self.NumberOfWheatstoneBridges
        self.VoltageRatioInputsList_VoltageRatioChangeTrigger_ReceivedFromBoard = [-11111.0] * self.NumberOfWheatstoneBridges

        self.VoltageRatioInputsList_ListOfOnAttachCallbackFunctionNames = [self.VoltageRatioInput0onAttachCallback, self.VoltageRatioInput1onAttachCallback, self.VoltageRatioInput2onAttachCallback, self.VoltageRatioInput3onAttachCallback]
        self.VoltageRatioInputsList_ListOfOnDetachCallbackFunctionNames = [self.VoltageRatioInput0onDetachCallback, self.VoltageRatioInput1onDetachCallback, self.VoltageRatioInput2onDetachCallback, self.VoltageRatioInput3onDetachCallback]
        self.VoltageRatioInputsList_ListOfOnErrorCallbackFunctionNames = [self.VoltageRatioInput0onErrorCallback, self.VoltageRatioInput1onErrorCallback, self.VoltageRatioInput2onErrorCallback, self.VoltageRatioInput3onErrorCallback]
        self.VoltageRatioInputsList_ListOfOnVoltageRatioChangeCallbackFunctionNames = [self.VoltageRatioInput0onVoltageRatioChangeCallback, self.VoltageRatioInput1onVoltageRatioChangeCallback, self.VoltageRatioInput2onVoltageRatioChangeCallback, self.VoltageRatioInput3onVoltageRatioChangeCallback]

        self.BridgeGain_SupportedValuesDict_ActualIntegerValuesAsKeys = dict([(1, Phidget22.Devices.VoltageRatioInput.BridgeGain.BRIDGE_GAIN_1),
                                                      (8, Phidget22.Devices.VoltageRatioInput.BridgeGain.BRIDGE_GAIN_8),
                                                      (16, Phidget22.Devices.VoltageRatioInput.BridgeGain.BRIDGE_GAIN_16),
                                                      (32, Phidget22.Devices.VoltageRatioInput.BridgeGain.BRIDGE_GAIN_32),
                                                      (64, Phidget22.Devices.VoltageRatioInput.BridgeGain.BRIDGE_GAIN_64),
                                                      (128, Phidget22.Devices.VoltageRatioInput.BridgeGain.BRIDGE_GAIN_128)])

        #####
        self.BridgeGain_SupportedValuesDict_PhidgetConstantsAsKeys = dict()
        for key in self.BridgeGain_SupportedValuesDict_ActualIntegerValuesAsKeys:
            self.BridgeGain_SupportedValuesDict_PhidgetConstantsAsKeys[self.BridgeGain_SupportedValuesDict_ActualIntegerValuesAsKeys[key]] = key
        #####

        self.MostRecentDataDict = dict()
        #########################################################
        #########################################################
        
        #########################################################
        #########################################################
        if platform.system() == "Linux":

            if "raspberrypi" in platform.uname(): #os.uname() doesn't work in windows
                self.my_platform = "pi"
            else:
                self.my_platform = "linux"

        elif platform.system() == "Windows":
            self.my_platform = "windows"

        elif platform.system() == "Darwin":
            self.my_platform = "mac"

        else:
            self.my_platform = "other"

        print("Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class __init__: The OS platform is: " + self.my_platform)
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "GUIparametersDict" in setup_dict:
            self.GUIparametersDict = setup_dict["GUIparametersDict"]

            #########################################################
            if "USE_GUI_FLAG" in self.GUIparametersDict:
                self.USE_GUI_FLAG = self.PassThrough0and1values_ExitProgramOtherwise("USE_GUI_FLAG", self.GUIparametersDict["USE_GUI_FLAG"])
            else:
                self.USE_GUI_FLAG = 0

            print("Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class __init__: USE_GUI_FLAG: " + str(self.USE_GUI_FLAG))
            #########################################################

            #########################################################
            if "root" in self.GUIparametersDict:
                self.root = self.GUIparametersDict["root"]
            else:
                print("Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class __init__: Error, must pass in 'root'")
                return
            #########################################################

            #########################################################
            if "EnableInternal_MyPrint_Flag" in self.GUIparametersDict:
                self.EnableInternal_MyPrint_Flag = self.PassThrough0and1values_ExitProgramOtherwise("EnableInternal_MyPrint_Flag", self.GUIparametersDict["EnableInternal_MyPrint_Flag"])
            else:
                self.EnableInternal_MyPrint_Flag = 0

            print("Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class __init__: EnableInternal_MyPrint_Flag: " + str(self.EnableInternal_MyPrint_Flag))
            #########################################################

            #########################################################
            if "PrintToConsoleFlag" in self.GUIparametersDict:
                self.PrintToConsoleFlag = self.PassThrough0and1values_ExitProgramOtherwise("PrintToConsoleFlag", self.GUIparametersDict["PrintToConsoleFlag"])
            else:
                self.PrintToConsoleFlag = 1

            print("Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class __init__: PrintToConsoleFlag: " + str(self.PrintToConsoleFlag))
            #########################################################

            #########################################################
            if "NumberOfPrintLines" in self.GUIparametersDict:
                self.NumberOfPrintLines = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("NumberOfPrintLines", self.GUIparametersDict["NumberOfPrintLines"], 0.0, 50.0))
            else:
                self.NumberOfPrintLines = 10

            print("Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class __init__: NumberOfPrintLines: " + str(self.NumberOfPrintLines))
            #########################################################

            #########################################################
            if "UseBorderAroundThisGuiObjectFlag" in self.GUIparametersDict:
                self.UseBorderAroundThisGuiObjectFlag = self.PassThrough0and1values_ExitProgramOtherwise("UseBorderAroundThisGuiObjectFlag", self.GUIparametersDict["UseBorderAroundThisGuiObjectFlag"])
            else:
                self.UseBorderAroundThisGuiObjectFlag = 0

            print("Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class __init__: UseBorderAroundThisGuiObjectFlag: " + str(self.UseBorderAroundThisGuiObjectFlag))
            #########################################################

            #########################################################
            if "GUI_ROW" in self.GUIparametersDict:
                self.GUI_ROW = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_ROW", self.GUIparametersDict["GUI_ROW"], 0.0, 1000.0))
            else:
                self.GUI_ROW = 0

            print("Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class __init__: GUI_ROW: " + str(self.GUI_ROW))
            #########################################################

            #########################################################
            if "GUI_COLUMN" in self.GUIparametersDict:
                self.GUI_COLUMN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_COLUMN", self.GUIparametersDict["GUI_COLUMN"], 0.0, 1000.0))
            else:
                self.GUI_COLUMN = 0

            print("Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class __init__: GUI_COLUMN: " + str(self.GUI_COLUMN))
            #########################################################

            #########################################################
            if "GUI_PADX" in self.GUIparametersDict:
                self.GUI_PADX = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_PADX", self.GUIparametersDict["GUI_PADX"], 0.0, 1000.0))
            else:
                self.GUI_PADX = 1

            print("Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class __init__: GUI_PADX: " + str(self.GUI_PADX))
            #########################################################

            #########################################################
            if "GUI_PADY" in self.GUIparametersDict:
                self.GUI_PADY = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_PADY", self.GUIparametersDict["GUI_PADY"], 0.0, 1000.0))
            else:
                self.GUI_PADY = 1

            print("Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class __init__: GUI_PADY: " + str(self.GUI_PADY))
            #########################################################

            #########################################################
            if "GUI_ROWSPAN" in self.GUIparametersDict:
                self.GUI_ROWSPAN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_ROWSPAN", self.GUIparametersDict["GUI_ROWSPAN"], 1.0, 1000.0))
            else:
                self.GUI_ROWSPAN = 1

            print("Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class __init__: GUI_ROWSPAN: " + str(self.GUI_ROWSPAN))
            #########################################################

            #########################################################
            if "GUI_COLUMNSPAN" in self.GUIparametersDict:
                self.GUI_COLUMNSPAN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_COLUMNSPAN", self.GUIparametersDict["GUI_COLUMNSPAN"], 1.0, 1000.0))
            else:
                self.GUI_COLUMNSPAN = 1

            print("Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class __init__: GUI_COLUMNSPAN: " + str(self.GUI_COLUMNSPAN))
            #########################################################

            #########################################################
            if "GUI_STICKY" in self.GUIparametersDict:
                self.GUI_STICKY = str(self.GUIparametersDict["GUI_STICKY"])
            else:
                self.GUI_STICKY = "w"

            print("Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class __init__: GUI_STICKY: " + str(self.GUI_STICKY))
            #########################################################

        else:
            self.GUIparametersDict = dict()
            self.USE_GUI_FLAG = 0
            print("Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class __init__: No GUIparametersDict present, setting USE_GUI_FLAG: " + str(self.USE_GUI_FLAG))

        #print("Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class __init__: GUIparametersDict: " + str(self.GUIparametersDict))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "DesiredSerialNumber" in setup_dict:
            try:
                self.DesiredSerialNumber = int(setup_dict["DesiredSerialNumber"])
            except:
                print("Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class __init__: Error, DesiredSerialNumber invalid.")
        else:
            self.DesiredSerialNumber = -1
        
        print("Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class __init__: DesiredSerialNumber: " + str(self.DesiredSerialNumber))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "NameToDisplay_UserSet" in setup_dict:
            self.NameToDisplay_UserSet = str(setup_dict["NameToDisplay_UserSet"])
        else:
            self.NameToDisplay_UserSet = ""

        print("Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class __init__: NameToDisplay_UserSet: " + str(self.NameToDisplay_UserSet))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "WaitForAttached_TimeoutDuration_Milliseconds" in setup_dict:
            self.WaitForAttached_TimeoutDuration_Milliseconds = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("WaitForAttached_TimeoutDuration_Milliseconds", setup_dict["WaitForAttached_TimeoutDuration_Milliseconds"], 0.0, 60000.0))

        else:
            self.WaitForAttached_TimeoutDuration_Milliseconds = 5000

        print("Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class __init__: WaitForAttached_TimeoutDuration_Milliseconds: " + str(self.WaitForAttached_TimeoutDuration_Milliseconds))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "UsePhidgetsLoggingInternalToThisClassObjectFlag" in setup_dict:
            self.UsePhidgetsLoggingInternalToThisClassObjectFlag = self.PassThrough0and1values_ExitProgramOtherwise("UsePhidgetsLoggingInternalToThisClassObjectFlag", setup_dict["UsePhidgetsLoggingInternalToThisClassObjectFlag"])
        else:
            self.UsePhidgetsLoggingInternalToThisClassObjectFlag = 1

        print("Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class __init__: UsePhidgetsLoggingInternalToThisClassObjectFlag: " + str(self.UsePhidgetsLoggingInternalToThisClassObjectFlag))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "VoltageRatioInputsList_EnabledStateBoolean" in setup_dict:
            VoltageRatioInputsList_EnabledStateBoolean_TEMP = setup_dict["VoltageRatioInputsList_EnabledStateBoolean"]

            if self.IsInputList(VoltageRatioInputsList_EnabledStateBoolean_TEMP) == 1 and len(VoltageRatioInputsList_EnabledStateBoolean_TEMP) == self.NumberOfWheatstoneBridges:

                self.VoltageRatioInputsList_EnabledStateBoolean = list()
                for VoltageRatioInputChannel, EnabledState_TEMP in enumerate(VoltageRatioInputsList_EnabledStateBoolean_TEMP):
                    EnabledState = int(self.PassThrough0and1values_ExitProgramOtherwise("VoltageRatioInputsList_EnabledStateBoolean, VoltageRatioInputChannel " + str(VoltageRatioInputChannel), EnabledState_TEMP))
                    self.VoltageRatioInputsList_EnabledStateBoolean.append(EnabledState)
            else:
                print("Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class __init__: Error, 'VoltageRatioInputsList_EnabledStateBoolean' must be length " + str(len(self.NumberOfWheatstoneBridges)))
                return
        else:
            self.VoltageRatioInputsList_EnabledStateBoolean = [1]*self.NumberOfWheatstoneBridges

        print("Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class __init__: VoltageRatioInputsList_EnabledStateBoolean: " + str(self.VoltageRatioInputsList_EnabledStateBoolean))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "VoltageRatioInputsList_BridgeGain_ActualIntegerValue" in setup_dict:
            VoltageRatioInputsList_BridgeGain_TEMP = setup_dict["VoltageRatioInputsList_BridgeGain_ActualIntegerValue"]
            
            if self.IsInputList(VoltageRatioInputsList_BridgeGain_TEMP) == 1 and len(VoltageRatioInputsList_BridgeGain_TEMP) == self.NumberOfWheatstoneBridges:
                self.VoltageRatioInputsList_BridgeGain_ActualIntegerValue = list()
                self.VoltageRatioInputsList_BridgeGain_PhidgetsConstant = list()
                
                for VoltageRatioInputChannel, BridgeGain_TEMP in enumerate(VoltageRatioInputsList_BridgeGain_TEMP):
                    BridgeGain = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("VoltageRatioInputsList_BridgeGain, VoltageRatioInputChannel " + str(VoltageRatioInputChannel), BridgeGain_TEMP, 1, 128))

                    if BridgeGain in self.BridgeGain_SupportedValuesDict_ActualIntegerValuesAsKeys:
                        self.VoltageRatioInputsList_BridgeGain_ActualIntegerValue.append(BridgeGain)
                        self.VoltageRatioInputsList_BridgeGain_PhidgetsConstant.append(self.BridgeGain_SupportedValuesDict_ActualIntegerValuesAsKeys[BridgeGain])
                    else:

                        ###
                        SetToPrint = "["
                        for key in self.BridgeGain_SupportedValuesDict_ActualIntegerValuesAsKeys:
                            SetToPrint = SetToPrint + str(key) + ", "
                        SetToPrint = SetToPrint[:-2] + "]"
                        ###

                        print("Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class __init__: Error, 'VoltageRatioInputsList_BridgeGain' must be in the set " + SetToPrint)
                        return
            else:
                print("Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class __init__: Error, 'VoltageRatioInputsList_BridgeGain' must be a length " + str(len(self.NumberOfWheatstoneBridges)))
                return
        else:
            self.VoltageRatioInputsList_BridgeGain_ActualIntegerValue = [1]*self.NumberOfWheatstoneBridges
            self.VoltageRatioInputsList_BridgeGain_PhidgetsConstant = [1]*self.NumberOfWheatstoneBridges

        print("Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class __init__: VoltageRatioInputsList_BridgeGain: " + str(self.VoltageRatioInputsList_BridgeGain_ActualIntegerValue))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "VoltageRatioInputsList_VoltageRatio_LowPassFilter_Lambda" in setup_dict:
            VoltageRatioInputsList_VoltageRatio_LowPassFilter_Lambda_TEMP = setup_dict["VoltageRatioInputsList_VoltageRatio_LowPassFilter_Lambda"]
            if self.IsInputList(VoltageRatioInputsList_VoltageRatio_LowPassFilter_Lambda_TEMP) == 1 and len(VoltageRatioInputsList_VoltageRatio_LowPassFilter_Lambda_TEMP) == self.NumberOfWheatstoneBridges:
                self.VoltageRatioInputsList_VoltageRatio_LowPassFilter_Lambda = list()
                for VoltageRatioInputChannel, SpeedExponentialFilterLambda_TEMP in enumerate(VoltageRatioInputsList_VoltageRatio_LowPassFilter_Lambda_TEMP):
                    SpeedExponentialFilterLambda = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("VoltageRatioInputsList_VoltageRatio_LowPassFilter_Lambda, VoltageRatioInputChannel " + str(VoltageRatioInputChannel), SpeedExponentialFilterLambda_TEMP, 0.0, 1.0)
                    self.VoltageRatioInputsList_VoltageRatio_LowPassFilter_Lambda.append(SpeedExponentialFilterLambda)
            else:
                print("Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class __init__: Error, 'VoltageRatioInputsList_VoltageRatio_LowPassFilter_Lambda' must be a length " + str(len(self.NumberOfWheatstoneBridges)))
                return
        else:
            self.VoltageRatioInputsList_VoltageRatio_LowPassFilter_Lambda = [1.0]*self.NumberOfWheatstoneBridges #Default to no filtering, new_filtered_value = k * raw_sensor_value + (1 - k) * old_filtered_value

        print("Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class __init__: VoltageRatioInputsList_VoltageRatio_LowPassFilter_Lambda: " + str(self.VoltageRatioInputsList_VoltageRatio_LowPassFilter_Lambda))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "VoltageRatioInputsList_VoltageRatioChangeTrigger" in setup_dict:
            VoltageRatioInputsList_VoltageRatioChangeTrigger_TEMP = setup_dict["VoltageRatioInputsList_VoltageRatioChangeTrigger"]
            if self.IsInputList(VoltageRatioInputsList_VoltageRatioChangeTrigger_TEMP) == 1 and len(VoltageRatioInputsList_VoltageRatioChangeTrigger_TEMP) == self.NumberOfWheatstoneBridges:
                self.VoltageRatioInputsList_VoltageRatioChangeTrigger = list()
                for VoltageRatioInputChannel, VoltageRatioChangeTrigger_TEMP in enumerate(VoltageRatioInputsList_VoltageRatioChangeTrigger_TEMP):
                    VoltageRatioChangeTrigger = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("VoltageRatioInputsList_VoltageRatioChangeTrigger, VoltageRatioInputChannel " + str(VoltageRatioInputChannel), VoltageRatioChangeTrigger_TEMP, 0.0, 1.0)
                    self.VoltageRatioInputsList_VoltageRatioChangeTrigger.append(VoltageRatioChangeTrigger)
            else:
                print("Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class __init__: Error, 'VoltageRatioInputsList_VoltageRatioChangeTrigger' must be a length " + str(len(self.NumberOfWheatstoneBridges)))
                return
        else:
            self.VoltageRatioInputsList_VoltageRatioChangeTrigger = [1.0]*self.NumberOfWheatstoneBridges

        print("Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class __init__: VoltageRatioInputsList_VoltageRatioChangeTrigger: " + str(self.VoltageRatioInputsList_VoltageRatioChangeTrigger))
        #########################################################
        #########################################################
        
        #########################################################
        #########################################################
        if "DataCollectionDurationInSecondsForSnapshottingBridge" in setup_dict:
            self.DataCollectionDurationInSecondsForSnapshottingBridge = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("DataCollectionDurationInSecondsForSnapshottingBridge", setup_dict["DataCollectionDurationInSecondsForSnapshottingBridge"], 0.0, 60.0)

        else:
            self.DataCollectionDurationInSecondsForSnapshottingBridge = 1.0

        print("Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class __init__: DataCollectionDurationInSecondsForSnapshottingBridge: " + str(self.DataCollectionDurationInSecondsForSnapshottingBridge))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "MainThread_TimeToSleepEachLoop" in setup_dict:
            self.MainThread_TimeToSleepEachLoop = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("MainThread_TimeToSleepEachLoop", setup_dict["MainThread_TimeToSleepEachLoop"], 0.001, 100000)

        else:
            self.MainThread_TimeToSleepEachLoop = 0.008

        print("Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class __init__: MainThread_TimeToSleepEachLoop: " + str(self.MainThread_TimeToSleepEachLoop))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        try:
            
            for VoltageRatioInputChannel in range(0, self.NumberOfWheatstoneBridges):
                self.VoltageRatioInputsList_VoltageRatio_LowPassFilter_ReubenPython2and3ClassObject.append(LowPassFilter_ReubenPython2and3Class(dict([("UseMedianFilterFlag", 0),
                                                                                                                ("UseExponentialSmoothingFilterFlag", 1),
                                                                                                                ("ExponentialSmoothingFilterLambda", self.VoltageRatioInputsList_VoltageRatio_LowPassFilter_Lambda[VoltageRatioInputChannel])])))
                time.sleep(0.1)
                LOWPASSFILTER_OPEN_FLAG = self.VoltageRatioInputsList_VoltageRatio_LowPassFilter_ReubenPython2and3ClassObject[VoltageRatioInputChannel].OBJECT_CREATED_SUCCESSFULLY_FLAG
    
                if LOWPASSFILTER_OPEN_FLAG != 1:
                    print("Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class __init__: Failed to open LowPassFilter_ReubenPython2and3ClassObject.")
                    return

        except:
            exceptions = sys.exc_info()[0]
            print("Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class __init__: Exceptions: %s" % exceptions)
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.PrintToGui_Label_TextInputHistory_List = [" "]*self.NumberOfPrintLines
        self.PrintToGui_Label_TextInput_Str = ""
        self.GUI_ready_to_be_updated_flag = 0
        #########################################################
        #########################################################

        ######################################################### MUST OPEN THE DEVICE BEFORE WE CAN QUERY ITS INFORMATION
        #########################################################
        try:
            VoltageRatioInput_OpenedTemporarilyJustToGetDeviceInfo = VoltageRatioInput()

            if self.DesiredSerialNumber != -1:
                VoltageRatioInput_OpenedTemporarilyJustToGetDeviceInfo.setDeviceSerialNumber(self.DesiredSerialNumber)

            VoltageRatioInput_OpenedTemporarilyJustToGetDeviceInfo.setChannel(0)
            VoltageRatioInput_OpenedTemporarilyJustToGetDeviceInfo.openWaitForAttachment(self.WaitForAttached_TimeoutDuration_Milliseconds)

            self.DetectedDeviceName = VoltageRatioInput_OpenedTemporarilyJustToGetDeviceInfo.getDeviceName()
            print("Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class __init__: DetectedDeviceName: " + self.DetectedDeviceName)

            self.DetectedDeviceSerialNumber = VoltageRatioInput_OpenedTemporarilyJustToGetDeviceInfo.getDeviceSerialNumber()
            print("Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class __init__: DetectedDeviceSerialNumber: " + str(self.DetectedDeviceSerialNumber))

            self.DetectedDeviceID = VoltageRatioInput_OpenedTemporarilyJustToGetDeviceInfo.getDeviceID()
            print("Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class __init__: DetectedDeviceID: " + str(self.DetectedDeviceID))

            self.DetectedDeviceVersion = VoltageRatioInput_OpenedTemporarilyJustToGetDeviceInfo.getDeviceVersion()
            print("Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class __init__: DetectedDeviceVersion: " + str(self.DetectedDeviceVersion))

            self.DetectedDeviceLibraryVersion = VoltageRatioInput_OpenedTemporarilyJustToGetDeviceInfo.getLibraryVersion()
            print("Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class __init__: DetectedDeviceLibraryVersion: " + str(self.DetectedDeviceLibraryVersion))

            VoltageRatioInput_OpenedTemporarilyJustToGetDeviceInfo.close()

        except PhidgetException as e:
            print("Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class __init__: Failed to call Device Information, Phidget Exception %i: %s" % (e.code, e.details))
            return
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if self.DesiredSerialNumber != -1: #'-1' means we should open the device regardless os serial number.
            if self.DetectedDeviceSerialNumber != self.DesiredSerialNumber:
                print("Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class __init__: The desired Serial Number (" + str(self.DesiredSerialNumber) + ") does not match the detected serial number (" + str(self.DetectedDeviceSerialNumber) + ").")
                return
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        try:

            '''
            ########### DetectedDeviceID is not currently differentiating.
            if self.DetectedDeviceID == 24:
                self.CallbackUpdateDeltaTmilliseconds_MinimumValue = 8
            elif self.DetectedDeviceID  == 24:
                self.CallbackUpdateDeltaTmilliseconds_MinimumValue = 1
            else:
                self.CallbackUpdateDeltaTmilliseconds_MinimumValue = 8
            print("Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class __init__: self.CallbackUpdateDeltaTmilliseconds_MinimumValue: " + str(self.CallbackUpdateDeltaTmilliseconds_MinimumValue))
            ##########
            '''

            ########## DetectedDeviceVersion differentiates but isn't long-term, reliable method.
            if str(self.DetectedDeviceVersion)[0] == "1":
                self.CallbackUpdateDeltaTmilliseconds_MinimumValue = 8
            elif str(self.DetectedDeviceVersion)[0]  == "2":
                self.CallbackUpdateDeltaTmilliseconds_MinimumValue = 1
            else:
                self.CallbackUpdateDeltaTmilliseconds_MinimumValue = 8
            print("Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class __init__: self.CallbackUpdateDeltaTmilliseconds_MinimumValue: " + str(self.CallbackUpdateDeltaTmilliseconds_MinimumValue))
            ##########

            ##########
            if "VoltageRatioInputsList_CallbackUpdateDeltaTmilliseconds" in setup_dict:
                VoltageRatioInputsList_CallbackUpdateDeltaTmilliseconds_TEMP = setup_dict["VoltageRatioInputsList_CallbackUpdateDeltaTmilliseconds"]

                if self.IsInputList(VoltageRatioInputsList_CallbackUpdateDeltaTmilliseconds_TEMP) == 1 and len(VoltageRatioInputsList_CallbackUpdateDeltaTmilliseconds_TEMP) == self.NumberOfWheatstoneBridges:

                    self.VoltageRatioInputsList_CallbackUpdateDeltaTmilliseconds = list()
                    for VoltageRatioInputChannel, CallbackUpdateDeltaTmilliseconds_TEMP in enumerate(VoltageRatioInputsList_CallbackUpdateDeltaTmilliseconds_TEMP):
                        CallbackUpdateDeltaTmilliseconds = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("VoltageRatioInputsList_CallbackUpdateDeltaTmilliseconds, VoltageRatioInputChannel " + str(VoltageRatioInputChannel), CallbackUpdateDeltaTmilliseconds_TEMP, self.CallbackUpdateDeltaTmilliseconds_MinimumValue, 1000.0))
                        self.VoltageRatioInputsList_CallbackUpdateDeltaTmilliseconds.append(CallbackUpdateDeltaTmilliseconds)
                else:
                    print("Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class __init__: Error, 'VoltageRatioInputsList_CallbackUpdateDeltaTmilliseconds' must be length " + str(len(self.NumberOfWheatstoneBridges)))
                    return
            else:
                self.VoltageRatioInputsList_CallbackUpdateDeltaTmilliseconds = [self.CallbackUpdateDeltaTmilliseconds_MinimumValue] * self.NumberOfWheatstoneBridges

            print("Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class __init__: VoltageRatioInputsList_CallbackUpdateDeltaTmilliseconds: " + str(self.VoltageRatioInputsList_CallbackUpdateDeltaTmilliseconds))
            ##########

        except:
            exceptions = sys.exc_info()[0]
            print("Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class __init__: Error, VoltageRatioInputsList_CallbackUpdateDeltaTmilliseconds parsing Exceptions: %s" % exceptions)
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        try:

            #########################################################
            for VoltageRatioInputChannel in range(0, self.NumberOfWheatstoneBridges):
                print("Creating VoltageRatioInputChannel: " + str(VoltageRatioInputChannel))
                self.VoltageRatioInputsList_PhidgetsVoltageRatioInputObjects.append(VoltageRatioInput())

                if self.DesiredSerialNumber != -1:
                    self.VoltageRatioInputsList_PhidgetsVoltageRatioInputObjects[VoltageRatioInputChannel].setDeviceSerialNumber(self.DesiredSerialNumber)

                self.VoltageRatioInputsList_PhidgetsVoltageRatioInputObjects[VoltageRatioInputChannel].setChannel(VoltageRatioInputChannel)
                self.VoltageRatioInputsList_PhidgetsVoltageRatioInputObjects[VoltageRatioInputChannel].setOnAttachHandler(self.VoltageRatioInputsList_ListOfOnAttachCallbackFunctionNames[VoltageRatioInputChannel])
                self.VoltageRatioInputsList_PhidgetsVoltageRatioInputObjects[VoltageRatioInputChannel].setOnDetachHandler(self.VoltageRatioInputsList_ListOfOnDetachCallbackFunctionNames[VoltageRatioInputChannel])
                self.VoltageRatioInputsList_PhidgetsVoltageRatioInputObjects[VoltageRatioInputChannel].setOnErrorHandler(self.VoltageRatioInputsList_ListOfOnErrorCallbackFunctionNames[VoltageRatioInputChannel])
                self.VoltageRatioInputsList_PhidgetsVoltageRatioInputObjects[VoltageRatioInputChannel].setOnVoltageRatioChangeHandler(self.VoltageRatioInputsList_ListOfOnVoltageRatioChangeCallbackFunctionNames[VoltageRatioInputChannel])
                self.VoltageRatioInputsList_PhidgetsVoltageRatioInputObjects[VoltageRatioInputChannel].openWaitForAttachment(self.WaitForAttached_TimeoutDuration_Milliseconds)
            #########################################################
        
            self.PhidgetsDeviceConnectedFlag = 1

        except PhidgetException as e:
            self.PhidgetsDeviceConnectedFlag = 0
            print("Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class __init__: Failed to attach, Phidget Exception %i: %s" % (e.code, e.details))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if self.PhidgetsDeviceConnectedFlag == 1:

            #########################################################
            if self.UsePhidgetsLoggingInternalToThisClassObjectFlag == 1:
                try:
                    Log.enable(LogLevel.PHIDGET_LOG_INFO, os.getcwd() + "\Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class_PhidgetLog_INFO.txt")
                    print("Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class __init__: Enabled Phidget Logging.")
                except PhidgetException as e:
                    print("Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class __init__: Failed to enable Phidget Logging, Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################

            #########################################################
            self.MainThread_ThreadingObject = threading.Thread(target=self.MainThread, args=())
            self.MainThread_ThreadingObject.start()
            #########################################################

            #########################################################
            if self.USE_GUI_FLAG == 1:
                self.StartGUI(self.root)
            #########################################################

            #########################################################
            time.sleep(0.25)
            #########################################################

            #########################################################
            self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 1
            #########################################################

        #########################################################
        #########################################################

    #######################################################################################################################
    #######################################################################################################################

    #######################################################################################################################
    #######################################################################################################################
    def __del__(self):
        pass
    #######################################################################################################################
    #######################################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def PassThrough0and1values_ExitProgramOtherwise(self, InputNameString, InputNumber):

        try:
            InputNumber_ConvertedToFloat = float(InputNumber)
        except:
            exceptions = sys.exc_info()[0]
            print("PassThrough0and1values_ExitProgramOtherwise Error. InputNumber must be a float value, Exceptions: %s" % exceptions)
            input("Press any key to continue")
            sys.exit()

        try:
            if InputNumber_ConvertedToFloat == 0.0 or InputNumber_ConvertedToFloat == 1:
                return InputNumber_ConvertedToFloat
            else:
                input("PassThrough0and1values_ExitProgramOtherwise Error. '" +
                          InputNameString +
                          "' must be 0 or 1 (value was " +
                          str(InputNumber_ConvertedToFloat) +
                          "). Press any key (and enter) to exit.")

                sys.exit()
        except:
            exceptions = sys.exc_info()[0]
            print("PassThrough0and1values_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)
            input("Press any key to continue")
            sys.exit()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def PassThroughFloatValuesInRange_ExitProgramOtherwise(self, InputNameString, InputNumber, RangeMinValue, RangeMaxValue):
        try:
            InputNumber_ConvertedToFloat = float(InputNumber)
        except:
            exceptions = sys.exc_info()[0]
            print("PassThroughFloatValuesInRange_ExitProgramOtherwise Error. InputNumber must be a float value, Exceptions: %s" % exceptions)
            input("Press any key to continue")
            sys.exit()

        try:
            if InputNumber_ConvertedToFloat >= RangeMinValue and InputNumber_ConvertedToFloat <= RangeMaxValue:
                return InputNumber_ConvertedToFloat
            else:
                input("PassThroughFloatValuesInRange_ExitProgramOtherwise Error. '" +
                          InputNameString +
                          "' must be in the range [" +
                          str(RangeMinValue) +
                          ", " +
                          str(RangeMaxValue) +
                          "] (value was " +
                          str(InputNumber_ConvertedToFloat) + "). Press any key (and enter) to exit.")

                sys.exit()
        except:
            exceptions = sys.exc_info()[0]
            print("PassThroughFloatValuesInRange_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)
            input("Press any key to continue")
            sys.exit()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def TellWhichFileWereIn(self):

        #We used to use this method, but it gave us the root calling file, not the class calling file
        #absolute_file_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        #filename = absolute_file_path[absolute_file_path.rfind("\\") + 1:]

        frame = inspect.stack()[1]
        filename = frame[1][frame[1].rfind("\\") + 1:]
        filename = filename.replace(".py","")

        return filename
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def VoltageRatioInputGENERALonAttachCallback(self, VoltageRatioInputChannel):

        try:
            ##############################
            self.VoltageRatioInputsList_PhidgetsVoltageRatioInputObjects[VoltageRatioInputChannel].setDataInterval(self.VoltageRatioInputsList_CallbackUpdateDeltaTmilliseconds[VoltageRatioInputChannel])
            #self.VoltageRatioInputsList_PhidgetsVoltageRatioInputObjects[VoltageRatioInputChannel].setDataRate()

            self.VoltageRatioInputsList_PhidgetsVoltageRatioInputObjects[VoltageRatioInputChannel].setBridgeGain(self.VoltageRatioInputsList_BridgeGain_PhidgetsConstant[VoltageRatioInputChannel])
            self.VoltageRatioInputsList_PhidgetsVoltageRatioInputObjects[VoltageRatioInputChannel].setBridgeEnabled(self.VoltageRatioInputsList_EnabledStateBoolean[VoltageRatioInputChannel])
            print("self.VoltageRatioInputsList_VoltageRatioChangeTrigger[VoltageRatioInputChannel]: " + str(self.VoltageRatioInputsList_VoltageRatioChangeTrigger[VoltageRatioInputChannel]))
            self.VoltageRatioInputsList_PhidgetsVoltageRatioInputObjects[VoltageRatioInputChannel].setVoltageRatioChangeTrigger(self.VoltageRatioInputsList_VoltageRatioChangeTrigger[VoltageRatioInputChannel])

            self.VoltageRatioInputsList_EnabledStateBoolean_ReceivedFromBoard[VoltageRatioInputChannel] = self.VoltageRatioInputsList_PhidgetsVoltageRatioInputObjects[VoltageRatioInputChannel].getBridgeEnabled()
            self.VoltageRatioInputsList_BridgeGain_PhidgetsConstant_ReceivedFromBoard[VoltageRatioInputChannel] = self.VoltageRatioInputsList_PhidgetsVoltageRatioInputObjects[VoltageRatioInputChannel].getBridgeGain()
            self.VoltageRatioInputsList_CallbackUpdateDeltaTmilliseconds_ReceivedFromBoard[VoltageRatioInputChannel] = self.VoltageRatioInputsList_PhidgetsVoltageRatioInputObjects[VoltageRatioInputChannel].getDataInterval()
            self.VoltageRatioInputsList_BridgeGain_ActualIntegerValue_ReceivedFromBoard[VoltageRatioInputChannel] = self.BridgeGain_SupportedValuesDict_PhidgetConstantsAsKeys[self.VoltageRatioInputsList_BridgeGain_PhidgetsConstant_ReceivedFromBoard[VoltageRatioInputChannel]]
            self.VoltageRatioInputsList_VoltageRatioChangeTrigger_ReceivedFromBoard[VoltageRatioInputChannel] = self.VoltageRatioInputsList_PhidgetsVoltageRatioInputObjects[VoltageRatioInputChannel].getVoltageRatioChangeTrigger()

            self.MyPrint_WithoutLogFile("VoltageRatioInputGENERALonAttachCallback event, VoltageRatioInputChannel " +
                                        str(VoltageRatioInputChannel) +
                                        ", Enabled: " +
                                        str(self.VoltageRatioInputsList_EnabledStateBoolean_ReceivedFromBoard[VoltageRatioInputChannel]) +
                                        ", Bridge Gain: " +
                                        str(self.VoltageRatioInputsList_BridgeGain_PhidgetsConstant_ReceivedFromBoard[VoltageRatioInputChannel]) +
                                        ", DataInterval: " +
                                        str(self.VoltageRatioInputsList_CallbackUpdateDeltaTmilliseconds_ReceivedFromBoard[VoltageRatioInputChannel]) +
                                        ", VoltageRatioChangeTrigger: " +
                                        str(self.VoltageRatioInputsList_VoltageRatioChangeTrigger_ReceivedFromBoard[VoltageRatioInputChannel]))
            ##############################

            self.VoltageRatioInputsList_AttachedAndOpenFlag[VoltageRatioInputChannel] = 1
            
            self.MyPrint_WithoutLogFile("$$$$$$$$$$ VoltageRatioInputGENERALonAttachCallback event for VoltageRatioInputChannel " +
                                        str(VoltageRatioInputChannel) +
                                        ", Attached! $$$$$$$$$$")

        except PhidgetException as e:
            self.VoltageRatioInputsList_AttachedAndOpenFlag[VoltageRatioInputChannel] = 0
            self.MyPrint_WithoutLogFile("VoltageRatioInputGENERALonAttachCallback event for VoltageRatioInputChannel " + str(VoltageRatioInputChannel) + ", ERROR: Failed to attach, Phidget Exception %i: %s" % (e.code, e.details))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def VoltageRatioInputGENERALonDetachCallback(self, VoltageRatioInputChannel):

        self.VoltageRatioInputsList_AttachedAndOpenFlag[VoltageRatioInputChannel] = 0

        self.MyPrint_WithoutLogFile("$$$$$$$$$$ VoltageRatioInputGENERALonDetachCallback event for VoltageRatioInputChannel " +
                                    str(VoltageRatioInputChannel) +
                                    ", Detatched! $$$$$$$$$$")

        try:
            self.VoltageRatioInputsList_PhidgetsVoltageRatioInputObjects[VoltageRatioInputChannel].openWaitForAttachment(self.WaitForAttached_TimeoutDuration_Milliseconds)
            time.sleep(0.250)

        except PhidgetException as e:
            self.MyPrint_WithoutLogFile("VoltageRatioInputGENERALonDetachCallback event for Channel " + str(VoltageRatioInputChannel) + ", failed to openWaitForAttachment, Phidget Exception %i: %s" % (e.code, e.details))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def VoltageRatioInputGENERALonVoltageRatioChangeCallback(self, VoltageRatioInputChannel, VoltageRatio):

        ################################
        if self.VoltageRatioInputsList_OnVoltageRatioChangeCallback_StartingTime[VoltageRatioInputChannel] == -11111.0: #Set value on first callback firing
            self.VoltageRatioInputsList_OnVoltageRatioChangeCallback_StartingTime[VoltageRatioInputChannel] = self.getPreciseSecondsTimeStampString()
        ################################

        ################################
        self.VoltageRatioInputsList_OnVoltageRatioChangeCallback_CurrentTime[VoltageRatioInputChannel]  = self.getPreciseSecondsTimeStampString() - self.VoltageRatioInputsList_OnVoltageRatioChangeCallback_StartingTime[VoltageRatioInputChannel]
        self.UpdateFrequencyCalculation_OnVoltageRatioChangeCallback(VoltageRatioInputChannel)
        ################################

        ################################
        RawWITHOUT_ZeroOffset_TEMP = VoltageRatio
        self.VoltageRatioInputsList_VoltageRatio_Raw[VoltageRatioInputChannel] = RawWITHOUT_ZeroOffset_TEMP - self.VoltageRatioInputsList_VoltageRatio_Raw_ZeroOffsetValue[VoltageRatioInputChannel]

        #We feed in "RawWITHOUT_ZeroOffset_TEMP" so that we can maintain a separate filtered vs raw zero value.
        FilteredWITHOUT_ZeroOffset_TEMP = self.VoltageRatioInputsList_VoltageRatio_LowPassFilter_ReubenPython2and3ClassObject[VoltageRatioInputChannel].AddDataPointFromExternalProgram(RawWITHOUT_ZeroOffset_TEMP)["SignalOutSmoothed"]
        self.VoltageRatioInputsList_VoltageRatio_Filtered[VoltageRatioInputChannel] = FilteredWITHOUT_ZeroOffset_TEMP - self.VoltageRatioInputsList_VoltageRatio_Filtered_ZeroOffsetValue[VoltageRatioInputChannel]
        ################################

        ################################ unicorn
        if self.VoltageRatioInputsList_DataForSnapshottingBridge_EnableCollectionFlag[VoltageRatioInputChannel] == 1:

            if self.VoltageRatioInputsList_NeedsToBeZeroedFlag[VoltageRatioInputChannel] == 0: #Collecting data AS IS (without caring if we're trying to find the zero value).
                self.VoltageRatioInputsList_VoltageRatio_Raw_DataForSnapshottingBridgeQueue[VoltageRatioInputChannel].put(self.VoltageRatioInputsList_VoltageRatio_Raw[VoltageRatioInputChannel])
                self.VoltageRatioInputsList_VoltageRatio_Filtered_DataForSnapshottingBridgeQueue[VoltageRatioInputChannel].put(self.VoltageRatioInputsList_VoltageRatio_Filtered[VoltageRatioInputChannel])
            else:
                self.VoltageRatioInputsList_VoltageRatio_Raw_DataForSnapshottingBridgeQueue[VoltageRatioInputChannel].put(RawWITHOUT_ZeroOffset_TEMP)
                self.VoltageRatioInputsList_VoltageRatio_Filtered_DataForSnapshottingBridgeQueue[VoltageRatioInputChannel].put(FilteredWITHOUT_ZeroOffset_TEMP)
        ################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def VoltageRatioInputGENERALonErrorCallback(self, VoltageRatioInputChannel, code, description):

        self.VoltageRatioInputsList_ErrorCallbackFiredFlag[VoltageRatioInputChannel] = 1

        self.MyPrint_WithoutLogFile("VoltageRatioInputGENERALonErrorCallback event for Channel " + str(VoltageRatioInputChannel) + ", Error Code " + ErrorEventCode.getName(code) + ", description: " + str(description))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def VoltageRatioInput0onAttachCallback(self, HandlerSelf):

        VoltageRatioInputChannel = 0
        self.VoltageRatioInputGENERALonAttachCallback(VoltageRatioInputChannel)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def VoltageRatioInput0onDetachCallback(self, HandlerSelf):

        VoltageRatioInputChannel = 0
        self.VoltageRatioInputGENERALonDetachCallback(VoltageRatioInputChannel)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def VoltageRatioInput0onVoltageRatioChangeCallback(self, HandlerSelf, VoltageRatio):

        VoltageRatioInputChannel = 0
        self.VoltageRatioInputGENERALonVoltageRatioChangeCallback(VoltageRatioInputChannel, VoltageRatio)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def VoltageRatioInput0onErrorCallback(self, HandlerSelf, code, description):

        VoltageRatioInputChannel = 0
        self.VoltageRatioInputGENERALonErrorCallback(VoltageRatioInputChannel, code, description)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def VoltageRatioInput1onAttachCallback(self, HandlerSelf):

        VoltageRatioInputChannel = 1
        self.VoltageRatioInputGENERALonAttachCallback(VoltageRatioInputChannel)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def VoltageRatioInput1onDetachCallback(self, HandlerSelf):

        VoltageRatioInputChannel = 1
        self.VoltageRatioInputGENERALonDetachCallback(VoltageRatioInputChannel)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def VoltageRatioInput1onVoltageRatioChangeCallback(self, HandlerSelf, VoltageRatio):

        VoltageRatioInputChannel = 1
        self.VoltageRatioInputGENERALonVoltageRatioChangeCallback(VoltageRatioInputChannel, VoltageRatio)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def VoltageRatioInput1onErrorCallback(self, HandlerSelf, code, description):

        VoltageRatioInputChannel = 1
        self.VoltageRatioInputGENERALonErrorCallback(VoltageRatioInputChannel, code, description)

    ##########################################################################################################
    ##########################################################################################################
    
    ##########################################################################################################
    ##########################################################################################################
    def VoltageRatioInput2onAttachCallback(self, HandlerSelf):

        VoltageRatioInputChannel = 2
        self.VoltageRatioInputGENERALonAttachCallback(VoltageRatioInputChannel)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def VoltageRatioInput2onDetachCallback(self, HandlerSelf):

        VoltageRatioInputChannel = 2
        self.VoltageRatioInputGENERALonDetachCallback(VoltageRatioInputChannel)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def VoltageRatioInput2onVoltageRatioChangeCallback(self, HandlerSelf, VoltageRatio):

        VoltageRatioInputChannel = 2
        self.VoltageRatioInputGENERALonVoltageRatioChangeCallback(VoltageRatioInputChannel, VoltageRatio)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def VoltageRatioInput2onErrorCallback(self, HandlerSelf, code, description):

        VoltageRatioInputChannel = 2
        self.VoltageRatioInputGENERALonErrorCallback(VoltageRatioInputChannel, code, description)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def VoltageRatioInput3onAttachCallback(self, HandlerSelf):

        VoltageRatioInputChannel = 3
        self.VoltageRatioInputGENERALonAttachCallback(VoltageRatioInputChannel)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def VoltageRatioInput3onDetachCallback(self, HandlerSelf):

        VoltageRatioInputChannel = 3
        self.VoltageRatioInputGENERALonDetachCallback(VoltageRatioInputChannel)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def VoltageRatioInput3onVoltageRatioChangeCallback(self, HandlerSelf, VoltageRatio):

        VoltageRatioInputChannel = 3
        self.VoltageRatioInputGENERALonVoltageRatioChangeCallback(VoltageRatioInputChannel, VoltageRatio)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def VoltageRatioInput3onErrorCallback(self, HandlerSelf, code, description):

        VoltageRatioInputChannel = 3
        self.VoltageRatioInputGENERALonErrorCallback(VoltageRatioInputChannel, code, description)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def getPreciseSecondsTimeStampString(self):
        ts = time.time()

        return ts
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def StopCollectingDataForSnapshottingBridge(self, VoltageRatioInputChannel):

        self.VoltageRatioInputsList_DataForSnapshottingBridge_EnableCollectionFlag[VoltageRatioInputChannel] = 2
        self.MyPrint_WithoutLogFile("StopCollectingDataForSnapshottingBridge event fired for VoltageRatioInputChannel " + str(VoltageRatioInputChannel))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GetMostRecentDataDict(self):

        if self.EXIT_PROGRAM_FLAG == 0:

            return deepcopy(self.MostRecentDataDict) #deepcopy IS required as MostRecentDataDict contains lists.

        else:
            return dict() #So that we're not returning variables during the close-down process.
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ZeroWheatstoneBridges(self, VoltageRatioInputChannelsList):
        if self.IsInputList(VoltageRatioInputChannelsList) == 0:
            VoltageRatioInputChannelsList = list([VoltageRatioInputChannelsList])

        for VoltageRatioInputChannel in VoltageRatioInputChannelsList:
            if VoltageRatioInputChannel not in range(0, self.NumberOfWheatstoneBridges):
                print("ZeroWheatstoneBridges ERROR: Channel " + str(VoltageRatioInputChannel) + " not in the range " + str(list(range(0, self.NumberOfWheatstoneBridges))) + ".")
            else:
                self.VoltageRatioInputsList_NeedsToBeZeroedFlag[VoltageRatioInputChannel] = 1
                #self.MyPrint_WithoutLogFile("ZeroWheatstoneBridges: Issuing command to zero Channel " + str(VoltageRatioInputChannel))

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def SnapshotDataFromWheatstoneBridges(self, VoltageRatioInputChannelsList):

        if self.IsInputList(VoltageRatioInputChannelsList) == 0:
            VoltageRatioInputChannelsList = list([VoltageRatioInputChannelsList])

        for ForLoopIndex, VoltageRatioInputChannel in enumerate(VoltageRatioInputChannelsList):

            if VoltageRatioInputChannel not in range(0, self.NumberOfWheatstoneBridges):
                print("SnapshotDataFromWheatstoneBridges ERROR: Channel " + str(VoltageRatioInputChannel) + " not in the range " + str(list(range(0, self.NumberOfWheatstoneBridges))) + ".")
            else:
                self.VoltageRatioInputsList_NeedsToBeSnapshottedFlag[VoltageRatioInputChannel] = 1
                #self.MyPrint_WithoutLogFile("SnapshotDataFromWheatstoneBridges: Issuing command to snapshot Channel " + str(VoltageRatioInputChannel))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def UpdateFrequencyCalculation_MainThread(self):

        try:
            self.DataStreamingDeltaT_CalculatedFromMainThread = self.CurrentTime_CalculatedFromMainThread - self.LastTime_CalculatedFromMainThread

            if self.DataStreamingDeltaT_CalculatedFromMainThread != 0.0:
                self.DataStreamingFrequency_CalculatedFromMainThread = 1.0/self.DataStreamingDeltaT_CalculatedFromMainThread

            self.LastTime_CalculatedFromMainThread = self.CurrentTime_CalculatedFromMainThread
        except:
            exceptions = sys.exc_info()[0]
            print("UpdateFrequencyCalculation_MainThread ERROR with Exceptions: %s" % exceptions)
            #traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def UpdateFrequencyCalculation_OnVoltageRatioChangeCallback(self, VoltageRatioInputChannel):

        try:

            self.VoltageRatioInputsList_OnVoltageRatioChangeCallback_DataStreamingDeltaT[VoltageRatioInputChannel] = self.VoltageRatioInputsList_OnVoltageRatioChangeCallback_CurrentTime[VoltageRatioInputChannel] - self.VoltageRatioInputsList_OnVoltageRatioChangeCallback_LastTime[VoltageRatioInputChannel]

            if self.VoltageRatioInputsList_OnVoltageRatioChangeCallback_DataStreamingDeltaT[VoltageRatioInputChannel] != 0.0:
                self.VoltageRatioInputsList_OnVoltageRatioChangeCallback_DataStreamingFrequency[VoltageRatioInputChannel] = 1.0/self.VoltageRatioInputsList_OnVoltageRatioChangeCallback_DataStreamingDeltaT[VoltageRatioInputChannel]

            self.VoltageRatioInputsList_OnVoltageRatioChangeCallback_LastTime[VoltageRatioInputChannel] = self.VoltageRatioInputsList_OnVoltageRatioChangeCallback_CurrentTime[VoltageRatioInputChannel]
        except:
            exceptions = sys.exc_info()[0]
            print("UpdateFrequencyCalculation_OnVoltageRatioChangeCallback ERROR for VoltageRatioInputChannel " + str(VoltageRatioInputChannel) + " with Exceptions: %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ########################################################################################################## unicorn
    def MainThread(self):

        self.MyPrint_WithoutLogFile("Started MainThread for Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class object.")
        
        self.MainThread_still_running_flag = 1

        self.StartingTime_CalculatedFromMainThread = self.getPreciseSecondsTimeStampString()

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        while self.EXIT_PROGRAM_FLAG == 0:

            ##########################################################################################################
            ##########################################################################################################
            self.CurrentTime_CalculatedFromMainThread = self.getPreciseSecondsTimeStampString() - self.StartingTime_CalculatedFromMainThread
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            self.MostRecentDataDict = dict([("VoltageRatioInputsList_VoltageRatio_Raw", self.VoltageRatioInputsList_VoltageRatio_Raw),
                                            ("VoltageRatioInputsList_VoltageRatio_Filtered", self.VoltageRatioInputsList_VoltageRatio_Filtered),
                                            ("VoltageRatioInputsList_ErrorCallbackFiredFlag", self.VoltageRatioInputsList_ErrorCallbackFiredFlag),
                                            ("VoltageRatioInputsList_UpdateDeltaTseconds", self.VoltageRatioInputsList_UpdateDeltaTseconds),
                                            ("Time", self.CurrentTime_CalculatedFromMainThread)])
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            for VoltageRatioInputChannel, NeedsToBeZeroedFlag in enumerate(self.VoltageRatioInputsList_NeedsToBeZeroedFlag):

                if NeedsToBeZeroedFlag == 1:
                    if self.VoltageRatioInputsList_DataForSnapshottingBridge_EnableCollectionFlag[VoltageRatioInputChannel] == 0:
                        #print("Starting to collect data to Snapshot (FOR ZEROING) channel " + str(VoltageRatioInputChannel))
                        self.VoltageRatioInputsList_DataForSnapshottingBridge_EnableCollectionFlag[VoltageRatioInputChannel] = 1
                        self.TimerCallbackFunctionWithFunctionAsArgument_SingleShot_NoParenthesesAfterFunctionName(self.DataCollectionDurationInSecondsForSnapshottingBridge, self.StopCollectingDataForSnapshottingBridge, [VoltageRatioInputChannel])

                    elif self.VoltageRatioInputsList_DataForSnapshottingBridge_EnableCollectionFlag[VoltageRatioInputChannel] == 1:
                        pass

                    else: #Like 2
                        #print("Computing average for channel " + str(VoltageRatioInputChannel))
                        self.VoltageRatioInputsList_DataForSnapshottingBridge_EnableCollectionFlag[VoltageRatioInputChannel] = 0

                        Sum_Raw = 0.0
                        Sum_Filtered = 0.0
                        Counter = 0.0
                        while self.VoltageRatioInputsList_VoltageRatio_Raw_DataForSnapshottingBridgeQueue[VoltageRatioInputChannel].qsize() > 0:
                            Sum_Raw = Sum_Raw + self.VoltageRatioInputsList_VoltageRatio_Raw_DataForSnapshottingBridgeQueue[VoltageRatioInputChannel].get()
                            Sum_Filtered = Sum_Filtered + self.VoltageRatioInputsList_VoltageRatio_Filtered_DataForSnapshottingBridgeQueue[VoltageRatioInputChannel].get()
                            Counter = Counter + 1

                        if Counter > 0:
                            Average_Raw = Sum_Raw/Counter
                            Average_Filtered = Sum_Filtered/Counter
                            self.VoltageRatioInputsList_VoltageRatio_Raw_SnapshottedValue[VoltageRatioInputChannel] = Average_Raw
                            self.VoltageRatioInputsList_VoltageRatio_Filtered_SnapshottedValue[VoltageRatioInputChannel] = Average_Filtered
                        else:
                            self.VoltageRatioInputsList_VoltageRatio_Raw_SnapshottedValue[VoltageRatioInputChannel] = -11111.0
                            self.VoltageRatioInputsList_VoltageRatio_Filtered_SnapshottedValue[VoltageRatioInputChannel] = -11111.0

                        self.VoltageRatioInputsList_VoltageRatio_Raw_ZeroOffsetValue[VoltageRatioInputChannel]  = self.VoltageRatioInputsList_VoltageRatio_Raw_SnapshottedValue[VoltageRatioInputChannel]
                        self.VoltageRatioInputsList_VoltageRatio_Filtered_ZeroOffsetValue[VoltageRatioInputChannel]  = self.VoltageRatioInputsList_VoltageRatio_Filtered_SnapshottedValue[VoltageRatioInputChannel]

                        self.MyPrint_WithoutLogFile("self.VoltageRatioInputsList_VoltageRatio_Raw_ZeroOffsetValue for channel " + str(VoltageRatioInputChannel) +
                                                    ":" + str(self.VoltageRatioInputsList_VoltageRatio_Raw_ZeroOffsetValue[VoltageRatioInputChannel]) +
                                                    ", self.VoltageRatioInputsList_VoltageRatio_Filtered_ZeroOffsetValue for channel " + str(VoltageRatioInputChannel) +
                                                    ":" + str(self.VoltageRatioInputsList_VoltageRatio_Filtered_ZeroOffsetValue[VoltageRatioInputChannel]))

                        self.VoltageRatioInputsList_NeedsToBeZeroedFlag[VoltageRatioInputChannel] = 0

            ##########################################################################################################
            ##########################################################################################################
            
            ##########################################################################################################
            ##########################################################################################################
            for VoltageRatioInputChannel, NeedsToBeSnapshottedFlag in enumerate(self.VoltageRatioInputsList_NeedsToBeSnapshottedFlag):

                if NeedsToBeSnapshottedFlag == 1:
                    if self.VoltageRatioInputsList_DataForSnapshottingBridge_EnableCollectionFlag[VoltageRatioInputChannel] == 0:
                        #print("Starting to collect data to Snapshot channel " + str(VoltageRatioInputChannel))
                        self.VoltageRatioInputsList_DataForSnapshottingBridge_EnableCollectionFlag[VoltageRatioInputChannel] = 1
                        self.TimerCallbackFunctionWithFunctionAsArgument_SingleShot_NoParenthesesAfterFunctionName(self.DataCollectionDurationInSecondsForSnapshottingBridge, self.StopCollectingDataForSnapshottingBridge, [VoltageRatioInputChannel])

                    elif self.VoltageRatioInputsList_DataForSnapshottingBridge_EnableCollectionFlag[VoltageRatioInputChannel] == 1:
                        pass

                    else: #Like 2
                        #print("Computing average for channel " + str(VoltageRatioInputChannel))
                        self.VoltageRatioInputsList_DataForSnapshottingBridge_EnableCollectionFlag[VoltageRatioInputChannel] = 0

                        Sum_Raw = 0.0
                        Sum_Filtered = 0.0
                        Counter = 0.0
                        while self.VoltageRatioInputsList_VoltageRatio_Raw_DataForSnapshottingBridgeQueue[VoltageRatioInputChannel].qsize() > 0:
                            Sum_Raw = Sum_Raw + self.VoltageRatioInputsList_VoltageRatio_Raw_DataForSnapshottingBridgeQueue[VoltageRatioInputChannel].get()
                            Sum_Filtered = Sum_Filtered + self.VoltageRatioInputsList_VoltageRatio_Filtered_DataForSnapshottingBridgeQueue[VoltageRatioInputChannel].get()
                            Counter = Counter + 1

                        if Counter > 0:
                            Average_Raw = Sum_Raw/Counter
                            Average_Filtered = Sum_Filtered/Counter
                            self.VoltageRatioInputsList_VoltageRatio_Raw_SnapshottedValue[VoltageRatioInputChannel] = Average_Raw
                            self.VoltageRatioInputsList_VoltageRatio_Filtered_SnapshottedValue[VoltageRatioInputChannel] = Average_Filtered
                        else:
                            self.VoltageRatioInputsList_VoltageRatio_Raw_SnapshottedValue[VoltageRatioInputChannel] = -11111.0
                            self.VoltageRatioInputsList_VoltageRatio_Filtered_SnapshottedValue[VoltageRatioInputChannel] = -11111.0

                        self.MyPrint_WithoutLogFile("self.VoltageRatioInputsList_VoltageRatio_Raw_SnapshottedValue for channel " + str(VoltageRatioInputChannel) +
                                                    ":" + str(self.VoltageRatioInputsList_VoltageRatio_Raw_SnapshottedValue[VoltageRatioInputChannel]) +
                                                    ", self.VoltageRatioInputsList_VoltageRatio_Filtered_SnapshottedValue for channel " + str(VoltageRatioInputChannel) +
                                                    ":" + str(self.VoltageRatioInputsList_VoltageRatio_Filtered_SnapshottedValue[VoltageRatioInputChannel]))
                        
                        self.VoltageRatioInputsList_NeedsToBeSnapshottedFlag[VoltageRatioInputChannel] = 0
            ##########################################################################################################
            ##########################################################################################################
            
            ########################################################################################################## USE THE TIME.SLEEP() TO SET THE LOOP FREQUENCY
            ##########################################################################################################
            self.UpdateFrequencyCalculation_MainThread()

            if self.MainThread_TimeToSleepEachLoop > 0.0:
                time.sleep(self.MainThread_TimeToSleepEachLoop)
            ##########################################################################################################
            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        for VoltageRatioInput_Object in self.VoltageRatioInputsList_PhidgetsVoltageRatioInputObjects:
            VoltageRatioInput_Object.close()
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        self.MyPrint_WithoutLogFile("Finished MainThread for Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class object.")
        self.MainThread_still_running_flag = 0
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ExitProgram_Callback(self):

        print("Exiting all threads for Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class object")

        self.EXIT_PROGRAM_FLAG = 1

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def StartGUI(self, GuiParent):

        self.GUI_Thread_ThreadingObject = threading.Thread(target=self.GUI_Thread, args=(GuiParent,))
        self.GUI_Thread_ThreadingObject.setDaemon(True) #Should mean that the GUI thread is destroyed automatically when the main thread is destroyed.
        self.GUI_Thread_ThreadingObject.start()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GUI_Thread(self, parent):

        print("Starting the GUI_Thread for Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class object.")

        ###################################################
        ###################################################
        self.root = parent
        self.parent = parent
        ###################################################
        ###################################################

        ###################################################
        ###################################################
        self.myFrame = Frame(self.root)

        if self.UseBorderAroundThisGuiObjectFlag == 1:
            self.myFrame["borderwidth"] = 2
            self.myFrame["relief"] = "ridge"

        self.myFrame.grid(row = self.GUI_ROW,
                          column = self.GUI_COLUMN,
                          padx = self.GUI_PADX,
                          pady = self.GUI_PADY,
                          rowspan = self.GUI_ROWSPAN,
                          columnspan= self.GUI_COLUMNSPAN,
                          sticky = self.GUI_STICKY)
        ###################################################
        ###################################################

        ###################################################
        ###################################################
        self.TKinter_LightGreenColor = '#%02x%02x%02x' % (150, 255, 150) #RGB
        self.TKinter_LightRedColor = '#%02x%02x%02x' % (255, 150, 150) #RGB
        self.TKinter_LightYellowColor = '#%02x%02x%02x' % (255, 255, 150)  # RGB
        self.TKinter_DefaultGrayColor = '#%02x%02x%02x' % (240, 240, 240)  # RGB
        self.TkinterScaleWidth = 10
        self.TkinterScaleLength = 250
        ###################################################
        ###################################################

        ###################################################
        ###################################################
        self.DeviceInfoLabel = Label(self.myFrame, text="Device Info", width=50)
        self.DeviceInfoLabel.grid(row=0, column=0, padx=5, pady=1, columnspan=1, rowspan=1)
        ###################################################
        ###################################################

        ###################################################
        ###################################################
        self.VoltageRatioInputs_Label = Label(self.myFrame, text="VoltageRatioInputs_Label", width=80)
        self.VoltageRatioInputs_Label.grid(row=0, column=1, padx=5, pady=1, columnspan=1, rowspan=10)
        ###################################################
        ###################################################
        
        ###################################################
        ###################################################
        self.ZeroingButtonsFrame = Frame(self.myFrame)
        self.ZeroingButtonsFrame.grid(row = 1, column = 0, padx = 1, pady = 1, rowspan = 1, columnspan = 1)

        ###################################################
        self.VoltageRatioInputsList_ZeroingButtonObjects = []
        for VoltageRatioInputChannel in range(0, self.NumberOfWheatstoneBridges):
            self.VoltageRatioInputsList_ZeroingButtonObjects.append(Button(self.ZeroingButtonsFrame, text="Zero Bridge " + str(VoltageRatioInputChannel), state="normal", width=15, command=lambda i=VoltageRatioInputChannel: self.VoltageRatioInputsList_ZeroingButtonObjectsResponse(i)))
            self.VoltageRatioInputsList_ZeroingButtonObjects[VoltageRatioInputChannel].grid(row=1, column=VoltageRatioInputChannel, padx=1, pady=1)
        ###################################################

        ###################################################
        self.ZeroAllWheatstoneBridges_Button = Button(self.ZeroingButtonsFrame, text="Zero All Data", state="normal", width=15, command=lambda i=1: self.ZeroAllWheatstoneBridges_ButtonResponse())
        self.ZeroAllWheatstoneBridges_Button.grid(row=2, column=0, padx=1, pady=1, rowspan=1, columnspan=1)
        ###################################################

        ###################################################
        self.SnapshotDataFromWheatstoneBridges_Button = Button(self.ZeroingButtonsFrame, text="Snapshot All Data", state="normal", width=15, command=lambda i=1: self.SnapshotDataFromWheatstoneBridges_ButtonResponse())
        self.SnapshotDataFromWheatstoneBridges_Button.grid(row=2, column=1, padx=1, pady=1, rowspan=1, columnspan=1)
        ###################################################

        ###################################################
        ###################################################

        ###################################################
        ###################################################
        self.PrintToGui_Label = Label(self.myFrame, text="PrintToGui_Label", width=100)
        if self.EnableInternal_MyPrint_Flag == 1:
            self.PrintToGui_Label.grid(row=0, column=2, padx=1, pady=1, columnspan=1, rowspan=10)
        ###################################################
        ###################################################

        ###################################################
        ###################################################
        self.GUI_ready_to_be_updated_flag = 1
        ###################################################
        ###################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GUI_update_clock(self):

        #######################################################
        #######################################################
        #######################################################
        #######################################################
        if self.USE_GUI_FLAG == 1 and self.EXIT_PROGRAM_FLAG == 0:

            #######################################################
            #######################################################
            #######################################################
            if self.GUI_ready_to_be_updated_flag == 1:

                #######################################################
                #######################################################
                try:
                    #######################################################

                    ##################
                    ZeroValsTextToDisplay_Raw = "["
                    ZeroValsTextToDisplay_Filtered = "["
                    for VoltageRatioInputChannel in range(0, self.NumberOfWheatstoneBridges):
                        ZeroValsTextToDisplay_Raw = ZeroValsTextToDisplay_Raw + str(self.VoltageRatioInputsList_VoltageRatio_Raw_ZeroOffsetValue[VoltageRatioInputChannel]) + ",\n"
                        ZeroValsTextToDisplay_Filtered = ZeroValsTextToDisplay_Filtered + str(self.VoltageRatioInputsList_VoltageRatio_Filtered_ZeroOffsetValue[VoltageRatioInputChannel]) + ",\n"

                    ZeroValsTextToDisplay_Raw = ZeroValsTextToDisplay_Raw[:-2] + "]"
                    ZeroValsTextToDisplay_Filtered = ZeroValsTextToDisplay_Filtered[:-2] + "]"
                    ##################

                    ##################
                    SnapshottedValsTextToDisplay_Raw = "["
                    SnapshottedValsTextToDisplay_Filtered = "["
                    for VoltageRatioInputChannel in range(0, self.NumberOfWheatstoneBridges):
                        SnapshottedValsTextToDisplay_Raw = SnapshottedValsTextToDisplay_Raw + str(self.VoltageRatioInputsList_VoltageRatio_Raw_SnapshottedValue[VoltageRatioInputChannel]) + ",\n"
                        SnapshottedValsTextToDisplay_Filtered = SnapshottedValsTextToDisplay_Filtered + str(self.VoltageRatioInputsList_VoltageRatio_Filtered_SnapshottedValue[VoltageRatioInputChannel]) + ",\n"

                    SnapshottedValsTextToDisplay_Raw = SnapshottedValsTextToDisplay_Raw[:-2] + "]"
                    SnapshottedValsTextToDisplay_Filtered = SnapshottedValsTextToDisplay_Filtered[:-2] + "]"
                    ##################

                    self.DeviceInfoLabel["text"] = self.NameToDisplay_UserSet + \
                                                    "\nDevice Name: " + self.DetectedDeviceName + \
                                                    "\nDevice Serial Number: " + str(self.DetectedDeviceSerialNumber) + \
                                                    "\nDevice Version: " + str(self.DetectedDeviceVersion) + \
                                                    "\nDevice ID: " + str(self.DetectedDeviceID) + \
                                                    "\nBridgeGain (Actual Integer Value): " + str(self.VoltageRatioInputsList_BridgeGain_ActualIntegerValue_ReceivedFromBoard) + \
                                                    "\nBridgeGain (Phidgets Contant): " + str(self.VoltageRatioInputsList_BridgeGain_PhidgetsConstant_ReceivedFromBoard) + \
                                                    "\nBoard's Min Callback DeltaT (ms): " + str(self.CallbackUpdateDeltaTmilliseconds_MinimumValue) + \
                                                    "\nCallback DeltaT ms: " + str(self.VoltageRatioInputsList_CallbackUpdateDeltaTmilliseconds_ReceivedFromBoard) + \
                                                    "\nChangeTrigger: " + str(self.VoltageRatioInputsList_VoltageRatioChangeTrigger_ReceivedFromBoard) + \
                                                    "\nEnabledState: " + str(self.VoltageRatioInputsList_EnabledStateBoolean_ReceivedFromBoard) + \
                                                    "\nZeroVals, Raw: " + ZeroValsTextToDisplay_Raw + \
                                                    "\nSnapshottedVals, Raw: " + SnapshottedValsTextToDisplay_Raw + \
                                                    "\nZeroVals, Filtered: " + ZeroValsTextToDisplay_Filtered + \
                                                    "\nSnapshottedVals, Filtered:: " + SnapshottedValsTextToDisplay_Filtered

                    #######################################################

                    #######################################################
                    DataForSnapshottingBridgeQueue_QsizeTextToDisplay = "["
                    for VoltageRatioInputChannel in range(0, self.NumberOfWheatstoneBridges):
                        DataForSnapshottingBridgeQueue_QsizeTextToDisplay = DataForSnapshottingBridgeQueue_QsizeTextToDisplay + str(self.VoltageRatioInputsList_VoltageRatio_Raw_DataForSnapshottingBridgeQueue[VoltageRatioInputChannel].qsize()) + ", "
                    DataForSnapshottingBridgeQueue_QsizeTextToDisplay = DataForSnapshottingBridgeQueue_QsizeTextToDisplay[:-2] + "]"

                    self.VoltageRatioInputs_Label["text"] = "VoltageRati, Raw: " + str(self.VoltageRatioInputsList_VoltageRatio_Raw) + \
                                                "\nVoltageRatio, Filtered: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.VoltageRatioInputsList_VoltageRatio_Filtered, 0, 5) + \
                                                "\nUpdateDeltaTseconds: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.VoltageRatioInputsList_OnVoltageRatioChangeCallback_DataStreamingDeltaT, 0, 5) + \
                                                "\nTime: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.CurrentTime_CalculatedFromMainThread, 0, 3) + \
                                                "\nMain Thread Frequency: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.DataStreamingFrequency_CalculatedFromMainThread, 0, 3) + \
                                                "\nDataForSnapshottingBridgeQueue.qsize(): " + DataForSnapshottingBridgeQueue_QsizeTextToDisplay

                    #######################################################

                    #######################################################
                    self.PrintToGui_Label.config(text=self.PrintToGui_Label_TextInput_Str)
                    #######################################################

                except:
                    exceptions = sys.exc_info()[0]
                    print("Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class GUI_update_clock ERROR: Exceptions: %s" % exceptions)
                    traceback.print_exc()
                #######################################################
                #######################################################

            #######################################################
            #######################################################
            #######################################################

        #######################################################
        #######################################################
        #######################################################
        #######################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def VoltageRatioInputsList_ZeroingButtonObjectsResponse(self, VoltageRatioInputChannelNumber):

        self.ZeroWheatstoneBridges([VoltageRatioInputChannelNumber])
        #self.MyPrint_WithoutLogFile("VoltageRatioInputsList_ZeroingButtonObjectsResponse: Event fired for VoltageRatioInputChannelNumber " + str(VoltageRatioInputChannelNumber))

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ZeroAllWheatstoneBridges_ButtonResponse(self):

        self.VoltageRatioInputsList_NeedsToBeZeroedFlag = [1]*self.NumberOfWheatstoneBridges

        #self.MyPrint_WithoutLogFile("ZeroAllWheatstoneBridges_ButtonResponse: Event fired for VoltageRatioInputChannelNumber " + str(VoltageRatioInputChannelNumber))

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def SnapshotDataFromWheatstoneBridges_ButtonResponse(self):

        self.VoltageRatioInputsList_NeedsToBeSnapshottedFlag = [1]*self.NumberOfWheatstoneBridges

        #self.MyPrint_WithoutLogFile("SnapshotDataFromWheatstoneBridges_ButtonResponse: Event fired for VoltageRatioInputChannelNumber " + str(VoltageRatioInputChannelNumber))

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def TimerCallbackFunctionWithFunctionAsArgument_SingleShot_NoParenthesesAfterFunctionName(self, CallbackAfterDeltaTseconds, FunctionToCall_NoParenthesesAfterFunctionName, ArgumentListToFunction):

        self.TimerObject = threading.Timer(CallbackAfterDeltaTseconds, FunctionToCall_NoParenthesesAfterFunctionName, ArgumentListToFunction) #Must pass arguments to callback-function via list as the third argument to Timer call
        self.TimerObject.daemon = True #Without the daemon=True, this recursive function won't terminate when the main program does.
        self.TimerObject.start()

        print("TimerCallbackFunctionWithFunctionAsArgument_SingleShot_NoParenthesesAfterFunctionName event fired to call function: '" + str(FunctionToCall_NoParenthesesAfterFunctionName.__name__) + "' at time " + str(self.getPreciseSecondsTimeStampString()))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def MyPrint_WithoutLogFile(self, input_string):

        input_string = str(input_string)

        if input_string != "":

            #input_string = input_string.replace("\n", "").replace("\r", "")

            ################################ Write to console
            # Some people said that print crashed for pyinstaller-built-applications and that sys.stdout.write fixed this.
            # http://stackoverflow.com/questions/13429924/pyinstaller-packaged-application-works-fine-in-console-mode-crashes-in-window-m
            if self.PrintToConsoleFlag == 1:
                sys.stdout.write(input_string + "\n")
            ################################

            ################################ Write to GUI
            self.PrintToGui_Label_TextInputHistory_List.append(self.PrintToGui_Label_TextInputHistory_List.pop(0)) #Shift the list
            self.PrintToGui_Label_TextInputHistory_List[-1] = str(input_string) #Add the latest value

            self.PrintToGui_Label_TextInput_Str = ""
            for Counter, Line in enumerate(self.PrintToGui_Label_TextInputHistory_List):
                self.PrintToGui_Label_TextInput_Str = self.PrintToGui_Label_TextInput_Str + Line

                if Counter < len(self.PrintToGui_Label_TextInputHistory_List) - 1:
                    self.PrintToGui_Label_TextInput_Str = self.PrintToGui_Label_TextInput_Str + "\n"
            ################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def IsInputList(self, InputToCheck):

        result = isinstance(InputToCheck, list)
        return result
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self, input, number_of_leading_numbers = 4, number_of_decimal_places = 3):

        number_of_decimal_places = max(1, number_of_decimal_places) #Make sure we're above 1

        ListOfStringsToJoin = []

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        if isinstance(input, str) == 1:
            ListOfStringsToJoin.append(input)
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        elif isinstance(input, int) == 1 or isinstance(input, float) == 1:
            element = float(input)
            prefix_string = "{:." + str(number_of_decimal_places) + "f}"
            element_as_string = prefix_string.format(element)

            ##########################################################################################################
            ##########################################################################################################
            if element >= 0:
                element_as_string = element_as_string.zfill(number_of_leading_numbers + number_of_decimal_places + 1 + 1)  # +1 for sign, +1 for decimal place
                element_as_string = "+" + element_as_string  # So that our strings always have either + or - signs to maintain the same string length
            else:
                element_as_string = element_as_string.zfill(number_of_leading_numbers + number_of_decimal_places + 1 + 1 + 1)  # +1 for sign, +1 for decimal place
            ##########################################################################################################
            ##########################################################################################################

            ListOfStringsToJoin.append(element_as_string)
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        elif isinstance(input, list) == 1:

            if len(input) > 0:
                for element in input: #RECURSION
                    ListOfStringsToJoin.append(self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, number_of_leading_numbers, number_of_decimal_places))

            else: #Situation when we get a list() or []
                ListOfStringsToJoin.append(str(input))

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        elif isinstance(input, tuple) == 1:

            if len(input) > 0:
                for element in input: #RECURSION
                    ListOfStringsToJoin.append("TUPLE" + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, number_of_leading_numbers, number_of_decimal_places))

            else: #Situation when we get a list() or []
                ListOfStringsToJoin.append(str(input))

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        elif isinstance(input, dict) == 1:

            if len(input) > 0:
                for Key in input: #RECURSION
                    ListOfStringsToJoin.append(str(Key) + ": " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(input[Key], number_of_leading_numbers, number_of_decimal_places))

            else: #Situation when we get a dict()
                ListOfStringsToJoin.append(str(input))

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        else:
            ListOfStringsToJoin.append(str(input))
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        if len(ListOfStringsToJoin) > 1:

            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            StringToReturn = ""
            for Index, StringToProcess in enumerate(ListOfStringsToJoin):

                ################################################
                if Index == 0: #The first element
                    if StringToProcess.find(":") != -1 and StringToProcess[0] != "{": #meaning that we're processing a dict()
                        StringToReturn = "{"
                    elif StringToProcess.find("TUPLE") != -1 and StringToProcess[0] != "(":  # meaning that we're processing a tuple
                        StringToReturn = "("
                    else:
                        StringToReturn = "["

                    StringToReturn = StringToReturn + StringToProcess.replace("TUPLE","") + ", "
                ################################################

                ################################################
                elif Index < len(ListOfStringsToJoin) - 1: #The middle elements
                    StringToReturn = StringToReturn + StringToProcess + ", "
                ################################################

                ################################################
                else: #The last element
                    StringToReturn = StringToReturn + StringToProcess

                    if StringToProcess.find(":") != -1 and StringToProcess[-1] != "}":  # meaning that we're processing a dict()
                        StringToReturn = StringToReturn + "}"
                    elif StringToProcess.find("TUPLE") != -1 and StringToProcess[-1] != ")":  # meaning that we're processing a tuple
                        StringToReturn = StringToReturn + ")"
                    else:
                        StringToReturn = StringToReturn + "]"

                ################################################

            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################

        elif len(ListOfStringsToJoin) == 1:
            StringToReturn = ListOfStringsToJoin[0]

        else:
            StringToReturn = ListOfStringsToJoin

        return StringToReturn
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################


