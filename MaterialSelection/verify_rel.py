from neo4j import GraphDatabase
from web_app.config import Config

def verify_supported_by():
    driver = GraphDatabase.driver(
        Config.NEO4J_URI, 
        auth=(Config.NEO4J_USERNAME, Config.NEO4J_PASSWORD)
    )
    with driver.session(database=Config.NEO4J_DATABASE) as session:
        print("--- Alloys with Research Papers ---")
        query = """
        MATCH (a:Alloy)-[:SUPPORTED_BY]->(rp:ResearchPaper)
        RETURN a.code, rp.title, rp.journal
        LIMIT 10
        """
        result = session.run(query)
        for record in result:
            print(f"Alloy: {record['a.code']}, Title: {record['rp.title'][:30]}..., Journal: {record['rp.journal']}")
            
        print("\n--- Alloys WITHOUT Research Papers (Sample) ---")
        query_none = """
        MATCH (a:Alloy)
        WHERE NOT (a)-[:SUPPORTED_BY]->(:ResearchPaper)
        RETURN a.code LIMIT 5
        """
        result_none = session.run(query_none)
        for record in result_none:
            print(f"Alloy: {record['a.code']}")

    driver.close()

if __name__ == "__main__":
    verify_supported_by()
