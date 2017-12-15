import praw
import pdb
import re
import os




#search all comments in submissions with the tip-text
#and reply to these comments
subreddit = reddit.subreddit('NavTipbot')
my_inbox =reddit.inbox

for item in my_inbox.messages(limit=10):
    print(item.body)



