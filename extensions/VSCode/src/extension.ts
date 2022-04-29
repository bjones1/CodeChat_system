// .. Copyright (C) 2012-2020 Bryan A. Jones.
//
//  This file is part of the CodeChat System.
//
//  The CodeChat System is free software: you can redistribute it and/or
//  modify it under the terms of the GNU General Public License as
//  published by the Free Software Foundation, either version 3 of the
//  License, or (at your option) any later version.
//
//  The CodeChat System is distributed in the hope that it will be
//  useful, but WITHOUT ANY WARRANTY; without even the implied warranty
//  of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
//  General Public License for more details.
//
//  You should have received a copy of the GNU General Public License
//  along with the CodeChat System.  If not, see
//  <http://www.gnu.org/licenses/>.
//
// *****************************************************
// |docname| - The CodeChat Visual Studio Code extension
// *****************************************************
// This extension creates a webview (see `activation/deactivation`_), then uses `CodeChat services`_ to render editor text in that webview.
//
// Remote operation
// ================
// This extension doesn't fully work when running remotely. Specifically, the web browser in VSCode can't talk with the CodeChat Server via a websocket, since the server runs on the remote host while `the web browser (a WebView) runs locally <https://code.visualstudio.com/api/advanced-topics/remote-extensions#using-the-webview-api>`_. While the solutions on that page seem helpful, they don't support websocket connections (see the ``portMapping`` dropdown text in `WebViewOptions <https://code.visualstudio.com/api/references/vscode-api#WebviewOptions>`_). The workaround: use an external browser (running on the remote host).
//
//
// Requirements
// ============
// Node.js packages
// ----------------
import assert = require("assert");
import child_process = require("child_process");

// Third-party packages
// --------------------
import escape = require("escape-html");
import shlex = require("shlex");
import thrift = require("thrift");
import vscode = require("vscode");

// Local packages
// --------------
import EditorPlugin = require("./gen-nodejs/EditorPlugin");
import ttypes = require("./gen-nodejs/CodeChat_Services_types");

// Globals
// =======
// These globals are truly global: only one is needed for this entire plugin.
//
// The Thrift network connection to the CodeChat Server.
let thrift_connection: thrift.Connection | undefined;
// The Thrift client using this connection.
let thrift_client: EditorPlugin.Client | undefined;
// Where the webclient resides: ``html`` for a webview panel embedded in VSCode; ``browser`` to use an external browser.
let codechat_client_location: ttypes.CodeChatClientLocation =
    ttypes.CodeChatClientLocation.html;
// True if the subscriptions to IDE change notifications have been registered.
let subscribed = false;

// A unique instance of these variables is required for each CodeChat panel. However, this code doesn't have a good UI way to deal with multiple panels, so only one is supported at this time.
//
// The id of this render client, assigned by the CodeChat Server.
let codechat_client_id: number | undefined;
// The webview panel used to display the CodeChat Client
let webview_panel: vscode.WebviewPanel | undefined;
// A timer used to wait for additional events (keystrokes, etc.) before performing a render.
let idle_timer: NodeJS.Timeout | undefined;

