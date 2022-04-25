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
- how to proceed with fixing the ``window_onclick()`` issue.
- How to make codechat operate off of our changes
- How to make vscode codechat push to a browser

## Notes between Scrum 1-2

- Worked on getting window_onclick to register, right now it is simply a function within ``runclient()`` we need a way to get to ``window_onclick()``

    - My thoughts are this, when you click on a link an event is created, this is read by `CodeChat_client.js` and then pushed out to the browser (lines 112-147). This code takes the flag and says "is this a url flag?" if that is true then it does what is necessary to pull up the url (although this doesn't seem to be working for me?) There are two types of doing this, inital url loading and "User Navigation" (which is basically when you click on a link)

    - What I think we need to do is get/create an event when we click any text, make sure that we have a flag type in GetResultType, and then put in the event booleans a check for this flag. When that flag comes up as true we do what we need to (Hopefully only call ``window_onclick()`` and that sends the info to the server. From there we have to handle the movement of the cscroll bar in vscode based off of what .\

        - ``getRangeAt()`` might be useful for this

    - also need to add ``s`electionAnchorChoords()`` from [Enki](https://github.com/bjones1/enki/blob/master/enki/plugins/preview/preview_sync.py#L556), this could go outside of ``runclient()`` or inside I think

## Scrum 2
- Get `CodeChat_client.js` to recognize click on html
- Get `render_manager.py` to react to `CodeChat_client.js`'s recognition of click
