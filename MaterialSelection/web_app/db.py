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
        if not requirements:
            return []
            
        # Check if a process constraint exists
        target_process = requirements.get("process")

        query = """
        MATCH (a:Alloy)
        """
        
        if target_process:
            query += f"MATCH (a)-[:PROCESSED_BY]->(proc:Process) WHERE toLower(proc.name) CONTAINS toLower('{target_process}') "
        
        query += """
        // 1. Collect Ratings
        OPTIONAL MATCH (a)-[:HAS_RATING]->(r:Rating)
        
        // 2. Collect Quantitative Properties
        OPTIONAL MATCH (a)-[:HAS_PROPERTY_VALUE]->(pv:PropertyValue)-[:FOR_PROPERTY]->(p:Property)

        // 3. Collect Applications
        OPTIONAL MATCH (a)-[:USED_FOR]->(app:Application)
        
        // 4. Collect Processes
        OPTIONAL MATCH (a)-[:PROCESSED_BY]->(proc_node:Process)
        
        // 5. Collect Research Papers
        OPTIONAL MATCH (a)-[:SUPPORTED_BY]->(rp:ResearchPaper)
        
        RETURN 
            a.code as name, 
            a.description as description,
            a.standard as standard,
            a.sustainability_score as sustainability_score,
            a as alloy_node,
            collect(DISTINCT {type: 'rating', id: r.id, value: r.value, key: r.id}) as ratings,
            collect(DISTINCT {type: 'numeric', name: p.name, key: p.key, value: pv.value, unit: pv.unit}) as properties,
            collect(DISTINCT app.name) as applications,
            collect(DISTINCT proc_node.name) as processes,
            collect(DISTINCT {title: rp.title, reason: rp.journal}) as research_papers
        """
        
        try:
            with self.driver.session(database=Config.NEO4J_DATABASE) as session:
                result = session.run(query)
                materials = []
                for record in result:
                    mat = dict(record['alloy_node'])
                    mat['name'] = record['name']
                    mat['standard'] = record.get('standard', 'Unknown')
                    mat['sustainability_score'] = record.get('sustainability_score', 'N/A')
                    
                    for r in record['ratings']:
                        if r['id']:
                            # Only use the cleaned key, not the raw ID
                            parts = r['id'].split('|')
                            if len(parts) >= 2:
                                key = parts[1]
                                mat[key] = r['value']
                                
                    for p in record['properties']:
                        if p['name']:
                            mat[p['name']] = p['value']
                        if p['key']:
                            mat[p['key']] = p['value']
                    
                    mat['applications'] = record['applications']
                    mat['processes'] = record['processes']
                    mat['research_papers'] = [rp for rp in record['research_papers'] if rp['title'] or rp['reason']]
                    
                    materials.append(mat)
                
                return materials

        except Exception as e:
            print(f"Database error: {e}")
            return []
