const socket = io("http://81.110.114.52:3000");

let cardTypes = 
{
    "co": {"actions": {}, "image": "cortessa.png"},
    "du": {"actions": {"take-3": 1}, "image": "duke.png"},
    "ca": {"actions": {"steal": 1}, "image": "captain.png"},
    "as": {"actions": {"assassinate": 1}, "image": "assassin.png"},
    "am": {"actions": {"swap": 1},  "image": "ambassador.png"},
};

let defaultActions = {"take-1" : 1, "foreign-aid" : 1};

socket.on('connect', () => {
    console.log('connected');
    if (!localStorage.getItem("player_id")) localStorage.setItem("player_id", document.getElementById("player_id").value);
});

socket.on('disconnect', () => {
    console.log('disconnected');
});


socket.on('start_game', (data) => {
    console.log(data);
    var players = data[0];
    var hands = data[1];
    var ind = getOnTurn(players);  
    selectStarter(ind, players);    
});

socket.on('join_game', (data) => {
    console.log(data);
    var players = data[0];
    var hands = data[1];
    setPlayerDetails(players[0]);
    setOpponentDetails(players.slice(1));
});

socket.on('rejoin_game', (data) => {
    console.log(data);
    var players = data[0];
    var hands = data[1];
    let c_grid = document.getElementById("center-grid");
    c_grid.innerText = "";
    setPlayerDetails(players[0]);
    setOpponentDetails(players.slice(1));
});


function sendStart()
{
    socket.emit('start_game');
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
    let start_but = document.createElement('button');

    p_setup.parentElement.appendChild(start_but);
    p_setup.remove();
    start_but.innerText = "Start Game";
    start_but.classList.add("btn", "btn-success");
    start_but.style.minWidth = "200px";
    start_but.style.minHeight = "50px";
    start_but.addEventListener("click", sendStart);

    document.getElementById("player-ready").style.display = "grid";

    document.getElementById("player-name").innerText = name;
    let player_id = localStorage.getItem("player_id");
    socket.emit("join_game", {"nick": name, "player_id": player_id});

}

function selectStarter(ind, data)
{
    var finish = ind * 90;
    var rand = Math.random() * 20 - 10;
    document.documentElement.style.setProperty('--start-spin', 0 + "deg");
    document.documentElement.style.setProperty('--end-spin', (finish + 1890 + rand) + "deg");

    let spinner = document.createElement('span');
    spinner.data = data;
    spinner.addEventListener('animationend', startGame);
    spinner.innerText = "➤";
    spinner.id = "spinner";
    spinner.style.animation = "spin 2s ease 0s 1 normal forwards";
      
    let c_grid = document.getElementById("center-grid");
    c_grid.innerText = "";
    c_grid.appendChild(spinner);
}


function startGame(event)
{
    var data = event.currentTarget.data;
    setPlayerDetails(data[0]);
    setOpponentDetails(data.slice(1));
    var cards = document.querySelectorAll(".player-card-div");
    cards.forEach(element => element.classList.remove("hidden"));
    cards = document.querySelectorAll(".opponent-card-div");
    cards.forEach(element => element.classList.remove("hidden"));    
    document.getElementById('spinner').remove();
}

function sendRejoin(event)
{
    let nick_field = document.getElementById("nick");
    let name = nick_field.value;
    document.getElementById("player-ready").style.display = "grid";
    document.getElementById("player-name").innerText = name;
    let player_id = localStorage.getItem("player_id");
    var cards = document.querySelectorAll(".player-card-div");
    cards.forEach(element => element.classList.remove("hidden"));
    cards = document.querySelectorAll(".opponent-card-div");
    cards.forEach(element => element.classList.remove("hidden"));
    socket.emit("rejoin_game", {"nick": name, "player_id": player_id});
}


function setPlayerDetails(data)
{
    if (data.turn)
    {
        document.getElementById('player-info').classList.add("on-turn");
        var cards = data.hand.split(",");
        document.querySelector("#player-card-1").src = "/static/coup/" + cardTypes[cards[0]].image;
        if (cards[1])
        {
            document.querySelector("#player-card-2").src = "/static/coup/" + cardTypes[cards[1]].image;
        }
        var options = document.querySelectorAll(".turn-options");
        var buttons =  document.querySelectorAll(".option-button");
        options.forEach(element => {
                element.classList.remove("hidden");
            });
        buttons.forEach(element => {
                element.classList.remove("hidden");
                if (element.id == "coup-action")
                    {
                        return;
                    }
                if (cardTypes[cards[0]].actions[element.id] || cardTypes[cards[1]].actions[element.id] || defaultActions[element.id])
                {
                    element.classList.remove("option-button-lie");
                    element.classList.add("option-button-true");
                }
                else
                {
                    element.classList.add("option-button-lie");
                    element.classList.remove("option-button-true");
                
                }
            }
        );
    }
    else
    {
        document.getElementById('player-info').classList.remove("on-turn");
        var options = document.querySelectorAll(".turn-options");
        options.forEach(element => {
                element.classList.add("hidden");
            }
        );
    }
}

function setOpponentDetails(data)
{
    for (var i = 0; i < data.length; i++) {
        var player = data[i];
        document.querySelector("#opponent" + i + "-name").innerText =  player.name;
        document.querySelector("#opponent" + i + "-money").innerText = "Coins: " + player.coins;
        if (player.turn)
        {
            document.querySelector("#opponent" + i + "-info").classList.add("on-turn");
        }
    }
}

function getOnTurn(data)
{
    var ind = 0;
    for (var i = 0; i < data.length; i++) {
        var player = data[i];
        if (player.turn)
        {
            ind = i;
        }
    }
    return ind;
}