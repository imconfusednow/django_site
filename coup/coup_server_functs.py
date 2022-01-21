#!/usr/bin/env python3
import sqlite3


def set_player_nick(player_id, name):
    con = sqlite3.connect('/home/imconfusednow/cv_project/db.sqlite3')
    con.execute("UPDATE coup_players SET name = ? WHERE id = ?", [player_id, name])