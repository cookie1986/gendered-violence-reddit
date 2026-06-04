import re
import json

def match_keywords(text: str, keywords_dir: str) -> bool:
    """Check if the text contains any of the keywords."""
    with open(keywords_dir, "r") as f:
        keywords = json.load(f)
    # group all values into one list
    keywords = [item for sublist in keywords.values() for item in sublist]
    
    # Match keywords as whole words, case insensitive
    for keyword in keywords:
        pattern = r'\b' + re.escape(keyword) + r'\b'
        if re.search(pattern, text, re.I):
            return True
    return False