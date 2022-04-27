# *********************************
# **Read Me for Hyperlink Project**
# *********************************
# Project Description: Modify the existing CodeChat code so that it properly hyperlinks the file and the line. 
#
# .. contents:: Table of Contents
#   :depth: 3
#
# Class of Spring 2022 Group 1
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# 1. Describes the feature you will add.
        # * For this project, we will modify the existing CodeChat code so that it properly hyperlinks the file and the line. During this process, we will document any relevant information such as an explanation on ‘Regular Expressions’ in addition to any changes that we make.
#
# 2. Defines which repository/repositories your code will be added to.
        # * Documentation and code will be merged into the branch at CodeChat_system.
#
# 3. Specifies what libraries, languages, and interfaces your code must work with.
        # * Our code is primarily going to be written in JavaScript. I think that any edits should continue to work on any operating system that is already running CodeChat.
#
# 4. Details a series of steps you will follow to complete this feature.
        # * The first step in this coding project is understanding how hyperlinks are currently handled in CodeChat.
#
# 5. Defines tests to show the feature works correctly.
        # * The exact formatting is to be determined. We will test the error hyperlinking with multiple different types of errors. Another project requirement is that the hyperlink should bring you to the line as well as highlight the line that contains the error.
#
# *Work Done:*
# ===================
# Getting your Own Copy of CodeChat
# ------------------------------------
# By JP Gathings and Logan Johnson
# You will need an online copy of the project stored on your GitHub account (a fork), and a local version of the project you can edit on your hard drive (a clone).
# Things you will need:
        # * VS Code
        # * Codechat
        # * Codechat extension for VS Code
        # * SmartGit
# Forking
# -----------------
# First fork the CodeChat system to your profile from `Github <https://github.com/bjones1/Codechat_system>`_.
        # 
        # .. image:: Photos/Hyperlink-readmefile-image1.png
# 
# Cloning
# -------------
        # * Forking should take you to your fork of CodeChat. Once there, click on the green code icon, and copy
        #
        # .. image:: Photos/Hyperlink-readmefile-image2.png
        #
        # * Now open SmartGit. Click Repository at the top, then Clone. Paste the copied link into the Repository URL box and follow the prompts until the dialogues have stopped (next, next, finish).
        #
        # .. image:: Photos/Hyperlink-readmefile-image3.png
        #
        # * Make note of where the repository is on your computer by right clicking the repository in SmartGit under the Repositories pane and clicking Open in Explorer.
        #
        # .. image:: Photos/Hyperlink-readmefile-image4.png
        #
# ..  note:: You can try opening a file in this folder like README.rst to check if you need myst_parser. Open it in VS code and run codechat next to it. If you get the error “Could not import extension myst_parser” follow the instructions below.
# ..  note:: This clone of CodeChat that you make edits to is probably not currently the one that creates the window for you in VSCode. That copy is in your virtual environment. See Reinstalling CodeChat Server for more information.
#
# Editing the CodeChat System
# --------------------------------
# **Installing myst_parser**
#
# Windows:
        # * Open a terminal window and activate your virtual environment.
                # * In Windows - command should be “codechat\Scripts\activate” then press enter
                # * In Ubuntu  - command should be "source codechat\bin\activate" then press enter 
                # * Then in the same command window “pip install myst_parser”
# **Reinstalling CodeChat Server**
#
# First check where the CodeChat server is. (the one that runs in VSCode aka the one your virtual environment uses)
        # * To do this, activate your virtual environment
                # * In Windows - command should be “codechat\Scripts\activate” then press enter
                # * In Ubuntu  - command should be "source codechat\bin\activate" then press enter 
        # * Then find your installation by typing “pip show codechat_server”
                # * Under Location, you can copy this address and paste it into the top of a file explorer window to open it. This is where the CodeChat server your virtual environment knows about is currently installed. If this file location is not in your new cloned directory from Getting Your Own Copy of CodeChat, continue following along this section. 
                # * Below is an example of what it will look like if your server is in the wrong place.
        #
        # .. image:: Photos/Hyperlink-readmefile-image5.png
        #
# Now that you know your CodeChat server is not in your editable repository we are going to move it to the right spot.
        # * Go back to your activated virtual environment. (repeat the first step of this section if you closed the window)
        # * We need to cd to wherever your clone is installed.
                # * To do this, open a window in file explorer and navigate to your cloned repository titled CodeChat_system.
                # * Dig in file explorer to “CodeChat_system\CodeChat_Server”
        # * Highlight and copy that file path from the top of the file explorer: 
        #
        # .. image:: Photos/Hyperlink-readmefile-image6.png
        #
# Now open up the activated virtual environment and type “cd <paste that filepath>”
        #
        # .. image:: Photos/Hyperlink-readmefile-image7.png
        #        
# * Now that we are in the proper place, we can reinstall it.
        # * Type “pip install -e .” (the space and period is intentional) and press enter.
        # * Now check to make sure it worked by typing “pip show codechat_server”
                # * If it shows your local clone then you are good.
        #
        # .. image:: Photos/Hyperlink-readmefile-image8.png
        #
# **See Print Statements From the CodeChat Server**
        # * Close the CodeChat window in VS code.
        # * Open the command prompt and activate your CodeChat virtual environment. (codechat\Scripts\activate)
        # * Type “codechat_server serve” and press enter.
        #
        # .. image:: Photos/Hyperlink-readmefile-image9.png
        #
        # * Open a file that is properly formatted for CodeChat and run the CodeChat extension in VS Code.
        # * Create an error (mess up the heading underline on line 25 of render_manager.py)
        # * Click the hyperlink the error created.
        # * Check the command prompt for the print statement.
        #
        # .. image:: Photos/Hyperlink-readmefile-image10.png
        #
