https://github.com/bjones1/CodeChat_system/issues/24

# Features

- recognize a click on the screen
- get the coordinates of the click
- send coordinates to the server
- then move the other screen to the location

# Repositories / Files

- [CodeChat_system](https://github.com/bjones1/CodeChat_system)
- [Enki](https://github.com/bjones1/enki/blob/master/enki/plugins/preview/preview_sync.py#L556)
- /conf.py
- /CodeChat_Server/CodeChat_Server/render_manager.py
- /CodeChat_Server/CodeChat_Server/CodeChat_Client/static/CodeChat_client.js
- /CodeChat_system/CodeChat_Server/CodeChat_Server/CodeChat_Client/templates/CodeChat_client.html

# Libraries, Languages, Interfaces

- Javascript
- Python
- HTML

# Steps

Our main priority is fixing the html error in the window_onclick() function.
Our Secondary Objective is to scroll the code window (by random amounts) on any click on the html

# Tests
- Get window_conclick to proceed without errors
- Get render_manager.py to recognize click and scroll the window

# Goals

**Implement sync between text and rendered code.**
    
Sync functionality for the CodeChat system in Visual Studio Code.
Feature will allow the user to click parts of the HTML window and be taken to that section of code.

## Scrum 1

**Confer with Dr. Jones, Zach, and Austin on:**
- status of code
- how to proceed with fixing the window_onclick() issue.
- How to make codechat operate off of our changes
- How to make vscode codechat push to a browser

## Scrum 2
- Get ``CodeChat_client.js`` to recognize click on html
- Get ``render_manager.py`` to react to ``CodeChat_client.js``'s recognition of click
