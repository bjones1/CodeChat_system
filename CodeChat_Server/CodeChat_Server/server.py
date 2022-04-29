# .. Copyright (C) 2012-2022 Bryan A. Jones.
#
#   This file is part of the CodeChat System.
#
#   The CodeChat System is free software: you can redistribute it and/or
#   modify it under the terms of the GNU General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   The CodeChat System is distributed in the hope that it will be
#   useful, but WITHOUT ANY WARRANTY; without even the implied warranty
#   of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#   General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with the CodeChat System.  If not, see
#   <http://www.gnu.org/licenses/>.
#
# *******************************
# |docname| - The CodeChat Server
# *******************************
# The CodeChat Server receives requests from the editor/IDE, renders these, then displays them in the CodeChat Client; likewise, it listens for CodeChat Client requests, processes them, and forwards the results to the editor/IDE.
#
#
# Imports
# =======
# These are listed in the order prescribed by `PEP 8
# <http://www.python.org/dev/peps/pep-0008/#imports>`_.
#
# Standard library
# ----------------
import logging
from pathlib import Path
import signal
import socket
import sys
from textwrap import dedent
import threading
import webbrowser

# Third-party imports
# -------------------
import bottle
from thrift.server import TServer
from thrift.transport import TTransport
from thrift.transport import TSocket
from thrift.protocol import TBinaryProtocol


# Local application imports
# -------------------------
from . import __version__
from . import render_manager
from .constants import HTTP_PORT, LOCALHOST, THRIFT_PORT, WEBSOCKET_PORT
from .gen_py.CodeChat_Services import EditorPlugin
from .gen_py.CodeChat_Services.ttypes import (
    RenderClientReturn,
    CodeChatClientLocation,
)

# Constants
# =========
UNKNOWN_CLIENT = "Unknown client id {}."

logger = logging.getLogger(__name__)


# Service provider
# ================
# This class implements the EditorPlugin service.
class CodeChatHandler:
    def __init__(self):
        self.render_manager: render_manager.RenderManager
        self.insecure: bool

    # _`get_client`: Return the HTML for a web client.
    def get_client(self, codeChat_client_location: int) -> RenderClientReturn:
        try:
            location_name = CodeChatClientLocation._VALUES_TO_NAMES[
                codeChat_client_location
            ]
        except KeyError:
            location_name = "invalid location"
        logger.info("get_client({})".format(location_name))
        id = self.render_manager.threadsafe_create_client()
        # Get the next ID.
        if id is None:
            ret = RenderClientReturn("", -1, "Duplicate id {}".format(id))
            logger.info("  => {}".format(ret))
            return ret
        if id < 0:
            ret = RenderClientReturn("", -1, "Server is shutting down.")
            logger.info("  => {}".format(ret))
            return ret

        # Return what's requested.
        endpoint = "insecure" if self.insecure else "client"
        url = f"http://{LOCALHOST}:{HTTP_PORT}/{endpoint}?id={id}"
        if codeChat_client_location == CodeChatClientLocation.url:
            # Just return the URL.
            ret_str = url
        elif codeChat_client_location == CodeChatClientLocation.html:
            # Redirect to the webserver.
            ret_str = dedent(
                f"""\
                <!DOCTYPE html>
                <html>
                    <head>
                    </head>
                    <body style="margin: 0px; padding: 0px; overflow: hidden">
                        <iframe src="{url}" style="width: 100%; height: 100vh; border: none"></iframe>
                    </body>
                </html>"""
            )
        elif codeChat_client_location == CodeChatClientLocation.browser:
            # Open in an external browser.
            webbrowser.open(url, new=1, autoraise=True)
            ret_str = ""
        else:
            ret = RenderClientReturn(
                "", -1, "Invalid location {}".format(codeChat_client_location)
            )
            logger.info("  => {}".format(ret))
            return ret

        ret = RenderClientReturn(ret_str, id, "")
        logger.info("  => {}".format(ret))
        return ret

    # Indicate the server is alive.
    def ping(self) -> str:
        logger.info("ping()\n")
        if shutdown_event.is_set():
            # Indicate an error by returning a non-emptry string.
            return "Shutting down."
        return ""

    def gotoFile(self, id_) -> str:
        logger.info("go to file()\n")
        return "test"

    # Render the provided text to HTML, then enqueue it for the web view.
    def start_render(self, text: str, path: str, id: int, is_dirty: bool) -> str:
        logger.info(
            "start_render(path={}, id={}, is_dirty={}, html=\n{}...)\n".format(
                path, id, is_dirty, text[:80]
            )
        )
        if self.render_manager.threadsafe_start_render(text, path, id, is_dirty):
            # Indicate success.
            logger.info(" => (empty string)")
            return ""
        else:
            # If the client specified an non-existant ID, create it.
            if id < 0:
                if self.render_manager.threadsafe_create_client(id) != id:
                    ret = f"Duplicate id {id}."
                    logger.info(f" => {ret}")
                    return ret
                else:
                    # Since we just created this id, start the CodeChat Client in an external browser.
                    webbrowser.open(
                        "http://{}:{}/client?id={}".format(LOCALHOST, HTTP_PORT, id),
                        new=1,
                        autoraise=True,
                    )
                    # Try the render again.
                    if self.render_manager.threadsafe_start_render(
                        text, path, id, is_dirty
                    ):
                        # Indicate success.
                        logger.info(" => (empty string)")
                        return ""

            # Indicate an error.
            ret = UNKNOWN_CLIENT.format(id)
            logger.info(" => {}".format(ret))
            return ret

    # _`Shut down an editor client`. The sequence is complex. Here's a web of links which step throughs the process.
    #
    # _`Delete step 1.` `--> <Delete step 2.>` The editor/IDE invokes stop_client, which delegates to the render manager thread.
    def stop_client(self, id: int) -> str:
        logger.info("stop_client(id={})".format(id))
        ok = self.render_manager.threadsafe_shutdown_client(id)
        if not ok:
            ret = UNKNOWN_CLIENT.format(id)
            logger.info("  => {}".format(ret))
            return ret
        # Indicate success.
        logger.info("  => (empty string)")
        return ""


