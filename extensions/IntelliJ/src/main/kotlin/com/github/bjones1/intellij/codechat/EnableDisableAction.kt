// ************************************************
// |docname| - An action to enable/disable CodeChat
// ************************************************
package com.github.bjones1.intellij.codechat

import com.github.bjones1.intellij.codechat.services.ProjectService
import com.intellij.openapi.actionSystem.AnAction
import com.intellij.openapi.actionSystem.AnActionEvent
import com.intellij.openapi.actionSystem.CommonDataKeys
import com.intellij.openapi.components.service
import org.jetbrains.annotations.NotNull

// Create a project-wide menu item (an `action <https://plugins.jetbrains.com/docs/intellij/plugin-actions.html>`_) named "Enable/disable CodeChat".
class EnableDisableAction: AnAction() {
    // Update CodeCat's menu text (enable vs. disable) depending on if the client is available.
    override fun update(@NotNull event: AnActionEvent) {
        val project = event.dataContext.getData(CommonDataKeys.PROJECT)
        val projectService = project?.service<ProjectService>()
        // TODO: deal with trying to disable the plugin while the server is still starting (threading problems).
        event.presentation.text = if (projectService?.hasCodeChatClientId() == true) "Close CodeChat" else "Open CodeChat"
        event.presentation.isEnabled = project != null
    }

    // Start a CodeChat client for the current project.
    override fun actionPerformed(e: AnActionEvent) {
        val project = e.project
            ?:
            // This shouldn't happen, since the action is disabled if there's no project. TODO: display an error, or just ignore?
            return

        val projectService = project.service<ProjectService>()
        if (projectService.hasCodeChatClientId()) {
            projectService.dispose()
        } else {
            projectService.get_client()
        }
    }
}