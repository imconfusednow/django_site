function joinGame(button)
{
    var game_id_input = document.getElementById("game-id");

    if ( game_id_input.value == "" )
    {
        if (game_id_input.getAttribute("visible"))
        {
            game_id_input.setAttribute("required", "");
        }
        else
        {
            game_id_input.setAttribute("visible", "true");
            game_id_input.style = "Display:block";
        }
        return;
    } 

    button.form.submit();

}

function createGame(button)
{
    button.form.submit();
}

function handleSubmit()
{
    event.preventDefault();
}