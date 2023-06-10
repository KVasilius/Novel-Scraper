import db_insert as idb
import database_create as dc
import tkinter_interface as ti
import os


def initial_setup():
    dc.create_database()
    idb.database_scrape('https://www.novelupdates.com/novelslisting/?sort=7&order=1&status=1&pg=1')
    ti.Tkinter()

def normal_run():
    ti.Tkinter()

current_path = os.path.dirname(os.path.abspath(__file__))
database = os.path.join(current_path, "novel_database.db")

if os.path.exists(database):
    normal_run()
else:
    initial_setup()

