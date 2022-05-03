// **********************************************
// |docname| - Define plugin application services
// **********************************************
// This defines an application-wide service for this plugin. See the `docs <https://plugins.jetbrains.com/docs/intellij/plugin-services.html>`__. It provides access to ``client``, the Thrift client, starting the CodeChat Server and opening a Thrift network connection as needed; it also disposes of ``client`` on shutdown.
package com.github.bjones1.intellij.codechat.services

import com.github.bjones1.intellij.codechat.gen_java.CodeChat_ServicesConstants
import com.github.bjones1.intellij.codechat.gen_java.EditorPlugin
import com.intellij.ide.util.PropertiesComponent
import com.intellij.notification.Notification
import com.intellij.notification.NotificationType
import com.intellij.notification.Notifications
import com.intellij.openapi.Disposable
import com.intellij.openapi.components.Service
import com.intellij.openapi.components.service
import com.intellij.openapi.project.Project
import com.intellij.openapi.project.ProjectManager
import org.apache.thrift.TException
import org.apache.thrift.protocol.TBinaryProtocol
import org.apache.thrift.protocol.TProtocol
import org.apache.thrift.transport.TSocket
import org.apache.thrift.transport.TTransportException
import org.jetbrains.annotations.NonNls
import java.io.BufferedReader
import java.io.IOException
import java.io.InputStreamReader


// The name of the persistence key where the ``codeChatServerExecutable`` is stored.
@NonNls
private const val CODECHAT_SERVER_EXECUTABLE_KEY = "com.github.bjones1.intellij.codechat.CodeChatBinaryPath"


// Display CodeChat notifications.
fun notify(currentProject: Project, title: String, notificationType: NotificationType = NotificationType.ERROR) {
    // Use a `Notification <https://plugins.jetbrains.com/docs/intellij/notifications.html#top-level-notifications-balloons>`_.
    val n = Notification("CodeChat", title, "", notificationType)
    Notifications.Bus.notify(n, currentProject)
}

@Service
class ApplicationService: Disposable {
    // The Thrift network connection to the CodeChat Server.
    private var transport: TSocket? = null

    // The Thrift client to invoke functions on the CodeChat Server.
    var client: EditorPlugin.Client? = null
        private set

    // Open a connection to the CodeChat Server. Re-use any running pieces of that connection (a running transport or already open connection).
    fun openClient(currentProject: Project): Boolean {
            // If the Thrift transport isn't running, start it and the CodeChat Server.
            if (transport == null) {
                // An empty executable indicates that the server should already be running; otherwise, start the server.
                if (codeChatServerExecutable != "") {
                    // Otherwise, start the server, in case it's not running. First, tell the user what's happening with a
                    notify(currentProject, "Starting CodeChat Server...", NotificationType.INFORMATION)
                    // Run the server process; report any errors.
                    val (returnCode, output) = try {
                        //@NonNls
                        runProcess(codeChatServerExecutable, "start")
                    } catch (e: IOException) {
                        notify(currentProject, "Error trying to run the CodeChat Server: ${e.localizedMessage}.", NotificationType.ERROR)
                        return false
                    }
                    if (returnCode != 0) {
                        notify(currentProject, "Error: running the CodeChat Server produced return code $returnCode.\n$output")
                        return false
                    }
                }

                // Connect to the server. See Thrift's `Java tutorial <https://thrift.apache.org/tutorial/java.html>`_ and the corresponding `tutorial files on GitHub <https://github.com/apache/thrift/tree/master/lib/java>`_.
                try {
                    @NonNls
                    transport = TSocket("localhost", CodeChat_ServicesConstants.THRIFT_PORT.toInt())
                    transport!!.open()
                } catch (e: TTransportException) {
                    notify(currentProject, "Error connecting to the CodeChat Server: ${e.localizedMessage}.")
                    return false
                }
            }

            // Code to the CodeChat Services provided by the CodeChat Server.
            if (client == null) {
                try {
                    val protocol: TProtocol = TBinaryProtocol(transport)
                    client = EditorPlugin.Client(protocol)
                } catch (e: TException) {
                    notify(currentProject, "Error connecting to the CodeChat Service: ${e.localizedMessage}.")
                }
            }
            return true
        }

    // The path to the CodeChat Server executable; it's stored using IntelliJ's `persistance <https://plugins.jetbrains.com/docs/intellij/persisting-state-of-components.html#using-propertiescomponent-for-simple-non-roamable-persistence>`_ API.
    var codeChatServerExecutable: String
        get() = PropertiesComponent.getInstance().getValue(CODECHAT_SERVER_EXECUTABLE_KEY, "CodeChat_Server")
        set(value) = PropertiesComponent.getInstance().setValue(CODECHAT_SERVER_EXECUTABLE_KEY, value)

    override fun dispose() {
        // The server will close itself after the transport closes.
        transport?.close()
        transport = null
        client = null
        // Ensure all project services are disposed -- this clears all client IDs, which only had meaning when the client was running.
        for (p in ProjectManager.getInstance().openProjects) {
            p.service<ProjectService>().dispose()
        }
    }
}

// Run a process, waiting for it complete. Return the process's return code and all stderr/stdout produced.
@Throws(IOException::class)
fun runProcess(
    // THe command to run, along with any arguments.
    vararg command: String
    // The process's exit code and stdout/stderr
): Pair<Int, String> {
    // Run the process to completion, capturing the return code. Based on `SO <https://stackoverflow.com/a/57949752/16038919>`__.
    val pb = ProcessBuilder(*command).redirectErrorStream(true)
    val process = pb.start()
    val finished = process.waitFor()

    // Read the stdout/stderr.
    val br = BufferedReader(InputStreamReader(process.inputStream))
    val buffer = CharArray(1024)
    var numRead: Int
    val out = StringBuilder()
    while (true) {
        numRead = br.read(buffer, 0, buffer.size)
        if (numRead < 1) {
            break
        }
        out.append(buffer, 0, numRead)
    }

    return Pair(finished, out.toString())
}
