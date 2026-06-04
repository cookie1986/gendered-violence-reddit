import pandas as pd
from queries.get_posts_and_comments import query_all_posts, query_all_comments
from cleaning.text_cleaning import clean_text, dtype_string
from cleaning.data_cleaning import delete_empty_rows, remove_automoderator_comments

# query db and return all posts
posts = query_all_posts()

# convert to dataframe
posts_df = pd.DataFrame(posts, columns=[
    "reddit_post_id", 
    "subreddit_name", 
    "title_raw", 
    "selftext_raw", 
    "post_author", 
    "post_score", 
    "created_utc", 
    "post_url"
])

# remove duplicates based on reddit_post_id
posts_df = posts_df.drop_duplicates(subset=["reddit_post_id"])

# delete empty rows in title_raw
posts_df = delete_empty_rows(posts_df, "title_raw")

# check text fields are strings and convert if necessary
posts_df["title_raw"] = posts_df["title_raw"].apply(dtype_string)
posts_df["selftext_raw"] = posts_df["selftext_raw"].apply(dtype_string)

# clean post title text and selftext text
posts_df["title_clean"] = posts_df["title_raw"].apply(clean_text)
posts_df["selftext_clean"] = posts_df["selftext_raw"].apply(clean_text)

# drop the raw text columns
posts_df = posts_df.drop(columns=["title_raw", "selftext_raw"])

# save cleaned posts to csv
posts_df.to_csv("data/cleaned/posts.csv", index=False)

# query comments db and return all
comments = query_all_comments()

# remove duplicates based on reddit_comment_id
comments = list({comment[0]: comment for comment in comments}.values())

# remove comments with '[removed]' in body_raw
comments = [comment for comment in comments if comment[3] != "[removed]"]

# convert to dataframe
comments_df = pd.DataFrame(comments, columns=[
    "reddit_comment_id",
    "post_id",
    "comment_author",
    "body_raw",
    "comment_score",
    "created_utc"
])

# remove comments by AutoModerator
comments_df = remove_automoderator_comments(comments_df)

# remove empty rows in body_raw
comments_df = delete_empty_rows(comments_df, "body_raw")

# check text fields are strings and convert if necessary
comments_df["body_raw"] = comments_df["body_raw"].apply(dtype_string)

# clean comment body text
comments_df["body_clean"] = comments_df["body_raw"].apply(clean_text)

# drop the raw text columns
comments_df = comments_df.drop(columns=["body_raw"])

# save cleaned comments to csv
comments_df.to_csv("data/cleaned/comments.csv", index=False)