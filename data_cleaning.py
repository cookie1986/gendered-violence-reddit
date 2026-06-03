import pandas as pd
from src.queries.get_posts_and_comments import query_all_posts, query_all_comments
from src.cleaning.text_cleaning import clean_text

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

# clean post title text and selftext text
posts_df["title_clean"] = posts_df["title_raw"].apply(clean_text)
posts_df["selftext_clean"] = posts_df["selftext_raw"].apply(clean_text)

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

# clean comment body text
comments_df["body_clean"] = comments_df["body_raw"].apply(clean_text)

# save cleaned comments to csv
comments_df.to_csv("data/cleaned/comments.csv", index=False)