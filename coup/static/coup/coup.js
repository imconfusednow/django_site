const socket = io("http://81.110.114.52:3000");

socket.on('connect', () => {
    console.log('connected');
    //if (!localStorage.getItem("player_id")) localStorage.setItem("player_id", socket.id)
    //var title = document.getElementById("coup-title");
    //title.innerText = title.innerText + " " + localStorage.getItem("player_id");
});

socket.on('disconnect', () => {
    console.log('disconnected');
});


socket.on('send_result', (data) => {
    document.getElementById("responses").value = document.getElementById("responses").value + "\n" + data['result'];
});


function sendMessage()
{
    let msg = document.getElementById("message").value;
    socket.emit('send_message', {msg: msg});
}


function joinGame(button)
{
    var game_id_input = document.getElementById("game-id");
    var create_game_button = document.getElementById("create-game-button");
    create_game_button.style = "Display:none";

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