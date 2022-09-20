const setCommandsTextareaPlacholder = () => {
    $('.commands-textarea').attr("placeholder", "e.g.\n$ git init\n$ git add\n$ git commit -m 'First commit'\n$ git remote add origin <github_address>\n$ git branch -m main\n$ git push origin main");
}

const setCommandsTextareaValue = () => {
    let value = ""
    $('.commands-textarea').click(function() {
        if ($('.commands-textarea').val() === '') {
            value = '$ '
            $('.commands-textarea').val(value);
        }
    })
    $('.commands-textarea').keyup(function(e) {
        value = $('.commands-textarea').val();
        if (e.keyCode === 13) {
            value = value + "$ ";
        }
        $('.commands-textarea').val(value);
    })
}

const init = () => {
    setCommandsTextareaPlacholder();
    setCommandsTextareaValue();
}

init();