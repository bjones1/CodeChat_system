https://github.com/bjones1/CodeChat_system/issues/24

# Proposed Features

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


# Important info
## Getting Started on working on Sync.
I'd start off by looking at the files, specifically in the functions
- `CodeChat_client.js`
    - ``runclient()``
        - ``send_to_codechat_server()``
        - ``selectionAnchorCoords()``
        - ``window_onclick()``
    - ``findpos()``
- `render_manager.py`
    - ``read_websocket_handler()`` wow that's hard to find, 
        **ctrl+f(elif msg == "coordinates":)** to find the right area

`CodeChat_Client.html` is not as important, as we're doing the response to the clicking programmatically and not by hard coding it (Thankfully).

## Getting Setup
If you're working on the javascript to fix window_onclick
- Make sure that you will output your renders to a web browser 
    - File -> Preferences -> Settings -> Search(CodeChat)
    - Set Client Location to browser (this will load in your default, I used edge and it worked fine)
- In the web browser use f12 to open the editor and ctrl+f5 to reload the browser code (You'll do this to test any and every change you make)

No Matter What
- Make sure that your CodeChat_Server is pointing to your working directory for all it's stuff
    - activate your virtual enviroment in command prompt
    - cd to your working directory
    - run ``python -m pip install -e .``


## The JavaScript
This basically runs the client. This part of CodeChat is what we're looking at to make sure our documentation isn't borked. I'm actually using it now to check this documentation.

So anyway, the javascript, along with the css (but we don't have to touch that), determines how the user interacts with the browser. This is done primarily through ``runclient()`` and it's definitions and member functions. Think of ``runclient`` as a weird sort of class. This "class" has member functions and variables. The variables are all defined right up at the top, but the one that's important to us is ``outputElement`` This variable contains all of the information on the output window object, which is where our beautiful documentation is shown. 

There's a bunch of stuff that ``runclient`` does, but we're focused on specifically when the functionality of a click is implemented. 

This is done right at the end of the websocket build message.
1. This happens when the webpage gets the event ``ws.onmessage`` 
2. If the event is a ``url`` ``runclient`` does whole bunch of browser shenanigans to load up the page, but all we care about is that when the rendering is done, no matter if it was the initial render or one done due to user navigation, that ``onclick`` is set to run our ``window_onclick``
3. This function 
    1. Grabs the place on the document where we clicked
    2. Makes a selection from the beginning of the document to there
    3. Finds the location of the click in reference to the total string of the webpage
    4. Sends all that to the server with ``send_to_codechat_server``.

## The Render_Manager
Right now it just prints out the data when it gets ``msg == "coordinates"``.
This is printed out to the `cmd` console. This is important, you can only see this by running the codechat_server in serve mode and keeping the command window open.

That data being:
- ``coords``: The coordinates of the click (look into ``selectionAnchorCoords`` and ``findpos`` for more info)
- ``length``: The length of the selection from the beginning of the doc to where was clicked
- ``text``: and the whole darn webpage's contents

it is up to you to implement the rest

You'll need to interact with VSCode, Dr. Jones recommended looking into the hyperlink project's solution for that.

You'll probably also need some fuzzy search.

# Previous Development
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

    - What I think we need to do is get/create an event when we click any text, make sure that we have a flag type in GetResultType, and then put in the event booleans a check for this flag. When that flag comes up as true we do what we need to (Hopefully only call ``window_onclick()`` and that sends the info to the server. From there we have to handle the movement of the cscroll bar in vscode based off of what.

        - ``getRangeAt()`` might be useful for this

    - also need to add ``selectionAnchorChoords()`` from [Enki](https://github.com/bjones1/enki/blob/master/enki/plugins/preview/preview_sync.py#L556), this could go outside of ``runclient()`` or inside I think

## Scrum 2
- Get `CodeChat_client.js` to recognize click on html
- Get `render_manager.py` to react to `CodeChat_client.js`'s recognition of click
