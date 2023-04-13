import sqlite3
import json
from models import Mood

def get_all_moods ():
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            m.id,
            m.label
        
        FROM 
        Moods m
        """)

        # Initialize an empty list to hold all animal representations
        moods = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            mood = Mood(row['id'], row['label'])
    
            moods.append(mood.__dict__)
    return moods
def get_single_mood(id):
   with sqlite3.connect("./dailyjournal.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            m.id,
            m.label
            
        FROM Moods m
        WHERE m.id = ?
        """, (id, ))
 
        data = db_cursor.fetchone()

       
        mood = Mood(data['id'],data['label'])

        
          
        return mood.__dict__    