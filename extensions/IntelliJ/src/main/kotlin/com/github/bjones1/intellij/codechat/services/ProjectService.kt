// ******************************************
// |docname| - Define plugin project services
// ******************************************
// This defines a single plugin component per project. See the `docs <https://plugins.jetbrains.com/docs/intellij/plugin-services.html>`__.
package com.github.bjones1.intellij.codechat.services

import com.github.bjones1.intellij.codechat.MyBundle
import com.intellij.openapi.project.Project
import org.apache.thrift.TException
import com.intellij.openapi.components.Service
import com.intellij.openapi.components.service

@Service
class ProjectService(project: Project) {

    // TODO: store a client ID; stop that client in dispose().
    // TODO: provide an enable/disable.

    init {
        println(MyBundle.message("projectService", project.name))

        try {
            val applicationService = service<ApplicationService>()
            applicationService.getClient(project)?.ping()
        } catch (x: TException) {
            x.printStackTrace()
        }
    }
}
