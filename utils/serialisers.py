def reddit_sub_to_dict(submission) -> dict:
    return {
        "post_id":submission.id,
        "subreddit":submission.subreddit.display_name,
        "title":submission.title,
        "score":submission.score,
        "permalink":submission.permalink,
        "author":str(submission.author) if submission.author else None,
        "created_utc":submission.created_utc,
        "selftext":submission.selftext,
        "num_comments":submission.num_comments,
        "link":submission.url
    }