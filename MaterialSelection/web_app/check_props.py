from db import Database

def check_structure():
    db = Database()
    query = """
    MATCH (p:Property)
    RETURN DISTINCT p.name as name, p.key as key
    ORDER BY name
    """
    
    query2 = """
    MATCH (r:Rating)
    RETURN DISTINCT r.id as id
    LIMIT 20
    """
    
    with db.driver.session() as session:
        print("--- Quantitative Properties ---")
        result = session.run(query)
        for record in result:
            print(f"Name: '{record['name']}', Key: '{record['key']}'")
            
        print("\n--- Qualitative Ratings (Sample) ---")
        result2 = session.run(query2)
        for record in result2:
            print(f"ID: '{record['id']}'")

    db.close()

if __name__ == "__main__":
    check_structure()
