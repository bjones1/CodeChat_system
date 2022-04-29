// .. Copyright (C) 2012-2022 Bryan A. Jones.
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
// ************************************
// |docname| - Define CodeChat services
// ************************************
// This file defines a set of CodeChat services provided by the CodeChat Server.
//
// Draft sync interface
// ====================
// Draft of a `Thrift <https://thrift.apache.org/>`_ for synchronizing cursor location between the editor/IDE and the CodeChat Client, and for allowing editing of the document in either location. This requires one interface between the editor/IDE extension and the CodeChat Server and another between the CodeChat Client and the CodeChat Server:
//
// -    Extension service:
//
//      -   ``void sync_to(string text, uint text_index, uint global_y_coordinate_of_cursor)``
//      -   ``uint index, string text, enum result_type { sync, text, request_ownership } = get_results()`` returns:
//
//          -   The index for the next sync request made in the CodeChat Client. Valid if ``result_type == sync``.
//          -   Updated text for the editor. Valid if ``result_type == text``.
//
// -    ``void grant_ownswership(int id)``
//
// -    Web browser service. All methods raise an exception if the id isn't valid.
//
//      -   ``void sync_to(string text, uint text_index, uint global_y_coordinate_of_cursor)``
//      -   ``void request_ownership(int id)`` returns when ownership is granted.
//
// Edits may be made in the text editor or in the CodeChat Client. To prevent users from modifying both at the same time, only one of these two places may have editing priviledges. The text editor begins with this priviledge; the CodeChat Client must request and obtain it from the text editor before allowing edits. Privledges return to the text editor when the CodeChat Client sends updated text. What if the text editor changes to another document while the CodeChat Client is still editing? Probably pop up a modal dialog in the web page: save changes or discard changes.

// .. _editor_services:
//
// Services for the editor/IDE extension
// =====================================
//
// .. _CodeChat service port:
//
// The port used for the Thrift connection between text editor/IDE extensions/plugins and the CodeChat Server. All editor/IDE plugins must use this port to access CodeChat services.
const i16 THRIFT_PORT = 27376

// This defines the return value from ``get_client``.
struct RenderClientReturn {
    // An HTML string which contains either the render client or an URL for the client.
    1: string html,
    // The ID for this client.
    2: i32 id,
    // An empty string on success, or an error message.
    3: string error
}


// Define the location of the CodeChat Client; passed as a parameter to ``get_client``.
enum CodeChatClientLocation {
    // A URL, which the CodeChat System will host in its own web browser.
    url,
    // An HTML string, which the CodeChat System will host in its own web browser.
    html,
    // An external browser, which the CodeChat Server should launch.
    browser
}

// Provide CodeChat services to editor plugins.
service EditorPlugin {
    // See if the server is running. It returns an empty string on success.
    string ping()

    string gotoFile(
        1: i32 id
    )

    // Create a CodeChat Client and return HTML for it and its ID.
    RenderClientReturn get_client(
        // The location of the client to return.
        1: CodeChatClientLocation codeChat_client_location
    )

    // Render the provided text as html. Returns an empty string on success, or an error message.
    string start_render(
        // The source code or text to render.
        1: string text,
        // The path to this source file; may be blank for an unnamed file.
        2: string path,
        // _`id`: The ID of the client to render in.
        3: i32 id,
        // True if the document is dirty (modified), false if clean.
        4: bool is_dirty
    )

    // Release all resources associated with a CodeChat Client. Returns an empty string on success, or an error message.
    string stop_client(
        // See id_.
        1:i32 id
    )
 }
