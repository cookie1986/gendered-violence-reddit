import pandas as pd
from src.features.keyword_matching import match_keywords

# load cleaned posts and comments
posts_df = pd.read_csv("data/cleaned/posts.csv")
comments_df = pd.read_csv("data/cleaned/comments.csv")

# add keyword match feature to posts
posts_df["keyword_match"] = posts_df.apply(
    lambda row: match_keywords(str(row["title_clean"]) + " " + str(row["selftext_clean"]), "data/keywords/farrell_keywords.json"), axis=1
)
# add keyword match feature to comments
comments_df["keyword_match"] = comments_df["body_clean"].apply(
    lambda text: match_keywords(text, "data/keywords/farrell_keywords.json")
)
# save posts and comments with keyword match feature to csv
posts_df.to_csv("data/processed/posts.csv", index=False)
comments_df.to_csv("data/processed/comments.csv", index=False)