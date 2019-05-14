import twint
import json

users = set()

with open("tweets.json", "r") as tweets_file:
    line = tweets_file.readline()
    while line:
        document = json.loads(line)
        users.add(document["username"])
        line = tweets_file.readline()

print(users)

# for user in users:
#     c = twint.Config()
#     c.Username = user
#     c.Store_json = True
#     c.User_full = True
#     c.Output = "users.json"
#
#     twint.run.Lookup(c)

# # Configure
# c = twint.Config()
# c.Search = "#neo4j"
# c.Store_json = True
# c.Custom["user"] = ["id", "tweet", "user_id", "username", "hashtags", "mentions"]
# c.User_full = True
# c.Output = "users.json"
#
# twint.run.Search(c)
