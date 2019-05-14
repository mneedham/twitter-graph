import twint

# Configure
c = twint.Config()
c.Search = "neo4j OR \"graph database\" OR \"graph databases\" OR graphdb OR graphconnect OR @neoquestions OR @Neo4jDE OR @Neo4jFr OR neotechnology"
c.Store_json = True
c.Custom["user"] = ["id", "tweet", "user_id", "username", "hashtags", "mentions"]
c.User_full = True
c.Output = "tweets.json"

twint.run.Search(c)