// Activation/deactivation
// =======================
// This is invoked when the extension is activated. It either creates a new CodeChat instance or reveals the currently running one.
export function activate(context: vscode.ExtensionContext) {
    context.subscriptions.push(
        vscode.commands.registerCommand("extension.codeChat", async () => {
            console.log("CodeChat extension starting HEllo.");
            const path = '/Users/aaronpowell/Approaches to Firmware Development/CodeChat_system_dev/CodeChat_Server/CodeChat_Server/render_manager.py'
            const fileName =  vscode.Uri.file(path)
            let previewDoc = await vscode.workspace.openTextDocument(fileName)
            let previewEditorShowOptions: vscode.TextDocumentShowOptions = {
                viewColumn: vscode.ViewColumn.Beside, 
                preview: true,
                preserveFocus: true,
                selection: new vscode.Selection(new vscode.Position(0, 0), new vscode.Position(0, 0))
            };
            await vscode.window.showTextDocument(previewDoc,previewEditorShowOptions);
            // let activeTextEditor = vscode.window.activeTextEditor;
            // provider.show(fileName, activeTextEditor.document.uri, activeTextEditor.selections);
                // let previewDocument = await vscode.workspace.openTextDocument(previewUri);
                // let previewEditorShowOptions: vscode.TextDocumentShowOptions = {
                //     viewColumn: vscode.ViewColumn.Beside, 
                //     preview: true,
                //     preserveFocus: true,
                //     selection: new vscode.Selection(new vscode.Position(0, 0), new vscode.Position(0, 0))
                // };

            // await vscode.window.showTextDocument(doc, { preview: false });

            if (!subscribed) {
                subscribed = true;

                // Render when the text is changed by listening for the correct `event <https://code.visualstudio.com/docs/extensionAPI/vscode-api#Event>`_.
                context.subscriptions.push(
                    vscode.workspace.onDidChangeTextDocument((event) => {
                        start_render();
                    })
                );

                // Render when the active editor changes.
                context.subscriptions.push(
                    vscode.window.onDidChangeActiveTextEditor((event) => {
                        start_render();
                    })
                );
            }

            // Get the CodeChat Client's location from the VSCode configuration.
            const codechat_client_location_str = vscode.workspace
                .getConfiguration("CodeChat.CodeChatServer")
                .get("ClientLocation");
            assert(typeof codechat_client_location_str === "string");
            switch (codechat_client_location_str) {
                case "html":
                    codechat_client_location =
                        ttypes.CodeChatClientLocation.html;
                    break;

                case "browser":
                    codechat_client_location =
                        ttypes.CodeChatClientLocation.browser;
                    break;

                default:
                    assert(false);
            }

            // Create or reveal the webview panel; if this is an external browser, we'll open it after the client is created.
            if (
                codechat_client_location === ttypes.CodeChatClientLocation.html
            ) {
                if (webview_panel !== undefined) {
                    // As below, don't take the focus when revealing.
                    webview_panel.reveal(undefined, true);
                } else {
                    // Create a webview panel.
                    webview_panel = vscode.window.createWebviewPanel(
                        "CodeChat",
                        "CodeChat",
                        {
                            // Without this, the focus becomes this webview; setting this allows the code window open before this command was executed to retain the focus and be immediately rendered.
                            preserveFocus: true,
                            // Put this in the a column beside the current column.
                            viewColumn: vscode.ViewColumn.Beside,
                        },
                        // See WebViewOptions_.
                        {
                            enableScripts: true,
                            // Note: Per the `docs <https://code.visualstudio.com/api/advanced-topics/remote-extensions#option-2-use-a-port-mapping>`__, there's a way to map from ports on the extension host machine (which may be running remotely) to local ports the webview sees (since webviews always run locally). However, this doesn't support websockets, and should also be in place when using an external browser. Therefore, we don't supply ``portMapping``.
                        }
                    );
                    // TODO: do I need to dispose of this and the following event handlers? I'm assuming that it will be done automatically when the object is disposed.
                    webview_panel.onDidDispose((event) => {
                        // Shut down the render client when the webview panel closes.
                        console.log("CodeChat extension: shut down webview.");
                        stop_client();
                        webview_panel = undefined;
                    });

                    // Render when the webview panel is shown.
                    webview_panel.onDidChangeViewState((event) => {
                        start_render();
                    });
                }
            }

            // Provide a simple status display while the CodeChat System is starting up.
            if (webview_panel !== undefined) {
                // If we have an ID, then the GUI is already running; don't replace it.
                if (codechat_client_id === undefined) {
                    webview_panel.webview.html =
                        "<h1>CodeChat</h1><p>Loading...</p>";
                }
            } else {
                vscode.window.showInformationMessage(
                    "CodeChat is loading in an external browser..."
                );
            }

            // Start the server.
            try {
                await start_server();
            } catch (err) {
                assert(err instanceof Error);
                show_error(err.message);
                return;
            }

            if (thrift_connection === undefined) {
                console.log("CodeChat extension: creating Thrift client.");
                // The client should never exist if there's no connection.
                assert(thrift_client === undefined);

                // Try to connect to the CodeChat Server. The `createConnection function <https://github.com/apache/thrift/blob/master/lib/nodejs/lib/thrift/connection.js#L258>`_ wraps `net.createConnection <https://nodejs.org/api/net.html#net_net_createconnection_options_connectlistener>`_ then returns a `Connection object <https://github.com/apache/thrift/blob/master/lib/nodejs/lib/thrift/connection.js#L35>`_.
                //
                // This must use the `CodeChat service port <CodeChat service port>`.
                thrift_connection = thrift.createConnection(
                    "localhost",
                    ttypes.THRIFT_PORT,
                    {
                        transport: thrift.TBufferedTransport,
                        protocol: thrift.TBinaryProtocol,
                    }
                );

                let was_error: boolean = false;

                thrift_connection.on("error", function (err) {
                    console.log(
                        `CodeChat extension: error in Thrift connection: ${err.message}`
                    );
                    was_error = true;
                    show_error(
                        `Error communicating with the CodeChat Server: ${err.message}. Re-run the CodeChat extension to restart it.`
                    );
                    // End the connection, to hopefully avoid the socketing entering the ``TIME-WAIT`` state.
                    assert(thrift_connection);
                    thrift_connection.end();
                    // The close event will be `emitted next <https://nodejs.org/api/net.html#net_event_error_1>`_; that will handle cleanup.
                });

                thrift_connection.on("close", (hadError) => {
                    console.log(
                        "CodeChat extension: closing Thrift connection."
                    );
                    // If there was an error, the event handler above already provided the message. Note: the `parameter hadError <https://nodejs.org/api/net.html#net_event_close_1>`_ only applies to transmission errors, not to any other errors which trigger the error callback. Therefore, I'm using the ``was_error`` flag instead to catch non-transmission errors.
                    if (!was_error && hadError) {
                        show_error(
                            "The connection to the CodeChat Server was closed due to a transmission error. Re-run the CodeChat extension to restart it."
                        );
                    }
                    thrift_connection = undefined;
                    // Since the connection is closed, we can't gracefully shut down the client via ``stop_client()``. Simply mark it as undefined so it will be re-created.
                    thrift_client = undefined;
                    codechat_client_id = undefined;
                    idle_timer = undefined;
                });

                thrift_connection.on("connect", () => {
                    assert(thrift_connection !== undefined);
                    get_render_client(thrift_connection);
                });
            } else {
                // If this was invoked while a connection is still pending, let that connection run its course.
                if (!thrift_connection.connection.connecting) {
                    get_render_client(thrift_connection);
                } else {
                    console.log(
                        "CodeChat extension: connection already pending, so a new client wasn't created."
                    );
                }
            }
        })
    );
}

