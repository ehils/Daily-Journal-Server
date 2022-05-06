from curses.ascii import ETB
import sqlite3
import json
from models import Entry, Mood, EntryTag, Tag
def get_all_entries():
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.mood_id,
            e.date,
            t.id tag_id,
            t.tag,
            m.label mood_label
        FROM Entry e  
        JOIN Mood as m
            On m.id = e.mood_id 
        JOIN entrytag as et
            On et.entry_id = e.id   
        JOIN Tag as t
            On t.id = et.tag_id
        ORDER BY e.id   
        """)
        entries = []
        
        dataset = db_cursor.fetchall()
        # establishes entry for first pass
        # initialize and empty instance of entry object
        entry = Entry(0,'','',0,'')
        for row in dataset:
            # not reset the entry if the entry exists, but still add tag onto entry's array
            if row['id'] != entry.id:
                # explicity set tags to a new list in model
                entry = Entry(row['id'], row['concept'], row['entry'], row['mood_id'], row['date'], [])
                mood = Mood(row['id'], row['mood_label'])
                entry.mood = mood.__dict__
                # db_cursor.execute("""
                # SELECT
                #     tag.id,
                #     tag.tag
                # FROM entrytag et
                # JOIN tag t on t.id = et.tag_id
                # WHERE et.entry_id = ?
                # """,(entry.id, ))
                # sub_dataset = db_cursor.fetchall()
                # for sub_row in sub_dataset
                    # tag = Tag(sub_row['id'],sub_row['tag'])
                    # entry.tags.append(tag.__dict__)
        #         entries.append(entry.__dict__)
        # return json.dumps(entries)
            tag = Tag(row['tag_id'],row['tag'])
            entry.tags.append(tag.__dict__)
            # does current row id match next row id,
            # if doesn't, then add entry 
            try:
                if dataset[dataset.index(row)]['id'] != dataset[(dataset.index(row)) +1]['id']:              
                    entries.append(entry.__dict__)
            except:
                entries.append(entry.__dict__)
        return json.dumps(entries)
        # 
        # foreach entry in the loop, perform a SQL execution 
            # get all entry tags for entry ID
            
            # loop through
            # add to list
        # to select the tags associated with that entry
        # set entrytags to an empty array
            # entrytags = []
            # # get the entrytag_id list for each entry
            # # 
            # # SELECT entrytag and tag.tag
            # row['tags']= db_cursor.fetchall()
            # db_cursor.execute("""
            # SELECT
            #     et.id,
            #     et.tag_id,
            #     et.entry_id,
            #     t.tag tag_name
            # FROM entrytag et
            # JOIN Tag as t
            #     On t.id = et.tag_id
            # """)
            # join tag.id on each entrytag.tag_id
            # create instance of entry tag
            # create instance of tag
            # set each entrytag.tag equal to tag.__dict__
            # append tags to entrytags array
        # return list of tags for each entry
        # 
            # entrytags = []
            
            
            
            # for new_row in row['tags']:
            
            #     db_cursor.execute("""
            #     SELECT
            #         et.id,
            #         et.tag_id,
            #         et.entry_id
            #         t.tag tag_tag
            #     FROM entrytag et  
            #     JOIN Tag as t
            #         On t.id = et.tag_id        
            #     """)
            #     tag = Tag(new_row['id'], new_row['tag_tag'])
            #     entrytags.append(tag.__dict__)
def get_single_entry(id):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.mood_id,
            e.date,
            t.id tag_id,
            t.tag,
            m.label mood_label
        FROM Entry e  
        JOIN Mood as m
            On m.id = e.mood_id 
        JOIN entrytag as et
            On et.entry_id = e.id   
        JOIN Tag as t
            On t.id = et.tag_id
        WHERE e.id = ?
        ORDER BY e.id   
        """, (id, ))
        
        dataset = db_cursor.fetchall()
        # establishes entry for first pass
        # initialize and empty instance of entry object
        entry = Entry(0,'','',0,'')
        for row in dataset:
            # not reset the entry if the entry exists, but still add tag onto entry's array
            if row['id'] != entry.id:
                # explicity set tags to a new list in model
                entry = Entry(row['id'], row['concept'], row['entry'], row['mood_id'], row['date'], [])
                mood = Mood(row['id'], row['mood_label'])
                entry.mood = mood.__dict__
                # db_cursor.execute("""
                # SELECT
                #     tag.id,
                #     tag.tag
                # FROM entrytag et
                # JOIN tag t on t.id = et.tag_id
                # WHERE et.entry_id = ?
                # """,(entry.id, ))
                # sub_dataset = db_cursor.fetchall()
                # for sub_row in sub_dataset
                    # tag = Tag(sub_row['id'],sub_row['tag'])
                    # entry.tags.append(tag.__dict__)
        #         entries.append(entry.__dict__)
        # return json.dumps(entries)
            tag = Tag(row['tag_id'],row['tag'])
            entry.tags.append(tag.__dict__)
            # does current row id match next row id,
            # if doesn't, then add entry 
            try:
                if dataset[dataset.index(row)]['id'] != dataset[(dataset.index(row)) +1]['id']:              
                    entry.__dict__
            except:
                entry.__dict__
        return json.dumps(entry.__dict__)
            
def delete_entry(id):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        DELETE FROM Entry
        WHERE id = ?              
        """, (id, ))
        
        db_cursor.execute("""
        DELETE FROM entrytag
        WHERE entry_id = ?              
        """, (id, ))
        
def get_entries_by_search(search):

    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.mood_id,
            e.date,
            m.label mood_label
        FROM Entry e  
        JOIN Mood as m
            On m.id = e.mood_id  
        WHERE e.entry LIKE ?   
        """, ( f"%{search}%", ))

        entries = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            entry = Entry(row['id'], row['concept'], row['entry'],
                            row['mood_id'], row['date'])
            mood = Mood(row['id'], row['mood_label'])
            entry.mood = mood.__dict__
            entries.append(entry.__dict__)

    return json.dumps(entries)
def create_entry(new_entry):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Entry
            ( concept, entry, mood_id, date )
        VALUES
            ( ?, ?, ?, ?);
        """, (new_entry['concept'], new_entry['entry'],
              new_entry['moodId'], new_entry['date'], ))
        id = db_cursor.lastrowid

        new_entry['id'] = id
        
        for tag in new_entry['tags']:
            db_cursor.execute("""
            INSERT INTO entrytag
                ( tag_id, entry_id )
            VALUES
                ( ?, ?);
            """, (tag, new_entry['id'], ))


    return json.dumps(new_entry)
def update_entry(id, new_entry):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Entry
            SET
                concept = ?,
                entry = ?,
                mood_id = ?,
                date = ?
        WHERE id = ?
        """, (new_entry['concept'], new_entry['entry'],
              new_entry['moodId'], new_entry['date'], id, ))
        # Delete all tags with entry and add tags backs
        
        db_cursor.execute("""
        DELETE FROM entrytag
        WHERE entry_id = ?              
        """, (id, )) 
        for tag in new_entry['tags']:
            db_cursor.execute("""
            INSERT INTO entrytag
                ( tag_id, entry_id )
            VALUES
                ( ?, ?);
            """, (tag, new_entry['id'], ))           
            # rows_affected = db_cursor.rowcount   
        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True
    