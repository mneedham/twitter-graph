import twint
from neo4j import GraphDatabase
import json

driver = GraphDatabase.driver("bolt://localhost")

with driver.session() as session, \
     open("following.json", "a", newline='', encoding="utf-8") as followers_file:
    rows = session.run("""
    match (u:User) WHERE not(exists(u.followingImported))
    WITH u ORDER BY u.pagerank DESC WHERE u.following > 0 AND u.following  < 5000
    RETURN u
    """)

    for row in rows:
        username = row["u"]["username"]
        c = twint.Config()
        c.Username = username
        c.User_full = False
        c.Store_object = True

        twint.run.Following(c)
        following = twint.output.follow_object

        if not username in following:
            following[username] = {"following": []}

        print(username, following)

        json.dump(following, followers_file, ensure_ascii=False)
        followers_file.write("\n")

        params = {"following": following[username]["following"], "username": username}

        result = session.run("""
        MATCH (u:User {username: $username})
        SET u.followingImported = true
        WITH u
        UNWIND $following AS follows
        MATCH (f:User {username: follows})
        MERGE (u)-[:FOLLOWS]->(f)
        """, params)
        print(params, result.summary().counters)

        twint.output.follow_object = {}
