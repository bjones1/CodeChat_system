
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
$pythonOK = $false
 
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

if([int]$pythonVersionMin -lt [int]$pythonVersionReqArray[1]) {
    
    cls    
    
    echo "Python $pythonVersionReq or later required. Update Python or install latest version from Microsoft Store (https://apps.microsoft.com/store/detail/python-310/9PJPW5LDXLZ5?hl=en-us&gl=US), then rerun script."
    
    echo "`n"     
    
    Exit   
    
    }

# Case 4: Python 3
# -----------------
# "Python 3.10.6"

if(([int]$pythonVersionMaj -eq [int]$pythonVersionReqArray[0]) -and ([int]$pythonVersionMin -ge [int]$pythonVersionReqArray[1])) {

    # echo "python ok"
    $pythonOK = $true
    
    }
else {
    
    echo $pythonVersion
    
    echo "Unable to detect Python version. Check that Python $pythonVersionReq or later is installed, and that it is present in the path"
    
    Exit
    
    }

# Creating codechat venv
# ----------------------
## We do this so that our installation does not mess with any other installations of python

if ($pythonOK) {
    echo "Creating codechat venv..."
    $codechat = Get-Item codechat -ErrorAction SilentlyContinue
    if([string]::IsNullOrEmpty($codechat)){
        # Create a virtual enviroment named codechat
        python -m venv codechat
        echo "virtual environment successfully created"
    }
    else {
        echo "'codechat' virtual environment already found, skipping this step"
    }

    # find CodeChat_Server.exe and tell user if just updating or installing

    $CodeChat_Server = Get-Command $env:USERPROFILE\codechat\Scripts\CodeChat_Server -ErrorAction SilentlyContinue
    if([string]::IsNullOrEmpty($CodeChat_Server)){
        # Install the CodeChat Server
        echo "installing CodeChat_Server"
        codechat\Scripts\python -m pip install --upgrade CodeChat_Server
        echo "CodeChat_Server successfully installed"
    }
    else {
        # Update the CodeChat Server
        echo "CodeChat_Server found, running update"
        codechat\Scripts\python -m pip install --upgrade CodeChat_Server
        echo "CodeChat_Server successfully updated"
    }

    # Copies path of CodeChat_Server to the clipboard for easy pasting and displays path in terminal
    $pathToCodeChat = Get-Command $env:USERPROFILE\codechat\Scripts\CodeChat_Server | Select-Object -ExpandProperty Definition
    Set-Clipboard $pathToCodeChat
    echo "Here is your path to CodeChat (Also copied to your clipboard): $pathToCodeChat"
    echo "Now add this path to your plugin's setup - see https://codechat-system.readthedocs.io/en/latest/extensions/contents.html"
}

else {Exit}