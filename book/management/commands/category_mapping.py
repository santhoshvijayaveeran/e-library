# category_mapping.py
CATEGORY_MAP = {
    # Classic Fiction
    "Classics": "Classic Fiction",
    "Classical literature": "Classic Fiction",
    "Classic Fiction": "Classic Fiction",

    # Gothic / Horror
    "Frankenstein's monster (Fictitious character)": "Gothic Fiction / Horror",
    "Dracula, Count (Fictitious character)": "Gothic Fiction / Horror",
    "Gothic Fiction": "Gothic Fiction / Horror",
    "Horror": "Gothic Fiction / Horror",
    "Faust, -approximately 1540": "Gothic Fiction / Horror",

    # Mystery / Detective
    "Detective and mystery stories, English": "Mystery / Detective",
    "Detective and mystery stories": "Mystery / Detective",
    "Mystery": "Mystery / Detective",
    "Crime": "Mystery / Detective",
    "Burglars": "Mystery / Detective",
    "Beresford, Tommy (Fictitious character)": "Mystery / Detective",
    "Abduction": "Mystery / Detective",

    # Adventure
    "Adventure stories, English": "Adventure",
    "Adventure stories": "Adventure",
    "Adventure": "Adventure",
    "Pirates": "Adventure",

    # Romance
    "Man-woman relationships": "Romance",
    "Courtship": "Romance",
    "Adultery": "Romance",
    "Romance": "Romance",
    "Chastelard, Pierre de Bocosel de, 1540-1562": "Romance",

    # Fantasy
    "Fairy tales": "Fairy Tales",
    "Alice (Fictitious character from Carroll)": "Fantasy",
    "Fantasy": "Fantasy",
    "Metamorphosis": "Fantasy",

    # Drama / Plays
    "Comedy plays": "Comedy",
    "Drama": "Drama / Plays",
    "Comedy": "Comedy",
    "Herodias": "Drama / Plays",

    # Historical Fiction
    "Historical Fiction": "Historical Fiction",
    "France": "Historical Fiction",
    "England": "Historical Fiction",
    "Great Britain": "Historical Fiction",
    "Ireland": "Historical Fiction",
    "Dublin (Ireland)": "Historical Fiction",
    "Denmark": "Historical Fiction",
    "Africa": "Historical Fiction",
    "Hawaii": "Historical Fiction",
    "Frederick II, King of Prussia, 1712-1786": "Historical Fiction",
    "Arnold, Thomas, 1795-1842": "Historical Fiction",
    "Acadians": "Historical Fiction",
    "Belgians": "Historical Fiction",
    "African Americans": "Historical Fiction",
    "Aristocracy (Social class)": "Historical Fiction",
    "Brahmans": "Historical Fiction",

    # Biographical / Autobiographical
    "Autobiographical fiction": "Biographical / Autobiographical Fiction",
    "Biographical fiction": "Biographical / Autobiographical Fiction",
    "Dostoyevsky, Fyodor, 1821-1881": "Biographical / Autobiographical Fiction",
    "Benefactors": "Biographical / Autobiographical Fiction",

    # Psychological Fiction
    "Psychological Fiction": "Psychological Fiction",
    "Individuality": "Psychological Fiction",
    "Appearance (Philosophy)": "Psychological Fiction",
    "Conflict of generations": "Psychological Fiction",
    "Brothers": "Psychological Fiction",
    "Children": "Psychological Fiction",

    # Non-Fiction / Political / Philosophy
    "Non-Fiction": "Non-Fiction",
    "Political science": "Political Science / Philosophy",
    "Political Philosophy": "Political Science / Philosophy",
    "Political ethics": "Political Science / Philosophy",
    "Causation": "Political Science / Philosophy",
    "Chance": "Political Science / Philosophy",
    "Evolution (Biology)": "Non-Fiction",
    "Optimism": "Political Science / Philosophy",
    "Astrologers": "Non-Fiction",
    "Banks and banking": "Non-Fiction",
    "Corporal punishment": "Non-Fiction",
    "Courage": "Non-Fiction",

    # Feminist Fiction
    "Feminist fiction": "Feminist Fiction",

    # Bildungsroman
    "Bildungsromans": "Bildungsroman (Coming-of-age)",

    # Epistolary
    "Epistolary fiction": "Epistolary Fiction",

    # Short Story
    "Short Story": "Short Story",
    "Satire": "Comedy",

    # Fiction nationality tags -> Domestic/General
    "American fiction": "Classic Fiction",
    "French fiction": "Classic Fiction",
    "British": "Classic Fiction",
    "Domestic fiction": "Classic Fiction",
}

def get_category(raw_subject: str) -> str:
    return CATEGORY_MAP.get(raw_subject, "Non-Fiction")  # fallback