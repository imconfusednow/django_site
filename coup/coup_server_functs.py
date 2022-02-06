#!/usr/bin/env python3
import sqlite3
import random

def set_player_nick(player_id, sid, name):
    run_statement("UPDATE coup_players SET name = ?, player_id = ? WHERE id = ?", [name, sid, player_id])
    players = run_query("SELECT game_id_id FROM coup_players WHERE id = ?",  [player_id])
    return players[0]["game_id_id"]

def get_players(pick):
    players = run_query("SELECT * FROM coup_players", [])
    if pick:
        picked = random.choice(players)
        run_statement("UPDATE coup_players SET turn = ? WHERE id != ?", [0, picked["id"]])
        run_statement("UPDATE coup_players SET turn = ? WHERE id = ?", [1, picked["id"]])
    players = run_query("SELECT * FROM coup_players", [])
    for i in range(4 - len(players)):
        players.append({"id": "t" + str(i), "name": "temp" + str(i), "coins": 0, "game_id_id": "temp", "hand":"", "player_id": "temp", "turn": 0})
    return players


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