# **Making Edits to .js Files**
# 
# You may notice that changing the .js files doesn’t actually do anything. This is likely because there are multiple cached files getting reloaded such that your edits never make it through.
#
# .. note:: there is more than one way to do this, but following in this order first will help you get used to it.
        # 1. Close any form of CodeChat and open the file you want to edit. In this case we are looking at CodeChat_client.js
        # 2. Make your edits and save the file.
        # 3. Open a command prompt window and activate your codechat virtual environment (codechat\Scripts\activate) then type “codechat_server serve” (this allows you to view any print statements from the python server.)
        # 4. Open the corresponding html file. 
                # a. For CodeChat_client.js it is found here: \CodeChat_system\CodeChat_Server\CodeChat_Server\CodeChat_Client\templates\CodeChat_client.html.
        # 5. Change the name of the file that is cached to be loaded so it forces a reload. It will be the name of the javascript file you are trying to edit. You can easily do this by changing the number after v=”#”. (If it is v=3, I change it to v=4 and vice versa.) See below:
        #
        # .. image:: Photos/Hyperlink-readmefile-image11.png
        #
        # 6. Run codechat (If in VSCode ctrl-shift-P > CodeChat)
        # 7. If you make other edits, you can avoid reopening the terminal window by typing ctrl-C to quit the server, then changing the html, then running codechat in VS Code again (you don’t even need to close the dead codechat window for it to reload.
# Side Notes:
# -------------------
        # * The parsing part of this project is in javascript. The part that would open it in your editor is a combination of some Python code.
                # * The javascript has to send a message to the server in Python. Then the Python server has to send a message back to VS code for you to see it.
        # * The python server is located in CodeChat_system\CodeChat_Server\CodeChat_Server
                # * Mainly in server.py
        # * Regular expressions
                # * Right now the regular expression basically matches the entire line. Good for finding the line but bad because it finds too much.
                # * To play with regular expressions in a controlled environment go to: https://regex101.com/
                # * The following javascript site works well with the test site above: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_Expressions 
        # * Client side javascript
                # * Found in CodeChat_system\CodeChat_Server\CodeChat_Server\CodeChat_Client\static\CodeChat_client.js
                # * The server basically feeds the error messages it gets from running a build (a build meaning: saving a file and waiting it to show up on the CodeChat window in VS code) to the client and the client parses that that and is hyperlinking it.
                # * Most of the way down this file (line 329) there is a big chunk of documentation on the regex used to find the error messages and turn that into a hyperlink.
                # * Line 403 creates the link. The hyperlink supposedly calls the “navigate to error” function which doesn’t do anything yet.
                        # * The navigate_to_error function is on line 293 – this is phase 2 of the project, when defining what happens when the link is clicked.
        # * renderManager.py- creating a function for the link
                # * On line 363, this is where the sendToCodeChat function’s possible arguments are handled as the message is sent to the websocket.
                # * The server is the codechat server. The client is the html/javascript rendering you see in VS code. A websocket allows the server to send a message to the client anytime it wants. It also allows the client to send a message back to the server. 
                # * So the navigate_to_error function sends a message over the websocket to the server saying that something happened. In renderManager on line 436 (we are in the server here), the navigate_to_error function should be printing it.
        # * This line is where the function for 
        # * Get the hyperlink so it displays correctly first. Then have it do something.
                # * If the error message has a line number, the link should open that file and go to that line number. If there is no line number, the hyperlink should just open that file.
# *Given code in C was:*
    # Create a hyperlink to navigate to the error.
          #return `<a href='javascript:navigate_to_error(${JSON.stringify(
          #file_path
          #)}, ${line})' class="error_link">${match_text}</a>`;
# *What is was changed to in C:*
      #Extract the warning/error message from match_text
        #let just_text = match_text.replace(file_path, '')
        #just_text = just_text.replace(line, '')

        #Delete the first 3 characters (they are always ':: ' with how the string is currently made)
        #just_text = just_text.substring(3, just_text.length)

        #Display the error message and create a hyperlink to navigate to the error.
        #return `${just_text}\n<a href='javascript:navigate_to_error(${JSON.stringify(
                #file_path
            #)}, ${line})' class="error_link">${file_path}\nLine: ${line}</a>`;
#
# Class of Spring 2022 Group 2
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# 1. Describes the feature you will add.
        # * The group before us updated the CodeChat code so that it properly hyperlinks the file and the line. We will be double checking that this works.
#
# 2. Defines which repository/repositories your code will be added to.
        # * Will be creating a read me file-hyperlink debugging project to keep track of our research and update this issue with the link to it for the next group.
#
# 3. Specifies what libraries, languages, and interfaces your code must work with.
        # * Neither of us are familiar with JavaScript. We would have to go through a crash course to learn this code. IF we are able to use C, Python, or HTML would be easier for us.

#
# 4. Details a series of steps you will follow to complete this feature.
        # * Our first step is trying to figure out what the previous group did, where they left off, and what is next.
#
# 5. Defines tests to show the feature works correctly.
        # * We will be testing what the previous group did by generating common errors.
#
#
# *Work Done:*
# ===================
# The previous group took the Create a hyperlink code and updated to clean up the string to where it was more read able when displayed at the bottom. 
# Changed the hyperlink word doc to python to make it readable in codechat.
#
# Open Items
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# List:
        # * Create hyper link to common error page. 
        # * Update common error page with fixes. 
        # * Test out errors. 
                # * Windows - Completed
                # * Linux - tested- hyperlink doesn't go anywhere but does give a number to where the error is at.
                # * Mac 