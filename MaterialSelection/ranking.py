def sanitize_score(val):
    """
    Convert string ratings to numeric score.
    """
    if isinstance(val, (int, float)):
        return float(val)
        
    if isinstance(val, str):
        v = val.lower()
        if 'high' in v: return 100.0
        if 'medium' in v: return 50.0
        if 'low' in v: return 25.0
        
        # Try numeric regex
        import re
        match = re.search(r"[-+]?\d*\.\d+|\d+", val)
        if match:
            return float(match.group())
            
    return 0.0

def score_material(material: dict, requirements: dict) -> float:
    score = 0.0
    
    # Weights logic
    is_strength_focused = "Tensile Strength" in requirements or "Proof Stress (Rp0.2)" in requirements or "tensile_strength" in requirements.values()
    is_corrosion_focused = "Corrosion Resistance" in requirements or "corrosion_resistance" in requirements.values()
    
    weights = {}
    if is_strength_focused and not is_corrosion_focused:
        weights = {
            "Tensile Strength": 0.4,
            "tensile_strength": 0.4,
            "strength_level": 0.3,
            "Proof Stress": 0.3,
            "proof_stress_rp0_2": 0.3
        }
    elif is_corrosion_focused and not is_strength_focused:
        weights = {
            "corrosion_resistance": 0.5,
            "environmental_resistance": 0.3, 
            "temperature_resistance": 0.2
        }
    else:
        # Balanced or Default
        pass

    # Generic Scoring Loop  
    for req_input, req_expected_val in requirements.items():
        # Determine weight
        w = 0.5 # Default
        if is_strength_focused:
            if "strength" in req_input.lower(): w = 0.4
            elif "proof" in req_input.lower(): w = 0.3
        elif is_corrosion_focused:
            if "corrosion" in req_input.lower(): w = 0.5
            elif "environment" in req_input.lower(): w = 0.3
            elif "temperature" in req_input.lower(): w = 0.2
            
        # Find value in material
        potential_keys = [
            req_input, 
            req_input.lower().replace(" ", "_"),
             # Special mappings 
            "tensile_strength" if "tensile" in req_input.lower() else None,
            "corrosion_resistance" if "corrosion" in req_input.lower() else None,
            "strength_level" if "strength" in req_input.lower() else None
        ]
        
        found_val = 0.0
        for k in potential_keys:
            if k and k in material:
                found_val = sanitize_score(material[k])
                if found_val > 0: 
                    break
        
        score += found_val * w

    return score


def rank_materials(materials: list, requirements: dict, return_scores=False) -> list:
    """
    Ranks materials. 
    If return_scores is True, returns list of (material, score) tuples.
    Otherwise returns list of materials.
    """
    # Deduplicate
    unique_materials = {m.get('name', str(m)): m for m in materials}.values()
    
    scored = []
    for m in unique_materials:
        s = score_material(m, requirements)
        if s > 0: 
            scored.append((m, s))
            
    scored.sort(key=lambda x: x[1], reverse=True)
    
    if return_scores:
        return scored
    return [m[0] for m in scored]
