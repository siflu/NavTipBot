import praw
import pdb
import re
import os

reddit = praw.Reddit('NavTipBot')

#text file to save comments, that we already replied to
if not os.path.isfile("comments_replied_to.txt"):
    comments_replied_to = []

else:
    with open("comments_replied_to.txt", "r") as f:
        comments_replied_to = f.read()
        comments_replied_to = comments_replied_to.split("\n")
        comments_replied_to = list(filter(None, comments_replied_to))


#search all comments in submissions with the tip-text
#and reply to these comments
subreddit = reddit.subreddit('NavTipbot')
for submission in subreddit.hot(limit=10):
    for comment in submission.comments:

        #only reply, if not already replied to this comment
        if comment.id not in comments_replied_to:
            if re.search("!tip x nav /u/NavTipBot", comment.body, re.IGNORECASE): #TODO: use regex for number
                comment.reply("This is an automatic answer!")
                comments_replied_to.append(comment.id)


with open("comments_replied_to.txt", "w") as f:
    for comment_id in comments_replied_to:
        f.write(comment_id + "\n")