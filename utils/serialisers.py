from typing import Any, Dict

def reddit_post_to_dict(submission) -> dict:
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

def reddit_comment_to_dict(comment, reddit_post_id: str) -> Dict[str, Any]:
    return {
        "reddit_id":comment.id,
        "reddit_post_id":reddit_post_id,
        "parent_id":comment.parent_id,
        "author":str(comment.author) if comment.author else None,
        "body":comment.body,
        "score":comment.score,
        "created_utc":comment.created_utc,
        "permalink":comment.permalink,
        "is_submitter":getattr(comment, "is_submitter", None),
        "stickied":getattr(comment, "stickied", None),
        "distinguished":getattr(comment, "distinguished", None),
        "edited":comment.edited if comment.edited else False
    }