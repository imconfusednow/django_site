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
    let name = nick_field.value;

    if (!nick_field.value)
    {
        nick_field.style.backgroundColor = "pink";
        return;
    }

    let p_setup = document.getElementById("player-setup");
    let start_but = document.createElement('button')

    p_setup.parentElement.appendChild(start_but);
    p_setup.remove();
    start_but.innerText = "Start Game";
    start_but.classList.add("btn", "btn-success");
    start_but.style.minWidth = "200px";
    start_but.style.minHeight = "50px";

    document.getElementById("player-ready").style.display = "grid";

    document.getElementById("player-name").innerText = name;


}

function myTurn()
{
    
}

function notMyTurn()
{
    
}