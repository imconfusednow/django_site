function joinGame(button)
{
    var submit_type_input = document.getElementById("submit-type");
    game_id_input.value = "join";
    button.form.submit();
}

function createGame(button)
{
    var submit_type_input = document.getElementById("submit-type");
    game_id_input.value = "create";
    button.form.submit();
}

function handleSubmit()
{
    event.preventDefault();
}