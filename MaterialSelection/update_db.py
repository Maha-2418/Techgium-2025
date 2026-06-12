from db import Database
import random

def update_attributes():
    print("Updating Alloys with Standard and Sustainability Score...")
    db = Database()
    query = """
    MATCH (a:Alloy)
    SET a.standard = 'IS 617'
    SET a.sustainability_score = toString(round(7.0 + rand() * 2.0, 1)) + '/10'
    RETURN a.code, a.standard, a.sustainability_score
    """
    
    try:
        with db.driver.session(database="neo4j") as session:
            result = session.run(query)
            count = 0
            for record in result:
                count += 1
                print(f"Updated {record['a.code']}: Standard={record['a.standard']}, Score={record['a.sustainability_score']}")
            print(f"Total updated: {count}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    update_attributes()
