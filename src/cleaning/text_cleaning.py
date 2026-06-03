def clean_text(text: str) -> str:
    """Clean the text"""
    # remove newlines and tabs
    cleaned_text = text.replace("\n", " ").replace("\t", " ")
    # remove extra spaces
    cleaned_text = " ".join(cleaned_text.split())
    return cleaned_text
