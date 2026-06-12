from db import Database

def check_processes():
    db = Database()
    query = """
    MATCH (p:Process)
    RETURN DISTINCT p.name as name
    LIMIT 20
    """
    
    with db.driver.session() as session:
        print("--- Processes ---")
        result = session.run(query)
        for record in result:
            print(f"Process: '{record['name']}'")

    db.close()

if __name__ == "__main__":
    check_processes()
