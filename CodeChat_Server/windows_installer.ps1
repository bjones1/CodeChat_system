# **************************************************
# |docname| - Windows PowerShell Installation Script
# **************************************************
#
# Pre-Script Definitions
# ----------------------
# Automatically moves PowerShell to the user directory; when using Powershell as an admin as the default admin location is in ``Windows/System32``.
cd $env:USERPROFILE

# Version of python required, put into both string and array form to be easier to parse and output
$pythonVersionReq = '3.7.0'
$pythonVersionReqArray = '3','7','0'


# Checking if Python is Installed
# ===============================
# .. note::
# 2>&1 Sends errors (2) and success output (1) to the success output stream. (PS> man about_Redirection)
# %{ "$_" } converts objects on the error stream to strings
# (https://stackoverflow.com/questions/10666101/lastexitcode-0-but-false-in-powershell-redirecting-stderr-to-stdout-gives/12866669) 
$pythonVersion = python --version 2>&1 | %{ "$_" }

# Case 1: No Python
# -----------------
# sometimes the ``pythonVersion`` variable is empty other times it contains "Python was not found..."
if (([string]::IsNullOrEmpty($pythonVersion)) -or (($pythonVersion.StartsWith("Python was")))) {
    # clear screen to hide confusing or conflicting powershell error message(s)
    cls
    echo "Python $pythonVersionReq or later required. Type 'python' and press "
    echo "Enter to install from Microsoft Store, then rerun script."
    # blank line
    echo "`n"
    # abort script
    exit
}

# Split the ``pythonVersion`` variable into an array.
$pythonVersion = $pythonVersion.Split()[1]  # 3.10.6
$pythonVersionMaj = $pythonVersion.Split('.')[0] # 3
$pythonVersionMin = $pythonVersion.Split('.')[1] # 10

# Case 1: Old Python 2
# --------------------
if ($pythonVersionMaj -lt $pythonVersionReqArray[0]) {
    cls
    echo "Python $pythonVersionReq or later required. Install Python 3 from"
    echo "the Microsoft Store at"
    echo "https://apps.microsoft.com/store/detail/python-310/9PJPW5LDXLZ5?hl=en-us&gl=US"
    echo "then rerun script."
    echo "`n"
    exit
}

# Case 2: Old Python 3
# --------------------
if (([int]$pythonVersionMaj -ne [int]$pythonVersionReqArray[0]) -or ([int]$pythonVersionMin -lt [int]$pythonVersionReqArray[1])) {
    echo $pythonVersion
    echo "Unable to detect Python version. Check that Python $pythonVersionReq"
    echo "or later is installed, and that it is present in the path."
    exit
}

# Creating codechat venv
# ----------------------
# We do this so that our installation does not mess with any Python libraries.
echo "Creating codechat venv..."
$codechat = Get-Item codechat -ErrorAction SilentlyContinue
if ([string]::IsNullOrEmpty($codechat)) {
    # Create a virtual enviroment named codechat
    python -m venv codechat
    echo "virtual environment successfully created"
} else {
        echo "'codechat' virtual environment already found, skipping this step."
}
# find CodeChat_Server.exe and tell user if just updating or installing
$CodeChat_Server = Get-Command $env:USERPROFILE\codechat\Scripts\CodeChat_Server -ErrorAction SilentlyContinue
if ([string]::IsNullOrEmpty($CodeChat_Server)) {
    # Install the CodeChat Server
    echo "installing CodeChat_Server"
    codechat\Scripts\python -m pip install --upgrade CodeChat_Server
    echo "CodeChat_Server successfully installed"
} else {
    # Update the CodeChat Server
    echo "CodeChat_Server found, running update"
    codechat\Scripts\python -m pip install --upgrade CodeChat_Server
    echo "CodeChat_Server successfully updated"
}

# Copies path of CodeChat_Server to the clipboard for easy pasting and displays path in terminal
$pathToCodeChat = Get-Command $env:USERPROFILE\codechat\Scripts\CodeChat_Server | Select-Object -ExpandProperty Definition
Set-Clipboard $pathToCodeChat
echo "Here is your path to CodeChat (Also copied to your clipboard): $pathToCodeChat"
echo "Now add this path to your plugin's setup - see"
echo "https://codechat-system.readthedocs.io/en/latest/extensions/contents.html"
