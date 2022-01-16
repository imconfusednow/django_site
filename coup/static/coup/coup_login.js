function joinGame(button)
{
    var room_name = document.getElementById("room-name");
    if (!room_name.value) return;
    var submit_type_input = document.getElementById("submit-type");
    submit_type_input.value = "join";
    button.form.submit();
}

function createGame(button)
{
    var room_name = document.getElementById("room-name");
    if (!room_name.value) return;
    var submit_type_input = document.getElementById("submit-type");
    submit_type_input.value = "create";
    button.form.submit();
}

function handleSubmit()
{
    event.preventDefault();
}