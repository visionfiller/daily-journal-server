import sqlite3
import json
from models import Entry, Mood, Entry_Tag, Tag
from .tag_request import get_single_tag

def get_all_entries ():
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
       SELECT DISTINCT
            a.id,
            a.concept,
            a.entry,
            a.mood_id,
            m.label,
           (SELECT GROUP_CONCAT(t.id) 
           FROM Entry_Tags e JOIN Tags t ON e.tag_id = t.id WHERE e.entry_id = a.id ) AS Tags
        
        FROM Journal_Entries a
        JOIN Moods m ON m.id = a.mood_id
        JOIN Entry_Tags e ON a.id = e.entry_id
        JOIN Tags t ON e.tag_id = t.id
        """)

        # Initialize an empty list to hold all animal representations
        entries = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:
            
            entry = Entry(row['id'], row['concept'], row['entry'], row['mood_id'])
            mood = Mood(row['id'], row['label'])
            entry.mood = mood.__dict__
            
            tag_ids = row['tags'].split(",") if row["tags"] else []
            tags = []
            for tag in tag_ids:
                tag_object = get_single_tag(tag)
                tags.append(tag_object)
            entry.tag = tags
            entries.append(entry.__dict__)
    return entries
def get_single_entry(id):
   with sqlite3.connect("./dailyjournal.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            a.id,
            a.concept,
            a.entry,
            a.mood_id,
            m.label
            
        FROM Journal_Entries a
        JOIN Moods m ON m.id = a.mood_id
        WHERE a.id = ?
        """, (id, ))
 
        data = db_cursor.fetchone()

       
        entry = Entry(data['id'], 
                    data['concept'], data['entry'], data['mood_id'])

        mood = Mood(data['id'], data['label'])
        entry.mood = mood.__dict__
          
        return entry.__dict__
def delete_entry(id):
       with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Journal_Entries
        WHERE id = ?
        """, (id, ))
def get_entry_by_word(word):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            a.id,
            a.concept,
            a.entry,
            a.mood_id
        FROM Journal_Entries a
        WHERE a.entry LIKE ?
        """, ( f"%{word}%", ))

        entries = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            entry = Entry(row['id'], row['concept'], row['entry'],
                            row['mood_id'])

            entries.append(entry.__dict__)

    return entries
def create_new_entry(new_entry):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            a.id,
            a.concept,
            a.entry,
            a.mood_id,
            m.label,
            t.id tag_id
        
        FROM Journal_Entries a
        JOIN Moods m ON m.id = a.mood_id
        JOIN Entry_Tags e ON a.id = e.entry_id
        JOIN Tags t ON e.tag_id = t.id
        """)
        db_cursor.execute("""
        INSERT INTO Journal_Entries
            ( concept, entry, mood_id)
        VALUES
            ( ?, ?, ?);
        """, (new_entry['concept'], new_entry['entry'],
              new_entry['mood_id'] ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_entry['id'] = id

        for tag in new_entry['tags']:
             db_cursor.execute("""
            INSERT INTO Entry_Tags
                ( entry_id, tag_id)
             VALUES
                ( ?, ?);
            """, (new_entry['id'], tag,
             ))
   

    return new_entry
def update_entry(id, new_entry):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Journal_Entries
             SET
                concept = ?,
                entry = ?,
                mood_id = ?   
        WHERE id = ?
        """, (new_entry['concept'], new_entry['entry'], new_entry['mood_id'], id, ))
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
            # Forces 404 response by main module
        return False
    else:
            # Forces 204 response by main module
        return True