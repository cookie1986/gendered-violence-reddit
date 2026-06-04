def delete_empty_rows(df, text_col):
    return df[df[text_col].str.strip().isna() == False]

def remove_automoderator_comments(df):
    return df[df['comment_author'] != 'AutoModerator']