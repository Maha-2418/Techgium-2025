from db import Database

def debug_db():
    print("Debugging Neo4j Database Content...")
    try:
        db = Database()
        with db.driver.session(database="neo4j") as session:
            with open("debug_output.txt", "w", encoding='utf-8') as f:
                # Check for standard and sustainability
                f.write("\n--- Sample Alloy Nodes Attributes ---\n")
                result = session.run("MATCH (a:Alloy) RETURN a.code AS code, a.standard AS standard, a.sustainability_score AS score, keys(a) AS keys LIMIT 5")
                for record in result:
                    f.write(f"Code: {record['code']}\n")
                    f.write(f"Standard: {record['standard']}\n")
                    f.write(f"Sustainability: {record['score']}\n")
                    f.write(f"All Keys: {record['keys']}\n")
                    f.write("-" * 20 + "\n")

                # 3. Check Applications
                f.write("\n--- Alloys with Applications ---\n")
                result = session.run("MATCH (a:Alloy)-[:USED_FOR]->(app:Application) RETURN a.code, collect(app.name) as apps")
                for record in result:
                    f.write(f"Alloy: {record['a.code']} -> {record['apps']}\n")

    except Exception as e:
        print(f"Database Error during Debug: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    debug_db()
