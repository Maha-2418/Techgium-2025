from db import Database

def check_apps():
    db = Database()
    query = """
    MATCH (a:Alloy)
    OPTIONAL MATCH (a)-[r]->(n)
    RETURN DISTINCT type(r) as rel_type, labels(n) as target_labels
    LIMIT 20
    """
    
    with db.driver.session() as session:
        print("--- Relationships ---")
        result = session.run(query)
        for record in result:
            print(f"Rel: {record['rel_type']} -> {record['target_labels']}")

        print("\n--- Alloy Properties ---")
        result2 = session.run("MATCH (a:Alloy) RETURN keys(a) as props LIMIT 1")
        for record in result2:
            print(f"Node Props: {record['props']}")

    db.close()

if __name__ == "__main__":
    check_apps()
