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
    localStorage.setItem("player_id", document.getElementById("player_id").value);
});

socket.on('disconnect', () => {
    console.log('disconnected');
});


socket.on('start_game', (data) => {
    console.log(data);
    let players = data[0];
    let hands = data[1];
    let ind = getOnTurn(players);  
    selectStarter(ind, data);    
});

socket.on('join_game', (data) => {
    console.log(data);
    let players = data[0];
    let hands = data[1];
    setPlayerDetails(players[0], hands[0]);
    setOpponentDetails(players.slice(1), hands.slice(1));
});

socket.on('rejoin_game', (data) => {
    console.log(data);
    let players = data[0];
    let hands = data[1];
    let c_grid = document.getElementById("center-grid");
    c_grid.innerText = "";
    setPlayerDetails(players[0], hands[0]);
    setOpponentDetails(players.slice(1), hands.slice(1));
});

socket.on('get_card_swap', (data) => {
    console.log(data);    
    showCardModal(data);
});


socket.on('report_action', (data) => {
    console.log(data);
    let text = data.player + " performed action " + data.action_type;
    let visible_time = 2000;
    let truth = "true";

    if (data.player === "You")
    {
        text = "Waiting for challenges";
    }
    let buttons = [];
    if (data.allow_challenge)
    {
        buttons.push({"text":"Challenge", "function": sendChallenge});
        visible_time = 8000;
    }
    if (data.allow_block)
    {
        buttons.push({"text":"Block", "function": sendBlock});
        visible_time = 8000;
    }
    showModal(text, buttons, visible_time, truth, false);

});

socket.on('report_challenge', (data) => {
    console.log(data);
    let text = data.player + " challenged action " + data.action_type;
    let visible_time = 3000;

    if (data.player === "You")
    {
        text = "You challenged";
    }

    showModal(text, [], visible_time, "", false);
    setTimeout(function() {flipCard(data); }, visible_time);

});

socket.on('report_block', (data) => {
    console.log(data);
    let text = data.player + " blocked action";
    let visible_time = 8000;

    let buttons = [];

    if (data.player === "You")
    {
        text = "You blocked waiting on challenges";
    }
    else
    {
        buttons.push({"text":"Challenge", "function": sendChallenge});
    }

    showModal(text, buttons, visible_time, "", false);
});

socket.on('lose', (data) => {
    console.log(data);
    let text = "You have been eliminated from the game"
    let visible_time = 3000;

    showModal(text, [], visible_time, "", false);
    setTimeout(function() {flipCard(data); }, visible_time);

});

function showModal(text, buttons, visible_time, truth, vertical)
{
    let modal = document.querySelector("#action-overlay");
    modal.style.display = "block";
    let modal_text = document.querySelector("#action-modal-text");
    modal_text.innerText = text;
    let modal_btn_div = document.querySelector("#action-modal-btn-div");
    modal_btn_div.innerText = "";

    buttons.forEach((element) =>{
        let button = document.createElement('button');
        modal_btn_div.appendChild(button);
        button.innerText = element.text;
        button.classList.add("action-modal-btn");
        button.classList.add("action-modal-btn-" + truth);
        button.classList.add("option-button");
        button.addEventListener("click", element.function);
    });
    if (visible_time !== "infinite")
    {
        setTimeout(closeModal, visible_time);
    }
}

function showCardModal(cards)
{
    let modal = document.querySelector("#action-overlay");
    modal.style.display = "block";
    let modal_text = document.querySelector("#action-modal-text");
    modal_text.innerText = "Choose 2 Cards to keep";
    let modal_btn_div = document.querySelector("#action-modal-btn-div");
    modal_btn_div.innerText = "";

    let div1 = document.createElement("div");
    div1.classList.add("modal-card-div");
    div1.id = "modal-card-div";
    modal_btn_div.appendChild(div1);

    let count = 0;

    cards.forEach((element) =>{
        let img = document.createElement('img');
        let thisID = element.card_type + "-" + count;
        img.id = thisID;
        img.src = "/static/coup/" + cardTypes[element.card_type].image;
        img.draggable = false;
        div1.appendChild(img);
        img.classList.add("player-card");
        img.classList.add("modal-card");
        let selectFunct = (e) => {            
            selectCard(thisID);
        }
        img.addEventListener("click", selectFunct);
        count ++;
    });

    let div2 = document.createElement("div");
    div2.classList.add("modal-btn-div");
    div2.id = "modal-btn-div";
    modal_btn_div.appendChild(div2);

    let button = document.createElement('button');
    div2.appendChild(button);
    button.innerText = "Swap";
    button.classList.add("action-modal-btn");
    button.classList.add("action-modal-btn-truth");
    button.classList.add("option-button");
    button.addEventListener("click", doSwap);
}

function doSwap()
{
    let childs = document.querySelector("#modal-card-div").childNodes;

    let cards = {};

    childs.forEach((element) =>{
        cards[element.id] = "";
        if (element.classList.contains("selected-card"))
        {
            cards[element.id] = "selected";
        }
    });

    doAction("swap", false, "", cards);

}

function selectCard(thisID)
{
    let card = document.querySelector("#" + thisID);
    if (card.classList.contains("selected-card"))
    {
        card.classList.remove("selected-card");
        return;
    }

    let selected = document.querySelectorAll(".selected-card").length;
    
    if (selected >= 2){return;}     

    card.classList.toggle("selected-card");
}

function closeModal(e)
{
    if ((e) && (e.target !== e.currentTarget)){return;}
    let modal = document.querySelector("#action-overlay");
    modal.style.display = "none";
}

