#!/usr/bin/env python3
import sqlite3


def set_player_nick(player_id, name):
    try:
        con = sqlite3.connect('/home/imconfusednow/cv_project/db.sqlite3')
        con.execute("UPDATE coup_players SET name = ? WHERE id = ?", [name, player_id])
        con.commit()
        con.close()
    except Exception as e:
        print(e)