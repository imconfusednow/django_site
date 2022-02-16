#!/usr/bin/env python3
import sqlite3
import random

def set_player_nick(player_id, sid, name):
    run_statement("UPDATE coup_players SET name = ?, player_id = ? WHERE id = ?", [name, sid, player_id])    

def get_players(pick, sid):
    room = sid_to_room(sid)
    where = "SELECT * FROM coup_players WHERE player_id != '' AND game_id_id = ?"
    params = [room]
    players = run_query(where, params)
    if pick:
        picked = random.choice(players)
        run_statement("UPDATE coup_players SET turn = ? WHERE id != ?", [0, picked["id"]])
        run_statement("UPDATE coup_players SET turn = ? WHERE id = ?", [1, picked["id"]])
    players = run_query(where, params)
    for i in range(4 - len(players)):
        players.append({"id": "t" + str(i), "name": "???", "coins": 0, "game_id_id": room, "hand":"", "player_id": "temp", "turn": 0})
    return players


def sid_to_room(sid):
    players = run_query("SELECT game_id_id FROM coup_players WHERE player_id = ?", [sid])
    return players[0]["game_id_id"]


def deal(players):
    for p in players:
        p["hand"] = assign_cards(2, p["player_id"], p["game_id_id"])
    run_statement("UPDATE coup_games SET started = 1 WHERE game_id_id = ?", players[0]["game_id_id"])


def assign_cards(num, player_id, game_id):
    cards = run_query("SELECT card_type FROM coup_decks WHERE game_id_id = ? ORDER BY id ASC LIMIT ?", [game_id, num])
    types = f"{cards[0]['card_type']},{cards[1]['card_type']}"
    run_statement("UPDATE coup_players SET hand = ? WHERE player_id = ?", [types, player_id])
    run_statement("DELETE FROM coup_decks WHERE game_id_id = ? ORDER BY id ASC LIMIT ?", [game_id, num])
    return types

def discard_cards(num, player):
    pass


def run_statement(query, params):
    try:
        con = sqlite3.connect('/home/imconfusednow/cv_project/db.sqlite3')
        con.execute(query, params)
        con.commit()
        con.close()
    except Exception as e:
        print(e)

def run_query(query, params):
    return_value = []
    try:
        con = sqlite3.connect('/home/imconfusednow/cv_project/db.sqlite3')
        con.row_factory = sqlite3.Row
        rows = list(con.execute(query, params).fetchall())
        for r in rows:
            return_value.append(dict(r))
    except Exception as e:
        print(e)

    return return_value


