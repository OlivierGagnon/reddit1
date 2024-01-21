import praw
import pymongo
import re

#initialize praw
reddit = praw.Reddit(
    client_id="xxxxxxxxx",
    client_secret="xxxxxxxxxxx",
    user_agent="deals.finder:v1.2.3 (by /u/xxxxxxxx)",
)

#initialize mongodb client
client = pymongo.MongoClient("localhost", 27017)
#choose the db freegamefindings
db = client.freegamefindings
#then choose the table posts
posts = db.posts
#create an index so that the "id" column is the unique id so that we can avoid duplicates
db.posts.create_index([("id", pymongo.ASCENDING)], unique=True)

#get praw to get on FreeGameFindings
subreddit = reddit.subreddit("FreeGameFindings")
#pull latest 10 posts
for submission in subreddit.new(limit=10):
    gamestore = "None"
    #regular expression on the title to pull the first [] where the game store is
    gamestoreRe = re.findall(r'\[.*?\]', submission.title)
    #below just in case the return is null so that it doesn't crash
    if len(gamestoreRe) > 0:
        gamestore = gamestoreRe[0]
    #using the praw "submission" object we build a json with the data we need
    post = {
        "id": submission.id,
        "createdAt": submission.created_utc,
        "redditThread": "https://www.reddit.com" + submission.permalink,
        "redditTitle": submission.title,
        "gameLink": submission.url,
        "gameStore": gamestore
    }
    #slightly weird command to insert into mongodb in a way that duplicates won't happen
    #and it'll update new data
    posts.update_one({"id": post["id"]},{"$set": post}, upsert=True)
