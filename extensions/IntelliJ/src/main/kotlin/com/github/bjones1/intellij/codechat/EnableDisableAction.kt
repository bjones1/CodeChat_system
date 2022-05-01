package com.github.bjones1.intellij.codechat

import com.github.bjones1.intellij.codechat.services.ApplicationService
import com.github.bjones1.intellij.codechat.services.ProjectService
import com.intellij.openapi.actionSystem.AnAction
import com.intellij.openapi.actionSystem.AnActionEvent
import com.intellij.openapi.components.service
import org.jetbrains.annotations.NotNull

class EnableDisableAction: AnAction() {
    // Update CodeCat's menu text (enable vs. disable) depending on if the client is available.
    override fun update(@NotNull event: AnActionEvent) {
        val applicationService = service<ApplicationService>()
        event.presentation.text = if (applicationService.isClientAvailable()) "Disable CodeChat" else "Enable CodeChat"
    }

    // Start a CodeChat client for the current project.
    override fun actionPerformed(e: AnActionEvent) {
        val project = e.project
        // TODO: Handle the case where project is null.
        // TODO: Treat as enable/disable.
        val projectService = project!!.service<ProjectService>()
    }
}