
# Windows PowerShell Installation Script
# **************************************
# 
# PowerShell.exe -ExecutionPolicy Bypass -File .\win.ps1
# 
# Pre-Script Definitions
# ----------------------
# Automatically moves Powershell to the user directory; when using powershell as an admin as the default admin location is in "Windows/System32"
cd $env:USERPROFILE
# 
# Version of python required, put into both string and array form to be easier to parse and output
$pythonVersionReq = '3.7.0'
$pythonVersionReqArray = '3','7','0'
 
# 
# Checking if Python is Installed
# ===============================

$pythonVersion = python --version 2>&1 | %{ "$_" }


# Case 1: No Python
# -----------------

## sometimes variable is empty other times contains "Python was not found..." 
if(([string]::IsNullOrEmpty($pythonVersion)) -or (($pythonVersion[0] -ceq "P") -and ($pythonVersion[7] -eq "w"))) {
    
    cls    # clear screen to hide confusing or conflicting powershell error message(s)
    
    echo "Python $pythonVersionReq or later required. Type 'python' and press Enter to install from Microsoft Store, then rerun script."
    
    echo "`n"     # blank line
    
    Exit   # abort script
    
    }

## split pythonVersion variable into an array 
$pythonVersion = $pythonVersion.Split()[1]  # 3.10.6
$pythonVersionMaj = $pythonVersion.Split('.')[0] # 3
$pythonVersionMin = $pythonVersion.Split('.')[1] # 10

# Case 2: Python 2
# -----------------
# "Python 2.7.14"

if($pythonVersionMaj -lt $pythonVersionReqArray[0]) {

    cls   
    
    echo "Python $pythonVersionReq or later required. Install Python 3 from Microsoft Store (https://apps.microsoft.com/store/detail/python-310/9PJPW5LDXLZ5?hl=en-us&gl=US), then rerun script."
    
    echo "`n"     
    
    Exit   
    
    }

# Case 3: Outdated Python 3
# -------------------------
# "Python 3.6.7"

if($pythonVersionMin -lt $pythonVersionReqArray[1]) {
    
    cls    
    
    echo "Python $pythonVersionReq or later required. Update Python or install latest version from Microsoft Store (https://apps.microsoft.com/store/detail/python-310/9PJPW5LDXLZ5?hl=en-us&gl=US), then rerun script."
    
    echo "`n"     # blank line
    
    Exit   # abort script
    
    }

# Case 4: Python 3
# -----------------
# "Python 3.10.6"

 if(($pythonVersion[0] -ceq "P") -and ($pythonVersion[7] -eq "3")) {
    
    echo "Python 3"
    
    }

# $pythonVersionReqArray = '3','7','0'
# echo $pythonVersion

<#
   

# Returning to User Dir
cd $env:USERPROFILE
# |
# 
# Grabbing the version of python and splitting it up so as to make parsing easier
$pythonVersion = python --version
$pythonVersion = $pythonVersion.Split()[1]
$pythonVersionMaj = $pythonVersion.Split('.')[0]
$pythonVersionMin = $pythonVersion.Split('.')[1]

# Version Checking
# if the version we have is not greater than or equal to the required version, an updated version must be installed
# checking negative case so that if it evaluates as true (version is less than required) then throw warning
$InstallBool = False;
if ($pythonVersionMaj -lt $pythonVersionReqArray[0]){
    $InstallBool = True
}
elseif($pythonVersionMaj -eq $pythonVersionReqArray[0]){
    if($pythonVersionMaj -lt $pythonVersionReqArray[1]){
        $InstallBool = True
    }
}

if($InstallBool){
    $response = Read-Host -Prompt "You do not have the correct version of Python installed, would you like the script to install the required version ($pythonVersionReq) (y/n)?"
    if($response -eq "y"){
        echo "Downloading Python Version $PyTarget"
        # Downloading Python Unsure if ``-UseDefaulCredential`` in necessary
        Invoke-WebRequest -Uri $PythonURL -OutFile $PythonDest -UseDefaultCredential
        echo "Python Version$PyTarget Downloaded
        
        Installing Python"
        Read-Host "Press any button to continue, then click 'Install Now' in popup"
        cd $env:USERPROFILE\Downloads

        # Installs Python ``Out-Null`` option makes sure the program doesn't continue before the installation completes Using Start-Process over just using the cmd because it allows me to input a string, so we can easily change the target python version. 
        Start-Process ".\python-$PyTarget-amd64.exe" -ArgumentList /quietly,PrependPath=1 -Wait

        echo "Python Version $PyTarget Installed Successfully
        "
    }
    else{
        echo "Please install the required version of python: $pythonVersionReq or later
        "
        exit
    }
}
else{
    echo "Acceptable version of Python found"
}

#>


# Going to the user dir
cd $env:USERPROFILE

<#
# Creating codechat venv
# ----------------------
# We do this so that our installation does not mess with any other installations of python
echo "Creating codechat venv..."
$codechat = Get-Item codechat
if([string]::IsNullOrEmpty($codechat)){
    # Create a virtual enviroment named codechat
    python -m venv codechat
    echo "virtual environment successfully created
    "
}
else{
    echo "'codechat' virtual environment already found, skipping this step
    "
}

# find CodeChat_Server.exe and tell user if just updating or installing
# This could probably be changed, so that it doesn't differentiate seeing as both paths do that same thing.
$CodeChat_Server = Get-Command $env:USERPROFILE\codechat\Scripts\CodeChat_Server
if([string]::IsNullOrEmpty($CodeChat_Server)){
    # Install the CodeChat Server
    echo "installing CodeChat_Server"
    # python -m pip install --upgrade CodeChat_Server
    codechat\Scripts\python -m pip install --upgrade CodeChat_Server
    echo "CodeChat_Server successfully installed
    "
}
else{
    # Update the CodeChat Server
    echo "CodeChat_Server found, running update"
    # python -m pip install --upgrade CodeChat_Server
    codechat\Scripts\python -m pip install --upgrade CodeChat_Server
    echo "CodeChat_Server successfully updated"
}


# `Set-Clipboard <https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.management/set-clipboard?view=powershell-7.2>`_: Copies path of CodeChat_Server to the clipboard for easy pasting and displays path in terminal
$pathToCodeChat = Get-Command $env:USERPROFILE\codechat\Scripts\CodeChat_Server | Select-Object -ExpandProperty Definition
Set-Clipboard $pathToCodeChat
echo "Here is your path to CodeChat (Also copied to your clipboard): $pathToCodeChat"
echo "Now add this path to your plugin's setup - see https://codechat-system.readthedocs.io/en/latest/extensions/contents.html"


# Exit the Script

#>
