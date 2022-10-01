const setCommandsTextareaPlacholder = () => {
    $('#commands-textarea').attr("placeholder", "e.g.\n$ git init\n$ git add\n$ git commit -m 'First commit'\n$ git remote add origin <github_address>\n$ git branch -m main\n$ git push origin main");
}

const init = () => {
    setCommandsTextareaPlacholder();
}

init();