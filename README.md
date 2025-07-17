###########################

Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class

Wrapper (including ability to hook to Tkinter GUI) to read load-cell/wheatstone-bridge data from PhidgetBridge 4-Input (4 Wheatstone bridges) 1046_0B (non VINT).

From Phidgets' website:

"The PhidgetBridge lets you connect up to 4 un-amplified Wheatstone bridges, such as:
Strain gauges,
Compression load cells,
Pressure sensors/Barometers,
Piezoresistive accelerometers, and
Magnetoresistive sensors (Compasses)."

PhidgetBridge 4-Input

ID: 1046_0B

https://www.phidgets.com/?tier=3&catid=98&pcid=78&prodid=1027

Reuben Brewer, Ph.D.

reuben.brewer@gmail.com

www.reubotics.com

Apache 2 License

Software Revision E, 07/17/2025

Verified working on:

Python 3.11/12

Windows 10/11 64-bit

Raspberry Pi Bookworm

*NOTE THAT YOU MUST INSTALL BOTH THE Phidget22 LIBRARY AS WELL AS THE PYTHON MODULE.*

###########################

########################### Python module installation instructions, all OS's

Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class, ListOfModuleDependencies: ['future.builtins', 'LowPassFilter_ReubenPython2and3Class', 'Phidget22']

Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class, ListOfModuleDependencies_TestProgram: ['keyboard', 'MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class', 'MyPrint_ReubenPython2and3Class']

Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class, ListOfModuleDependencies_NestedLayers: ['future.builtins', 'GetCPUandMemoryUsageOfProcessByPID_ReubenPython3Class', 'numpy', 'pexpect', 'psutil', 'pyautogui']

Phidgets4xWheatstoneBridge1046_ReubenPython2and3Class, ListOfModuleDependencies_All:['future.builtins', 'GetCPUandMemoryUsageOfProcessByPID_ReubenPython3Class', 'keyboard', 'LowPassFilter_ReubenPython2and3Class', 'MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class', 'MyPrint_ReubenPython2and3Class', 'numpy', 'pexpect', 'Phidget22', 'psutil', 'pyautogui']

https://pypi.org/project/Phidget22/#files

To install the Python module using pip:

pip install Phidget22       (with "sudo" if on Linux/Raspberry Pi)

To install the Python module from the downloaded .tar.gz file, enter downloaded folder and type "python setup.py install"

###########################

########################### Library/driver installation instructions, Windows

https://www.phidgets.com/docs/OS_-_Windows

###########################

########################### Library/driver installation instructions, Linux (other than Raspberry Pi)

https://www.phidgets.com/docs/OS_-_Linux#Quick_Downloads

###########################

########################### Library/driver installation instructions, Raspberry Pi (models 2 and above)

https://www.phidgets.com/education/learn/getting-started-kit-tutorial/install-libraries/

curl -fsSL https://www.phidgets.com/downloads/setup_linux | sudo -E bash -

sudo apt-get install -y libphidget22
 
###########################