# Instantiate this class, which will be used by both servers.
handler = CodeChatHandler()


# Servers
# =======
#
# Server for the CodeChat editor plugin
# -------------------------------------
def editor_plugin_server() -> None:
    transport = TSocket.TServerSocket(host=LOCALHOST, port=THRIFT_PORT)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()
    processor = EditorPlugin.Processor(handler)

    # Spawns up to 10 threads by default, then uses those. Mark these threads as daemon, so they will be terminated on program exit.
    server = TServer.TThreadPoolServer(
        processor, transport, tfactory, pfactory, daemon=True
    )
    # Other options for the server:
    #
    # This server spawns a thread per connection.
    ## server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)  # noqa: E266
    # A simpler server:
    ## server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)  # noqa: E266

    try:
        server.serve()
    except Exception:
        # Shut down the server instead of allowing it to keep running in a broken state.
        shutdown_event.set()
        raise


# Server for the CodeChat Client
# ------------------------------
# Serve CodeChat Client files statically.
@bottle.route("/static/<filepath:path>")
def server_static(filepath):
    return bottle.static_file(
        filepath, root=str(Path(__file__).parent / "CodeChat_Client/static")
    )


# The endpoint to get the HTML for the CodeChat Client.
@bottle.route("/client")
def client_html() -> str:
    return bottle.template(
        str(Path(__file__).parent / "CodeChat_Client/templates/CodeChat_client.html"),
        client_id=bottle.request.query.id,
        WEBSOCKET_PORT=WEBSOCKET_PORT,
    )


# Inform users if running in insecure mode.
@bottle.route("/insecure")
def insecure_warning():
    return bottle.template(
        str(Path(__file__).parent / "CodeChat_Client/templates/insecure.html"),
        THRIFT_PORT=THRIFT_PORT,
        HTTP_PORT=HTTP_PORT,
        WEBSOCKET_PORT=WEBSOCKET_PORT,
    )


# The endpoint for files requested by a specific client, including rendered source files. Note that ``int`` by default is `positive only <https://werkzeug.palletsprojects.com/en/2.0.x/routing/#werkzeug.routing.IntegerConverter>`_.
@bottle.route("/client/<id:int>/<url_path:path>")
def client_data(id: int, url_path: str) -> bottle.HTTPResponse:
    # See if we rendered this file.
    html = handler.render_manager.threadsafe_get_render_results(id, url_path)

    # If we have rendered HTML, return it.
    if type(html) == str:
        assert isinstance(html, str)
        response = bottle.HTTPResponse(html)
    else:
        # The file is on disk. Send it or a 404 if nothing was found.
        try:
            # ``static_file`` needs a non-empty root. Windows roots start with a drive letter, while other OSes don't. Use Path to split the overall path nicely to avoid this problem.
            url_path_ = Path(url_path)
            response = bottle.static_file(url_path_.name, root=url_path_.parent)
        except (FileNotFoundError, PermissionError):
            bottle.abort(404)

    # Don't allow the browser to cache files. See the `SO <https://stackoverflow.com/a/24748094/16038919>`__, `bottle API <https://bottlepy.org/docs/dev/api.html#bottle.BaseResponse.add_header>`_, and `MDN docs <https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control#Directives>`_.
    response.add_header("Cache-Control", "no-store, max-age=0")
    return response


