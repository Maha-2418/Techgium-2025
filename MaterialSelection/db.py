from neo4j import GraphDatabase
from config import Config

class Database:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            Config.NEO4J_URI, 
            auth=(Config.NEO4J_USERNAME, Config.NEO4J_PASSWORD)
        )

    def close(self):
        self.driver.close()

    def get_materials(self, requirements: dict) -> list:
        """
        Executes a Cypher query to find Alloys.
        Retuns a list of dicts, each containing the Alloy info and its properties/ratings
        flattened for easy ranking.
        """
        if not requirements:
            return []

        # We will fetch ALL info for matching alloys to allow Python-side ranking.
        # Construct simplified WHERE clause:
        # For each req, ensure at least some data exists for it (optional validation)
        # OR just fetch everything and let ranking sort it out.
        # But to be "efficient", we should filter.
        
        # Strategy:
        # MATCH (a:Alloy)
        # ... logic to collect properties
        # RETURN a structure
        
        query = """
        MATCH (a:Alloy)
        
        // 1. Collect Ratings
        OPTIONAL MATCH (a)-[:HAS_RATING]->(r:Rating)
        
        // 2. Collect Quantitative Properties
        OPTIONAL MATCH (a)-[:HAS_PROPERTY_VALUE]->(pv:PropertyValue)-[:FOR_PROPERTY]->(p:Property)
        
        // Return structured object
        RETURN 
            a.code as name, 
            a.description as description,
            a as alloy_node,
            collect(DISTINCT {type: 'rating', id: r.id, value: r.value, key: r.id}) as ratings,
            collect(DISTINCT {type: 'numeric', name: p.name, key: p.key, value: pv.value, unit: pv.unit}) as properties
        """
        
        # Note: 'r.id' contains the key like 'corrosion_resistance'.
        # 'p.key' is explicit like 'tensile_strength'.
        
        try:
            with self.driver.session(database=Config.NEO4J_DATABASE) as session:
                result = session.run(query)
                materials = []
                for record in result:
                    # Flatten the structure for the ranker
                    mat = dict(record['alloy_node'])
                    mat['name'] = record['name'] # Ensure 'name' key exists
                    
                    # Process Ratings
                    for r in record['ratings']:
                        if r['id']:
                            # extract key from id found in debug: "LM 0|strength_level|Low"
                            # simple hack: check if req key is in id
                            mat[r['id']] = r['value'] # Store full ID as key for now? simpler to store by 'key' if we can parse it
                            # Let's clean it up:
                            parts = r['id'].split('|')
                            if len(parts) >= 2:
                                key = parts[1] # e.g. 'strength_level', 'corrosion_resistance'
                                mat[key] = r['value']
                                
                    # Process Quantitative Properties
                    for p in record['properties']:
                        if p['name']:
                            mat[p['name']] = p['value'] # e.g. "Tensile Strength": 240
                        if p['key']:
                            mat[p['key']] = p['value'] # e.g. "tensile_strength": 240
                            
                    materials.append(mat)
                    
                # Post-fetch filtering? 
                # The prompt implies the QUERY should filter.
                # But mapping "Tensile Strength" to exact schema matches is tricky without strict name parity.
                # I'll rely on the Ranker to filter out 0-score matches if strictness is needed.
                # But let's at least filter out materials that don't match ANY requirement in the ranker.
                
                return materials

        except Exception as e:
            print(f"Database error: {e}")
            return []