// On deactivation, close everything down.
export async function deactivate() {
    console.log("CodeChat extension: deactivating.");
    stop_client();
    webview_panel?.dispose();
    console.log("CodeChat extension: deactivated.");
}

// CodeChat services
// =================
// Get the render client from the CodeChat Server and place it in the web view. Then, start a render.
function get_render_client(connection: thrift.Connection) {
    // Get a client if needed.
    if (thrift_client === undefined) {
        thrift_client = thrift.createClient(EditorPlugin, connection);
    }
    // Get a render client if needed.
    if (codechat_client_id === undefined) {
        console.log("CodeChat extension: requesting a render client.");
        thrift_client.get_client(
            codechat_client_location,
            function (err, render_client_return) {
                if (err !== null) {
                    show_error(
                        `Communication error getting render client: ${err}`
                    );
                    stop_client();
                } else if (render_client_return.error === "") {
                    // For a browser location, the panel shouldn't exist and the HTML should be empty. Otherwise, assign the HTML to the panel.
                    if (webview_panel === undefined) {
                        assert(
                            codechat_client_location ===
                                ttypes.CodeChatClientLocation.browser
                        );
                        assert(render_client_return.html === "");
                    } else {
                        webview_panel.webview.html = render_client_return.html;
                    }

                    // Save the ID just provided.
                    assert(codechat_client_id === undefined);
                    codechat_client_id = render_client_return.id;

                    // Do an initial render.
                    start_render();
                } else {
                    show_error(
                        `Error getting render client: ${render_client_return.error}`
                    );
                    stop_client();
                }
            }
        );
    } else {
        // If the render client already exists, simply perform a render.
        console.log("CodeChat extension: client already exists.");
        start_render();
    }
}

// This is called after an event such as an edit, or when the CodeChat panel becomes visible. Wait a bit in case any other events occur, then request a render.
function start_render() {
    if (can_render()) {
        // Render after some inactivity: cancel any existing timer, then ...
        if (idle_timer !== undefined) {
            clearTimeout(idle_timer);
        }
        // ... schedule a render after 300 ms.
        idle_timer = setTimeout(() => {
            if (can_render()) {
                console.log("CodeChat extension: starting render.");
                thrift_client!.start_render(
                    vscode.window.activeTextEditor!.document.getText(),
                    vscode.window.activeTextEditor!.document.fileName,
                    codechat_client_id!,
                    vscode.window.activeTextEditor!.document.isDirty,
                    (err, start_render_return) => {
                        if (err !== null) {
                            show_error(
                                `Communication error when rendering: ${err}`
                            );
                        } else if (start_render_return !== "") {
                            show_error(
                                `Error when rendering: ${start_render_return}`
                            );
                        }
                    }
                );
            }
        }, 300);
    }
}