# Main code
# =========
# When this event is ``set``, ``run_servers`` will shut down the servers and return.
shutdown_event = threading.Event()


# Handle signals by setting the shutdown event.
def signal_handler(signum, frame):
    shutdown_event.set()


# Handle exceptions in the same way.
def excepthook(type, value, traceback):
    shutdown_event.set()
    sys.__excepthook__(type, value, traceback)


# Run both servers. This does not (usually) return.
def run_servers(
    # See ``INSECURE_HELP`` in the `CLI interface`.
    insecure=False,
    # See the ``--quiet`` option in the `CLI interface`.
    quiet=False,
) -> int:

    print(f"The CodeChat Server, v.{__version__}\n")
    logging.basicConfig(level=logging.INFO)

    # See if the required ports are in use, probably by another instance of this server.
    ports_in_use = [
        str(port)
        for port in (HTTP_PORT, WEBSOCKET_PORT, THRIFT_PORT)
        if is_port_in_use(port)
    ]
    if ports_in_use:
        print(
            f"Error: port(s) {', '.join(ports_in_use)} are already in use.\n"
            "Hopefully, this means that the CodeChat Server is already running in another process.\n"
            "Exiting.\n",
            file=sys.stderr,
        )
        return 1

    # Implement quiet option for all loggers.
    if quiet:
        # Set root logger options.
        logging.getLogger("").setLevel(logging.WARNING)

    # Shut down if any unhandled exception occurs.
    sys.excepthook = excepthook

    # Both servers block when run, so place them in a thread. Mark the servers as a daemon, so they will be killed when the program shuts down.
    handler.insecure = insecure
    editor_plugin_thread = threading.Thread(
        target=editor_plugin_server, name="Editor plugin server", daemon=True
    )
    editor_plugin_thread.start()

    def webserver_launcher(*args, **kwargs):
        try:
            # Omitting the ``quiet`` option causes the server Bottle uses by default (Python's stdlib wsgiref) to die when emitting stdio if run with the ``CodeChat_Server start`` option (where the stdio/stderr gets disconnected after the server is started). Therefore, the ``CodeChat_Server start`` command always invokes ``CodeChat_Server serve --quiet``.
            bottle.run(*args, quiet=quiet, **kwargs)
        except Exception:
            # Shut down the server instead of allowing it to keep running in a broken state.
            shutdown_event.set()
            raise

    server_host = "0.0.0.0" if insecure else LOCALHOST
    webserver_thread = threading.Thread(
        target=webserver_launcher,
        kwargs=dict(host=server_host, port=HTTP_PORT),
        name="Webserver",
        daemon=True,
    )
    webserver_thread.start()

    # Start the render loop in another thread.
    handler.render_manager = render_manager.RenderManager(shutdown_event)
    render_manager_thread = threading.Thread(
        target=handler.render_manager.run, name="asyncio", args=(server_host,)
    )
    render_manager_thread.start()

    # On a signal, shut down gracefully.
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    # Run the servers in threads until a user-requested shutdown occurs.
    while True:
        # Ctrl+C is ignored while waiting, so use a 1 second poll.
        if shutdown_event.wait(1):
            # If the event is received, exit the loop in order to shut down. First, clear the event so the next invocation of this function will work correctly.
            shutdown_event.clear()
            break

    logger.info("Shutting down...")
    # This will prevent future editor or web requests from being serviced.
    handler.render_manager.threadsafe_shutdown()
    # When this is done, the Flask server and editor plugin sever can be shut down, since they're idle. Since they're daemons, they'll be shut down by exiting main.
    render_manager_thread.join()
    return 0


# Inspired by Stack Overflow. The original post used ``connect_ex``, which is very slow (~2 seconds).
def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Allow reusing sockets in the TIME_WAIT state -- see the `Python docs <https://docs.python.org/3/library/socket.html#notes-on-socket-timeouts>`_.
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.bind((LOCALHOST, port))
        except OSError:
            return True
        return False
