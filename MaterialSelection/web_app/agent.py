from nlp import extract_requirements
from db import Database
from ranking import rank_materials

class MaterialsAgent:
    def __init__(self):
        self.db = Database()
        self.context = {
            "awaiting_clarification": False,
            "last_requirements": {},
            "candidates": []
        }

    def process_request(self, input_text: str):
        try:
            # Clarification handling
            if self.context["awaiting_clarification"]:
                return self.handle_clarification(input_text)
                
            requirements = extract_requirements(input_text)
            if not requirements:
                return {
                    "type": "error",
                    "message": "I couldn't identify any specific material properties. Please specify requirements like 'tensile strength' or 'corrosion resistance'."
                }
                
            materials = self.db.get_materials(requirements)
            
            if not materials:
                return {
                    "type": "error",
                    "message": f"No materials found matching: {', '.join(requirements.keys())}."
                }

            ranked_with_scores = rank_materials(materials, requirements, return_scores=True)
            
            if not ranked_with_scores:
                 return {
                    "type": "error",
                    "message": "Found matching materials but unable to rank them due to missing property data."
                 }

            top_material, top_score = ranked_with_scores[0]
            
            # Ambiguity Check
            if len(ranked_with_scores) > 1:
                second_material, second_score = ranked_with_scores[1]
                if second_score > 0 and (top_score - second_score) / top_score < 0.1:
                    self.context["awaiting_clarification"] = True
                    self.context["last_requirements"] = requirements
                    return {
                        "type": "clarification",
                        "candidates": [top_material.get('name'), second_material.get('name')],
                        "message": f"I found multiple suitable materials ({top_material.get('name')} and {second_material.get('name')}) with similar suitability. Do you prioritize strength, corrosion resistance, hardness, or temperature performance?"
                    }

            return self.format_recommendation(top_material, top_score, ranked_with_scores[1:3], requirements)
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {
                "type": "error",
                "message": f"An internal error occurred: {str(e)}"
            }

    def handle_clarification(self, input_text: str):
        new_reqs = extract_requirements(input_text)
        combined_reqs = self.context["last_requirements"].copy()
        combined_reqs.update(new_reqs)
        self.context["awaiting_clarification"] = False
        
        materials = self.db.get_materials(combined_reqs)
        ranked_with_scores = rank_materials(materials, combined_reqs, return_scores=True)
        
        if not ranked_with_scores:
            return {"type": "error", "message": "Could not find materials after refinement."}
            
        return self.format_recommendation(ranked_with_scores[0][0], ranked_with_scores[0][1], ranked_with_scores[1:3], combined_reqs)

    def format_recommendation(self, best_material, best_score, alternatives, requirements):
        reasons = []
        for req in requirements:
            label = req.replace("_", " ").title()
            reasons.append(f"Matches high {label}")
            
        alts = []
        for mat, score in alternatives:
            code = mat.get('name', 'Unknown')
            desc = mat.get('description', '')
            display_name = f"{code} - {desc}" if desc else code
            
            alts.append({
                "name": display_name,
                "score": round(score, 1),
                "properties": self.clean_properties(mat), # Cleaned properties
                "research_papers": mat.get('research_papers', [])
            })
            
        suggestions = []
        req_keys = [k.lower() for k in requirements.keys()]
        if any("tensile" in k or "strength" in k for k in req_keys):
             suggestions.append("If higher hardness required, consider heat treatment.")
        if any("corrosion" in k for k in req_keys):
             suggestions.append("If corrosion priority increases, choose alternative alloy.")

        # Dynamic Follow-up Questions
        followups = []
        if "Tensile Strength" in requirements or "tensile_strength" in requirements.values():
            followups.append("How does temperature affect this?")
            followups.append("What about corrosion resistance?")
        elif "Corrosion Resistance" in requirements or "corrosion_resistance" in requirements.values():
            followups.append("Do you need high strength too?")
            followups.append("Check environmental resistance")
        
        # Generic follow-ups
        followups.append("Check hardness requirements")
        followups.append("Evaluate environmental resistance")
        
            # Format Name: Code - Description
        code = best_material.get('name', 'Unknown')
        desc = best_material.get('description', '')
        display_name = f"{code} - {desc}" if desc else code

        return {
            "type": "recommendation",
            "recommended_material": {
                "name": display_name,
                "score": round(best_score, 1), # ADDED SCORE
                "description": best_material.get('description', ''),
                "standard": best_material.get('standard', 'N/A'),
                "sustainability_score": best_material.get('sustainability_score', 'N/A'),
                "properties": self.clean_properties(best_material), # Cleaned properties
                "research_papers": best_material.get('research_papers', [])
            },
            "reasons": reasons,
            "alternatives": alts,
            "suggestions": suggestions,
            "follow_ups": followups[:3] # Limit to 3
        }

    def clean_properties(self, material):
        """
        Filter out internal keys and redundant snake_case keys for display.
        """
        excluded = {
            'name', 'description', 'standard', 'sustainability_score', 
            'applications', 'processes', 'alloy_node', 'code', 'research_papers'
        }
        
        display_props = {}
        # First pass: collect all potential properties
        candidates = {k: v for k, v in material.items() if k not in excluded}
        
        # Helper to normalize keys for comparison
        import re
        def normalize(s):
            # Remove all non-alphanumeric characters and lowercase
            return re.sub(r'[^a-zA-Z0-9]', '', s).lower()

        # Build map of normalized -> best_key
        normalized_map = {}
        
        for k, v in candidates.items():
            norm = normalize(k)
            
            if norm in normalized_map:
                existing_k = normalized_map[norm]
                # Preference Logic:
                # 1. Prefer Title Case (Has spaces)
                # 2. Prefer Uppercase letters (e.g. HBW)
                # 3. Prefer containing parentheses (often units)
                
                score_k = (k.count(' ') * 2) + sum(1 for c in k if c.isupper()) + (1 if '(' in k else 0)
                score_existing = (existing_k.count(' ') * 2) + sum(1 for c in existing_k if c.isupper()) + (1 if '(' in existing_k else 0)
                
                if score_k > score_existing:
                    normalized_map[norm] = k
            else:
                normalized_map[norm] = k
                
        # Build final dict with filtered keys
        for orig_k in normalized_map.values():
            display_props[orig_k] = candidates[orig_k]
            
        return display_props

    def close(self):
        self.db.close()
