function joinGame(button)
{
    var submit_type_input = document.getElementById("submit-type");
    submit_type_input.value = "join";
    button.form.submit();
}

function createGame(button)
{
    var submit_type_input = document.getElementById("submit-type");
    submit_type_input.value = "create";
    button.form.submit();
}

function handleSubmit()
{
    event.preventDefault();
}