***********************
Developer documentation
***********************
This plugin was created following the `IntelliJ docs <https://plugins.jetbrains.com/docs/intellij/getting-started.html>`_ using their `GitHub template <https://plugins.jetbrains.com/docs/intellij/github-template.html>`_.

Architecture
============
-   An `application-wide service <src/main/kotlin/com/github/bjones1/intellij/codechat/services/ApplicationService.kt>` stores the Thrift transport and client; it starts the CodeChat Server and maintains a network connection to it.
-   A `per-project service <src/main/kotlin/com/github/bjones1/intellij/codechat/services/ProjectService.kt>` requests a CodeChat Client for a project from the application service's Thrift client. It provides methods to interact with the project's CodeChat Client.
-   An `action <src/main/kotlin/com/github/bjones1/intellij/codechat/EnableDisableAction.kt>` provides a menu item to enable/disable CodeChat for the current project.
-   A `setting <src/main/kotlin/com/github/bjones1/intellij/codechat/settings/AppSettingsConfigurable.kt>` and its `associated GUI <src/main/kotlin/com/github/bjones1/intellij/codechat/settings/AppSettingsComponent.kt>` allows the user to specify the path to the CodeChat Server executable.

Error handling
--------------
The Java networking libraries don't provide any listeners / callbacks if the network connection fails or is closed. Therefore, this plugin handles errors which arise from doing network I/O:

-   All CodeChat Services calls (which are RPC) are enclosed in a try/catch block.
-   We assume that any exceptions caused by these calls indicates that the network connection has failed. In this case:

    -   Report this failure to the user.
    -   Shut down the network connection.
    -   Disable CodeChat in all projects.

    Other projects using this network connection don't report the error, to avoid producing repetitive errors.

Plan
====
-   Need to use a `Java Timer <https://docs.oracle.com/en/java/javase/11/docs/api/java.base/java/util/Timer.html>`_ to render at a good time.


Questions:

-   Is there some callback for when the Thrift connection dies?
-   The `Markdown plugin <https://www.jetbrains.com/help/idea/markdown.html>`_ provides a nice split-screen environment. See https://github.com/JetBrains/intellij-community/tree/master/plugins/markdown. How can I use the Markdown plugin's GUI, but none of its parsing/logic. If not, fall back to:

    -   `JCEF - Java Chromium Embedded Framework <https://plugins.jetbrains.com/docs/intellij/jcef.html>`_.
    -   Send updates on edits, possibly using the `DocumentListener <https://upsource.jetbrains.com/idea-ce/file/idea-ce-4d741bc560dd19306d4624d7c8a88aea537f4e6f/platform/core-api/src/com/intellij/openapi/editor/event/DocumentListener.java?_ga=2.242772421.694060030.1650200348-2033576375.1648230492>`_.
    -   Send updates on focus changes (switching to another window). Not sure how -- the mention of focus in `FileEditorMananagerListener <https://upsource.jetbrains.com/idea-ce/file/idea-ce-4d741bc560dd19306d4624d7c8a88aea537f4e6f/platform/analysis-api/src/com/intellij/openapi/fileEditor/FileEditorManagerListener.java?_ga=2.28322171.694060030.1650200348-2033576375.1648230492>`_. Perhaps https://stackoverflow.com/questions/58627450/add-focus-blur-listener-in-intellij-plugin?
    -   See how to open a browser inside IntelliJ.


Notes
=====
To do plugin development, open the `Internal Actions Menu <https://plugins.jetbrains.com/docs/intellij/internal-actions-intro.html>`_.


Source
======
.. toctree::
    :maxdepth: 2

    .gitignore
    build.gradle.kts
    gradle.properties
    src/main/resources/META-INF/plugin.xml
    src/main/kotlin/com/github/bjones1/intellij/codechat/MyBundle.kt
    src/main/kotlin/com/github/bjones1/intellij/codechat/EnableDisableAction.kt
    src/main/kotlin/com/github/bjones1/intellij/codechat/listeners/MyProjectManagerListener.kt
    src/main/kotlin/com/github/bjones1/intellij/codechat/services/ApplicationService.kt
    src/main/kotlin/com/github/bjones1/intellij/codechat/services/ProjectService.kt
    src/main/kotlin/com/github/bjones1/intellij/codechat/settings/AppSettingsConfigurable.kt
    src/main/kotlin/com/github/bjones1/intellij/codechat/settings/AppSettingsComponent.kt
