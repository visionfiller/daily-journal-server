class Entry():

    def __init__(self, id, concept, entry, mood_id):
        self.id = id
        self.concept = concept
        self.entry = entry
        self.mood_id = mood_id
        self.mood = None