// Gracefully shut down the render client if possible. Shut down the client as well.
function stop_client() {
    console.log("CodeChat extension: stopping client.");
    if (thrift_client !== undefined) {
        assert(thrift_connection !== undefined);
        // Make a local copy to use for calling ``.end()``. If this function is called twice, then ``thift_connection`` will be set to false; if the callback invoked from the first call hasn't fun, then this local copy will still work.
        const local_thrift_connection = thrift_connection;
        assert(codechat_client_id !== undefined);
        thrift_client.stop_client(
            codechat_client_id,
            function (err, stop_client_return) {
                if (err !== null) {
                    show_error(
                        `Communication error when stopping the client: ${err}`
                    );
                } else if (stop_client_return !== "") {
                    show_error(
                        `Error when stopping the client: ${stop_client_return}`
                    );
                }
                // Close the Thrift connection in case the server is shutting down. Ideally, the server would return some sort of "shutting down now" response in ``stop_client_return``, but it's difficult for the server to know this.
                console.log("CodeChat extension: ending Thrift connection.");
                local_thrift_connection.end();
                thrift_connection = undefined;
            }
        );
    } else {
        // See above -- assume the server will soon shut down.
        thrift_connection?.end();
        thrift_connection = undefined;
    }

    // Even though the callbacks to ``stop_client`` haven't completed yet, set this now to prevent further use of the client, which is stopping.
    thrift_client = undefined;
    codechat_client_id = undefined;

    // Shut the timer down after the client is undefined, to ensure it can't be started again by a call to ``start_render()``.
    if (idle_timer !== undefined) {
        clearTimeout(idle_timer);
        idle_timer = undefined;
    }
}

// Supporting functions
// ====================
// Provide an error message in the panel if possible.
function show_error(message: string) {
    if (webview_panel !== undefined) {
        // If the panel was displaying other content, reset it for errors.
        if (!webview_panel.webview.html.startsWith("<h1>CodeChat</h1>")) {
            webview_panel.webview.html = "<h1>CodeChat</h1>";
        }
        webview_panel.webview.html += `<p style="white-space: pre-wrap;">${escape(
            message
        )}</p><p>See the <a href="https://codechat-system.readthedocs.io/en/latest/docs/common_problems.html" target="_blank" rel="noreferrer noopener">docs</a>.</p>`;
    } else {
        vscode.window.showErrorMessage(
            message +
                "\nSee https://codechat-system.readthedocs.io/en/latest/docs/common_problems.html."
        );
    }
}

// Only render if the window and editor are active, we have a valid render client, and the webview is visible.
function can_render(): boolean {
    return (
        vscode.window.activeTextEditor !== undefined &&
        codechat_client_id !== undefined &&
        thrift_client !== undefined &&
        // If rendering in an external browser, the CodeChat panel doesn't need to be visible.
        (codechat_client_location === ttypes.CodeChatClientLocation.browser ||
            (webview_panel !== undefined && webview_panel.visible))
    );
}

async function start_server() {
    // Get the command from the VSCode configuration.
    const codechat_server_command = vscode.workspace
        .getConfiguration("CodeChat.CodeChatServer")
        .get("Command");
    assert(typeof codechat_server_command === "string");

    // Split it into a command and args.
    const [command, ...args] = [
        ...shlex.split(codechat_server_command),
        "start",
    ];
    let stdout = "";
    let stderr = "";

    return new Promise((resolve, reject) => {
        assert(typeof command === "string");
        const server_process = child_process.spawn(command, args);
        server_process.on("error", (err: NodeJS.ErrnoException) => {
            const msg =
                err.code === "ENOENT"
                    ? `Error - cannot find the file ${err.path}`
                    : err;
            reject(new Error(`While starting the CodeChat Server: ${msg}.`));
        });

        server_process.on("exit", (code, signal) => {
            const exit_str = code ? `code ${code}` : `signal ${signal}`;
            if (code === 0) {
                resolve("");
            } else {
                reject(
                    new Error(
                        `${stdout}\n${stderr}\n\nCodeChat Server exited with ${exit_str}.\n`
                    )
                );
            }
        });

        assert(server_process.stdout !== null);
        server_process.stdout.on("data", (chunk) => {
            stdout += chunk.toString();
        });

        assert(server_process.stderr !== null);
        server_process.stderr.on("data", (chunk) => {
            stderr += chunk.toString();
        });
    });
}