function flipCard(data)
{
    let cardBack = document.querySelector("#opponent" + data.player_num + "-card-" + data.card_num);
    let cardFront = cardBack.cloneNode();
    cardFront.id = "animated-card-front";
    cardFront.src = "/static/coup/" + cardTypes[data.action_type].image;
    cardFront.style.position = "absolute";
    cardFront.style.transform = "rotateY(180deg)";
    cardFront.style.backfaceVisibility = "hidden";    
    cardBack.parentElement.appendChild(cardFront);
    cardFront.style.animation = "flip_to_front 2s ease 0s 1 normal forwards";
    cardBack.style.animation = "flip_to_back 2s ease 0s 1 normal forwards";
}

function sendStart()
{
    socket.emit('start_game');
}

function sendGetSwap()
{
    socket.emit('get_card_swap');
}

function sendChallenge()
{
    socket.emit("challenge");
}

function sendBlock()
{
    socket.emit("block");
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
    let finish = ind * 90;
    let rand = Math.random() * 20 - 10;
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
    let data = event.currentTarget.data;
    let players = data[0];
    let hands = data[1];
    setPlayerDetails(players[0], hands[0]);
    setOpponentDetails(players.slice(1), hands.slice(1));
    let cards = document.querySelectorAll(".player-card-div");
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
    let cards = document.querySelectorAll(".player-card-div");
    cards.forEach(element => element.classList.remove("hidden"));
    cards = document.querySelectorAll(".opponent-card-div");
    cards.forEach(element => element.classList.remove("hidden"));
    socket.emit("rejoin_game", {"nick": name, "player_id": player_id});
}


function setPlayerDetails(player, hand)
{
    let cards = hand.split(",");
    if (cards[0])
    {
        document.querySelector("#player-card-1").src = "/static/coup/" + cardTypes[cards[0]].image;
        document.querySelector("#player-card-1").classList.remove("hidden");
    }
    else
    {
        document.querySelector("#player-card-1").classList.add("hidden");
    }
    if (cards[1])
    {
        document.querySelector("#player-card-2").src = "/static/coup/" + cardTypes[cards[1]].image;
        document.querySelector("#player-card-2").classList.remove("hidden");
    }
    else
    {
        document.querySelector("#player-card-2").classList.add("hidden");
    }        
    
    if (player.turn)
    {
        document.getElementById('player-info').classList.add("on-turn");        
        let options = document.querySelectorAll(".turn-options");
        let buttons =  document.querySelectorAll(".option-button");
        options.forEach(element => {
                element.classList.remove("hidden");
            });
        buttons.forEach(element => {
                element.classList.remove("hidden");
                if (element.id == "coup-action")
                    {
                        return;
                    }
                if ((cards[0] && cardTypes[cards[0]].actions[element.id]) || (cards[1] && cardTypes[cards[1]].actions[element.id]) || defaultActions[element.id])
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
        let options = document.querySelectorAll(".turn-options");
        options.forEach(element => {
                element.classList.add("hidden");
            }
        );
    }
    if (player.coins >= 7)
    {
        let coup_button = document.querySelector("#coup-action");
        coup_button.disabled = false;
        coup_button.classList.remove("button-inactive");
        coup_button.classList.add("button-active");
    }
    else
    {
        let coup_button = document.querySelector("#coup-action");
        coup_button.disabled = true;
        coup_button.classList.add("button-inactive");
        coup_button.classList.remove("button-active");
    }
    if (player.coins >= 3)
    {
        let assassin_button = document.querySelector("#assassinate");
        assassin_button.disabled = false;
        assassin_button.classList.remove("button-inactive");
    }
    else
    {
        let assassin_button = document.querySelector("#assassinate");
        assassin_button.disabled = true;
        assassin_button.classList.add("button-inactive");
    }
    document.querySelector("#player-money").innerText = "Coins: " + player.coins;
    document.querySelector("#player-info").sequence = player.sequence;
}

function setOpponentDetails(players, hands)
{
    for (let i = 0; i < players.length; i++) {
        let player = players[i];
        let hand = hands[i];
        let cards = document.querySelectorAll(".opponent" + i + "-card");
        for (let c = cards.length - 1; c > - 1; c--) {
            if (c < hand)
            {
                cards[c].classList.remove("hidden");
            }
            else
            {
                cards[c].classList.add("hidden");
            }
        }
        let opponent_name = document.querySelector("#opponent" + i + "-name");
        opponent_name.innerText =  player.name;
        if (player.alive)
        {
            opponent_name.classList.add("opponent-alive");
        }
        {
            opponent_name.classList.add("opponent-remove");
        }
        document.querySelector("#opponent" + i + "-money").innerText = "Coins: " + player.coins;
        document.querySelector("#opponent" + i + "-info").sequence = player.sequence;
        if (player.turn)
        {
            document.querySelector("#opponent" + i + "-info").classList.add("on-turn");
        }
        else
        {
            document.querySelector("#opponent" + i + "-info").classList.remove("on-turn");
        }
    }
}

function getOnTurn(data)
{
    let ind = 0;
    for (let i = 0; i < data.length; i++) {
        let player = data[i];
        if (player.turn)
        {
            ind = i;
        }
    }
    return ind;
}

function doAction(event_type, need_pick, pick, cards)
{
    closeModal();
    if (need_pick)
    {
        pickPlayer(event_type);
    }
    else
    {
        socket.emit('do_action', {"event_type": event_type, "player": pick, "cards": cards});
    }
}

function pickPlayer(event_type)
{
    let buttons = [];
    let names = document.querySelectorAll(".opponent-alive");
    names.forEach((element) =>{
        let dact = () => {
            doAction(event_type, false, element.innerText);
        }
        buttons.push({"text":element.innerText, "function": dact});
    });
    showModal("Choose Target", buttons, "infinite", "lie", true);
}