def clean_text(text: str) -> str:
    """Clean the text"""
    # remove newlines and tabs
    cleaned_text = text.replace("\n", " ").replace("\t", " ")
    # remove extra spaces
    cleaned_text = " ".join(cleaned_text.split())
    return cleaned_text

# check (and convert) data type to string
def dtype_string(text) -> str:
    """Ensure the input is a string."""
    if not isinstance(text, str):
        return str(text)
    return text