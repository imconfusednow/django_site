const socket = io("http://81.110.114.52:3000");

socket.on('connect', () => {
    console.log('connected');
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
    game_id_input.style = "Display:block";
    var create_game_button = document.getElementById("create-game-button");
    create_game_button.style = "Display:none";

    if ( game_id_input.value == "" ) return;

    button.form.submitted = button;

}

function createGame()
{
    return;
}

function handleSubmit(event,button)
{
    event.preventDefault();
}