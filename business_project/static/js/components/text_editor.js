// Control behavior of special keys in commands editor
const keyControl = () => {
    $('#commands-textarea').keydown(function(e) {
        // Allow using tab to indent when writing commands
        if (e.keyCode === 9) {
            e.preventDefault();
            var start = $(this)[0].selectionStart;
            var end = $(this)[0].selectionEnd;
            // set textarea value to: text before caret + tab + text after caret
            $(this).val($(this).val().substring(0, start) +
            "\t" + $(this).val().substring(end));
            $(this)[0].selectionStart = $(this)[0].selectionEnd = start + 1;
        }
    })
}

// Allow previewing commands in md
const allowCommandsPreview = () => {
    // Initially hide the preview block
    const commandsPreviewBlock = $('.commands-block');
    commandsPreviewBlock.hide();

    $("#commands-preview-btn").click(function(e) {
        // What users currently have for commands
        const commandsTextarea = $("#commands-textarea");
        console.log("Original: " + JSON.stringify(commandsTextarea.val()));
        const commandsText = 
        commandsTextarea.val()
        .replaceAll("\n", "<br/>\n")
        .replaceAll("\t", "&emsp;")
        .replaceAll("  ", "&ensp;")
        .replaceAll("    ", "&emsp;");
        console.log("MD: " + JSON.stringify(commandsText));

        // Switch preview mode to editing mode
        if ($(this).hasClass('showing')) {
            commandsTextarea.show();
            commandsPreviewBlock.empty();
            commandsPreviewBlock.hide();
            $(this).removeClass('showing');
            $(this).text("Preview");
        } else {    // Switch editing mode to preview mode
            commandsPreviewBlock.append(`<md-block>${commandsText}</md-block>`);
            commandsPreviewBlock.show();
            commandsTextarea.hide();
            $(this).addClass('showing');
            $(this).text("Continue editing");
        }
    })
}

const textEditorInit = () => {
    // Control behavior of special keys in commands editor
    keyControl();
    // Allow previewing commands in md
    allowCommandsPreview();
}

textEditorInit();