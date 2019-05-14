import twint
from neo4j import GraphDatabase
import json

driver = GraphDatabase.driver("bolt://localhost")

with driver.session() as session, \
     open("followers.json", "a", newline='', encoding="utf-8") as followers_file:
    rows = session.run("""
    match (u:User) WHERE not(exists(u.followersImported))
    WITH u ORDER BY u.pagerank DESC WHERE u.followers > 0 and u.followers < 30000
    RETURN u
    LIMIT 5
    """)

    for row in rows:
        username = row["u"]["username"]
        c = twint.Config()
        c.Username = username
        c.User_full = False
        c.Store_object = True

        twint.run.Followers(c)
        followers = twint.output.follow_object

        if not username in followers:
            followers[username] = {"followers": []}

        print(username, followers)

        json.dump(followers, followers_file, ensure_ascii=False)
        followers_file.write("\n")

        params = {"followers": followers[username]["followers"], "username": username}

        result = session.run("""
        MATCH (u:User {username: $username})
        SET u.followersImported = true
        WITH u
        UNWIND $followers AS follower
        MATCH (f:User {username: follower})
        MERGE (f)-[:FOLLOWS]->(u)
        """, params)
        print(params, result.summary().counters)

        twint.output.follow_object = {}
