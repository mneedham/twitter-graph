from neo4j import GraphDatabase
import json

driver = GraphDatabase.driver("bolt://localhost")

with open("users.json", "r") as users_file, driver.session() as session:
    line = users_file.readline()
    while line:
        document = json.loads(line)
        params =  {
            "document": document,
            "keysToKeep": ["name", "username", "bio", "following", "followers"]
        }
        session.run("""
        MERGE (u:User {id: $document.id })
        SET u += apoc.map.fromLists($keysToKeep, apoc.map.values($document, $keysToKeep))
        """, params)

        line = users_file.readline()
