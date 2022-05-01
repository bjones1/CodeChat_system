// **********************************************
// |docname| - Define plugin application services
// **********************************************
// This defines an application-wide service for this plugin. See the `docs <https://plugins.jetbrains.com/docs/intellij/plugin-services.html>`__. It provides access to ``client``, the Thrift client, starting the CodeChat Server and opening a Thrift network connection as needed; it also disposes of ``client`` on shutdown.
package com.github.bjones1.intellij.codechat.services

import com.github.bjones1.intellij.codechat.MyBundle
import com.github.bjones1.intellij.codechat.gen_java.CodeChat_ServicesConstants
import com.github.bjones1.intellij.codechat.gen_java.EditorPlugin
import com.intellij.ide.util.PropertiesComponent
import com.intellij.notification.Notification
import com.intellij.notification.NotificationType
import com.intellij.notification.Notifications
import com.intellij.openapi.Disposable
import com.intellij.openapi.components.Service
import com.intellij.openapi.project.Project
import org.apache.thrift.protocol.TBinaryProtocol
import org.apache.thrift.protocol.TProtocol
import org.apache.thrift.transport.TSocket
import org.jetbrains.annotations.NonNls
import java.io.BufferedReader
import java.io.IOException
import java.io.InputStreamReader


// The name of the persistence key where the ``codeChatServerExecutable`` is stored.
@NonNls
private const val CODECHAT_SERVER_EXECUTABLE_KEY = "com.github.bjones1.intellij.codechat.CodeChatBinaryPath"

@Service
class ApplicationService: Disposable {
    // The Thrift network connection to the CodeChat Server.
    private var transport: TSocket? = null

    // The Thrift client to invoke functions on the CodeChat Server.
    private var client: EditorPlugin.Client? = null

    // Create or get the current client.
    fun getClient(currentProject: Project): EditorPlugin.Client? {
            // If the Thrift transport isn't running, start it. TODO: receive some sort of callback when an error occurs, when the connection is closed, etc.
            if (transport == null) {
                // An empty executable indicates that the server should already be running.
                if (codeChatServerExecutable != "") {
                    // Otherwise, start the server, in case it's not running. First, tell the user what's happening with a `Notification <https://plugins.jetbrains.com/docs/intellij/notifications.html#top-level-notifications-balloons>`_.
                    val n = Notification("CodeChat", "Starting CodeChat Server...", "", NotificationType.INFORMATION)
                    Notifications.Bus.notify(n, currentProject)
                    // Run the server process; report any errors. Is there any nicer way to do a `destructuring declaration <https://kotlinlang.org/docs/destructuring-declarations.html>`_ here?
                    val returnCode: Int
                    val output: String
                    try {
                        val p = runProcess(codeChatServerExecutable, "start")
                        returnCode = p.first
                        output = p.second
                    } catch (e: IOException) {
                        println("${e.localizedMessage}.")
                        return null
                    }
                    if (returnCode != 0) {
                        // See `editor hints <https://plugins.jetbrains.com/docs/intellij/notifications.html#editor-hints>`_ for showing error messages. But, we need the current editor to invoke this...
                        println("CodeChat: running CodeChat Server produced return code $returnCode.\n$output")
                        //HintManager.getInstance().showErrorHint(currentProject."Bang!")
                        return null
                    }
                }

                // Connect to the server. See Thrift's `Java tutorial <https://thrift.apache.org/tutorial/java.html>`_ and the corresponding `tutorial files on GitHub <https://github.com/apache/thrift/tree/master/lib/java>`_.
                transport = TSocket("localhost", CodeChat_ServicesConstants.THRIFT_PORT.toInt())
                transport!!.open()
            }
            if (client == null) {
                val protocol: TProtocol = TBinaryProtocol(transport)
                client = EditorPlugin.Client(protocol)
            }
            return client
        }

    // The path to the CodeChat Server executable.
    var codeChatServerExecutable: String
        get() = PropertiesComponent.getInstance().getValue(CODECHAT_SERVER_EXECUTABLE_KEY, "CodeChat_Server")
        set(value) = PropertiesComponent.getInstance().setValue(CODECHAT_SERVER_EXECUTABLE_KEY, value)

    init {
        println(MyBundle.message("applicationService"))
    }

    override fun dispose() {
        transport?.close()
    }
}


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
        if (numRead == 0) {
            break
        }
        out.append(buffer, 0, numRead)
    }

    return Pair(finished, out.toString())
}
