=====================================
NPP_Extension Developer Documentation
=====================================

This document is meant to show how a developer would proceed in:

#. Installing necessary extensions, libraries, and compilation tools
#. Setting up the development environment for a thrift server
#. Developing a Thrift server
#. Rendering a source file into html to be displayed to a browser window

Installing the Necessary Extensions, Libraries, and Compilation tools
=====================================================================
These Tools are what are needed to build the thrift includes and libraries to be used in the server setup:

#. `Visual Studio 2019 Community <https://visualstudio.microsoft.com/vs>`_ (We are using VS 2019 community version to work with our plugins. Ideally at some time in the future this will be changed to the most recent version. Also, Visual Studio will ONLY install to your storage device your Operating System is located on, so be wary if you have limited space on this drive. )
#. `Developer Command Prompt for VS 2019` This should have downloaded with the main Visual Studio 2019, search for it in the windows search bar
#. `thrift-0.15.0.exe <http://archive.apache.org/dist/thrift/0.15.0>`__ 

Side Note on Installation:  During our development, we noticed the `thrift compiler` was not in the master folder from github. As a result the thrift compiler was found and downloaded from 
https://www.apache.org/dyn/closer.cgi?path=/thrift/0.16.0/thrift-0.16.0.exe 

Working with your plugins
--------------------------
https://npp-user-manual.org/docs/plugins/ 
- Open CodeChat.vcproj in your Visual Studio.
- Define your plugin commands number in PluginDefinition.h
- Customize plugin commands names and associated function name (and the other stuff, optional) in PluginDefinition.cpp.
- Define the associated functions.
- Build the files in visual studio. (If you press the "run" button it builds the file, but gives an error, however this is ok because you cant run the .dll outside of Notepad++)

Open NotePad++
    - Copy the pl.x86.json file from NPP_Extension/basic_plugin into Notepad++/plugins/Config/
    - Select plugins from the top menu and open the plugin folder
    - Create a folder called CodeChat
    - Add your Codechat.dll to the CodeChat folder

CodeChat should appear in the plugins list with the option for a hello world
Currently the plugin creates a new file that says Hello, Notepad++

Building vcpkg
----------------------------------
In order to use the thrift library, 'vcpkg <https://vcpkg.info/port/thrift>`_ was used to install the thrift library.
To build the vcpkg follow this `tutorial <https://thrift.apache.org/lib/cpp.html#thrift-and-the-vcpkg-package-manager>`_ 

Creating Thrift Client in Visual Studio
----------------------------------------
When downloading Visual Studio 2019 the following packages need to be installed to properly install vcpkg.
    - Windows Universal C Runtime: Microsoft.VisualStudio.Component.Windows10SDK
    - C++ core desktop features: Microsoft.VisualStudio.ComponentGroup.NativeDesktop.Core
    - Microsoft.VisualStudio.Component.VC.140 (for Visual Studio 2015)
    - Microsoft.VisualStudio.Component.VC.Tools.x86.x64 (for Visual Studio 2017 or later)
    - MSBuild: Microsoft.Component.MSBuild
    - Windows SDK (one of them):
        - 8.1: Microsoft.VisualStudio.Component.Windows81SDK
        - 10.0.18362: Microsoft.VisualStudio.Component.Windows10SDK.18362
        - 10.0.19041: Microsoft.VisualStudio.Component.Windows10SDK.19041
        - 10.0.20348: Microsoft.VisualStudio.Component.Windows10SDK.20348
        - 11.0.22000: Microsoft.VisualStudio.Component.Windows11SDK.22000
    - ARM/ARM64:
        - Visual Studio Build tools for ARM: Microsoft.VisualStudio.Component.VC.Tools.arm
        - Visual Studio Build tools for ARM: Microsoft.VisualStudio.Component.VC.Tools.arm64
    - Visual Studio Build tools for UWP: Microsoft.VisualStudio.ComponentGroup.UWP.VC
    - C++ Desktop Developer Suite

Once the following packages are installed in visual studio, the thrift repository should be accessed.

The compiler should be placed in the tutorial folder of the thrift directory

The thrift client was made using the official client example from apache found `here <https://thrift.apache.org/tutorial/cpp.html>`_

The main library used to create the client is the "Calculator.h" header file. This file relies on the tutorial and shared code examples provided by apache. 
In order to retrieve these files, the user must run these two commands in the tutorial folder with the newly downloaded 
thrift compiler. 

thrift-0.16.0.exe -r --gen cpp shared.thrift
thrift-0.16.0.exe -r --gen cpp tutorial.thrift

The two commands above will produce all the necessary cpp and .h files needed to run the example thrift client.

Currently the solution file "NPP_Extension.sln" and the project file "NPP_Extension.vcxproj" contain all of the files 
necessary to correctly compile the example thrift client. However, one can modify the project for further functionality
by adding in more of the produced files from the shared.thrift and tutorial.thrift commands above. The files will be
located in the "gen-cpp" folder.

The current status of the thrift client is that it will ping the server when executed.
Testing was not able to be fully completed with the setup of the developers for this project, however, to test full functionality of the 
code chat server and the thrift client connection, the following needs to occur.

In one terminal, call the code chat server by first creating a virtual environment in python. Then the user should activate the code chat environment.
Lastly the user will call "CodeChat_Server serve" to instantiate the server. 

In another window, click on the "NPP_Extension.exe" file in the Debug folder of the NPP_Extension folder in code chat. A terminal should pop-up showing
the client pinging the server on port 27376.