#!/usr/bin/env python3
import sqlite3
import random
import string
import datetime

con = sqlite3.connect('/home/imconfusednow/cv_project/db.sqlite3')
names = ["David", "John", "Michael", "Jane", "Emily", "Mohammed", "Mary", "Shopie", "Olivia",
         "Ivy", "Rosie", "Isobel", "Charles", "Sadiq", "Noah", "George", "Alex", "Tim", "Isla"]


def set_player_nick(player_id, sid, name):
    run_statement("UPDATE coup_players SET name = ?, player_id = ? WHERE id = ?", [
                  name, sid, player_id])


def get_players(sid):
    room = sid_to_room(sid)
    where = "SELECT * FROM coup_players WHERE player_id != '' AND game_id_id = ?"
    params = [room]
    players = run_query(where, params)
    player = ""
    for i in players:
        if i["player_id"] == sid:
            player = i
    for i in range(4 - len(players)):
        players.append({"id": "t" + str(i), "name": "???", "coins": 0,
                        "game_id_id": room, "hand": "", "player_id": "temp", "turn": 0})
    return [players, player]


def sid_to_room(sid):
    players = run_query(
        "SELECT game_id_id FROM coup_players WHERE player_id = ?", [sid])
    return players[0]["game_id_id"]


def deal(players):
    for p in players:
        p["hand"] = assign_cards(2, p["player_id"], p["game_id_id"])
    run_statement("UPDATE coup_games SET started = 1 WHERE id = ?", [
                  players[0]["game_id_id"]])


def assign_cards(num, player_id, game_id):
    cards = run_query(
        "SELECT card_type FROM coup_decks WHERE game_id_id = ? ORDER BY id ASC LIMIT ?", [game_id, num])
    types = f"{cards[0]['card_type']},{cards[1]['card_type']}"
    run_statement("UPDATE coup_players SET hand = ? WHERE player_id = ?", [
                  types, player_id])
    run_statement(
        "DELETE FROM coup_decks WHERE game_id_id = ? ORDER BY id ASC LIMIT ?", [game_id, num])
    return types


def discard_cards(num, player):
    pass


def pick_starter(sid):
    room = sid_to_room(sid)
    where = "SELECT * FROM coup_players WHERE player_id != '' AND game_id_id = ?"
    params = [room]
    players = run_query(where, params)
    for i in range(4 - len(players)):
        player_id = get_random_string(8)
        run_statement("INSERT INTO coup_players (game_id_id, computer, coins, hand, turn, name, player_id) VALUES(?,?,?,?,?,?,?)", [
                      room, 1, 0, '', 0, 'AI ' + random.choice(names), player_id])
    players = run_query(where, params)
    picked = random.choice(players)
    run_statement("UPDATE coup_players SET turn = ? WHERE id != ?", [
                  0, picked["id"]])
    run_statement("UPDATE coup_players SET turn = ? WHERE id = ?", [
                  1, picked["id"]])

    players = run_query(where, params)
    return players, picked


def do_action(sid, action_type, blocked):
    if not blocked:
        if action_type == "take-1":
            take_one(sid)
        elif action_type == "foreign-aid":
            foreign_aid(sid)
        elif action_type == "take-3":
            take_three(sid)
        elif action_type == "assassinate":
            assassinate(sid)
        elif action_type == "swap":
            swap_cards(sid)
        elif action_type == "steal":
            steal(sid, sid)

    next_player = next_turn(sid)
    return next_player

def challenge(sid):
    room = sid_to_room(sid)
    run_statement("UPDATE coup_players SET challenged_by = ? WHERE turn = '1' AND game_id_id = ?", [sid, room])

def check_challenged(sid, action_type):
    cnb = run_query("SELECT challenged_by, blocked_by, hand FROM coup_players WHERE player_id = ?", [sid], True)
    if cnb["challenged_by"]:        
        challenger = run_query("SELECT name FROM coup_players WHERE player_id = ?", [cnb["challenged_by"]], True)
    hand = cnb["hand"].split(",")

    has_card = True if action_type in hand else False
    return cnb["challenged_by"], cnb["blocked_by"], has_card, challenger["name"]

def next_turn(sid):
    room = sid_to_room(sid)
    players = run_query(
        "SELECT * FROM coup_players WHERE (player_id != '' OR computer = 1) AND game_id_id = ?", [room])
    curr_player = next_player = 0
    for i, p in enumerate(players):
        if p["player_id"] == sid:
            curr_player = i

    if curr_player < len(players) - 1:
        next_player = curr_player + 1
    else:
        next_player = 0
    run_statement(
        "UPDATE coup_players SET turn = 0, challenged_by = '', blocked_by = '' WHERE player_id == ?", [sid])
    run_statement("UPDATE coup_players SET turn = 1 WHERE id == ?", [

                  players[next_player]["id"]])
    return players[next_player]


def take_one(sid):
    run_statement(
        "UPDATE coup_players SET coins = coins + 1 WHERE player_id == ?", [sid])


def foreign_aid(sid):
    run_statement(
        "UPDATE coup_players SET coins = coins + 2 WHERE player_id == ?", [sid])


def take_three(sid):
    run_statement(
        "UPDATE coup_players SET coins = coins + 3 WHERE player_id == ?", [sid])


def assassinate(sid):
    run_statement(
        "UPDATE coup_players SET hand = ? WHERE player_id == ?", ["am", sid])


def swap_cards(sid):
    pass


def steal(sid1, sid2):
    run_statement(
        "UPDATE coup_players SET coins = coins + 2 WHERE player_id == ?", [sid1])
    run_statement(
        "UPDATE coup_players SET coins = coins - 2 WHERE player_id == ?", [sid2])


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def run_statement(query, params):
    try:
        log(query + str(params))
        con.execute(query, params)
        con.commit()
    except Exception as e:
        print(e)


def run_query(query, params, only_one=False):
    return_value = []
    try:
        log(query + str(params))
        con.row_factory = sqlite3.Row
        rows = list(con.execute(query, params).fetchall())
        for r in rows:
            return_value.append(dict(r))
        if only_one:
            return_value = return_value[0]
    except Exception as e:
        print(e)

    return return_value


def log(msg, wipe=False):
    write_type = "w" if wipe else "a"
    file = open("/home/imconfusednow/log.log", write_type)
    time = str(datetime.datetime.now())
    file.write(f"[{time}] - {msg} \n")
    file.close()
