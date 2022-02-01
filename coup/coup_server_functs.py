#!/usr/bin/env python3
import sqlite3
import random

def set_player_nick(player_id, name):
    run_statement("UPDATE coup_players SET name = ? WHERE id = ?", [name, player_id])

def pick_player():
    players = run_query("SELECT * FROM coup_players", [])
    picked = random.choice(players)
    run_statement("UPDATE coup_players SET turn = ? WHERE id = ?", [1, picked["id"]])
    players = run_query("SELECT * FROM coup_players", [])
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
    rows = []
    try:
        con = sqlite3.connect('/home/imconfusednow/cv_project/db.sqlite3')
        con.row_factory = sqlite3.Row
        rows = list(con.execute(query, params).fetchall())
    except Exception as e:
        print(e)

    return rows