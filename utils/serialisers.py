def reddit_sub_to_dict(submission) -> dict:
    return {
        "id":submission.id,
        "title":submission.title,
        "score":submission.score,
        "url":submission.url,
        "permalink":submission.permalink,
        "author":str(submission.author) if submission.author else None,
        "created_utc":submission.created_utc,
        "num_comments":submission.num_comments,
        "selftext":submission.selftext
    }