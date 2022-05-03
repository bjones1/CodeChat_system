// ******************************************
// |docname| - Define plugin project services
// ******************************************
// This defines a single plugin component per project. See the `docs <https://plugins.jetbrains.com/docs/intellij/plugin-services.html>`__.
package com.github.bjones1.intellij.codechat.services

import com.github.bjones1.intellij.codechat.gen_java.CodeChatClientLocation
import com.github.bjones1.intellij.codechat.gen_java.EditorPlugin
import com.intellij.notification.NotificationType
import com.intellij.openapi.project.Project
import com.intellij.openapi.components.Service
import com.intellij.openapi.components.service
import com.intellij.openapi.Disposable
import org.apache.thrift.TException

@Service
class ProjectService(
    // The project for this service instance.
    private val project: Project
) : Disposable {

    // The ID for this project's CodeChat Client.
    private var codeChatClientId: Int? = null

    fun hasCodeChatClientId(): Boolean {
        return codeChatClientId != null
    }

    // Convenience access to the EditorClient.
    fun getEditorPluginClient(): EditorPlugin.Client? {
        return service<ApplicationService>().client
    }

    // This gets a CodeChat Client ID for this project; it also starts the CodeChat Server if necessary.
    fun get_client() {
        // Start then connect to the CodeChat Server if necessary.
        val applicationService = service<ApplicationService>()
        if (getEditorPluginClient() == null) {
            if (!applicationService.openClient(project)) {
                // If the open fails, give up.
                return
            }
        }

        // Get an ID.
        assert(codeChatClientId == null)
        val r = try {
            getEditorPluginClient()?.get_client(CodeChatClientLocation.browser) ?: throw TException()
        } catch (e: TException) {
            notify(project, "Error invoking get_client: ${e.localizedMessage}.")
            // Assume this means the transport is broken. Therefore, dispose of it.
            service<ApplicationService>().dispose()
            return
        }
        if (r.error != "") {
            notify(project, "Error in get_client: ${r.error}.")
            return
        }
        // For now, this is true. Later, when we support in-IDE operation, remove this line.
        assert(r.html == "")
        codeChatClientId = r.id
    }

    // Like ``stop_client``, this performs whatever shutdown of this class is possible given its current state.
    override fun dispose() {
        val ec = getEditorPluginClient()
        if (codeChatClientId != null && ec != null) {
            // When reporting errors, don't return -- we need to shut down the rest of the class first.
            val err = try {
                ec.stop_client(codeChatClientId!!) ?: throw TException()
            } catch (e: TException) {
                notify(project, "Error invoking stop_client: ${e.localizedMessage}.")
                // Assume the transport is broken, so shut it down.
                service<ApplicationService>().dispose()
                ""
            }
            if (err != "") {
                notify(project, "Error in stop_client: $err.")
            }
        }
        codeChatClientId = null
        // TODO: Close in-IDE browser.
    }
}
