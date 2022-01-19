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

function joinGame()
{
    let nick_field = document.getElementById("nick");

    if (!nick_field.value)
    {
        nick_field.style.backgroundColor = "pink";
        return;
    }

    let p_setup = document.getElementById("player-setup");
    p_setup.remove();

    document.getElementById("player-ready").style.display = "grid";
}

function myTurn()
{
    
}

function notMyTurn()
{
    
}