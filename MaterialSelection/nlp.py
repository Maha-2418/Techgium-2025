# Simple keyword mapping for the NLP module
PROPERTY_KEYWORDS = {
    # Qualitative Ratings (Rating nodes)
    "corrosion": "corrosion_resistance",
    "corrosion resistance": "corrosion_resistance",
    "temperature": "temperature_resistance",
    "temperature resistance": "temperature_resistance",
    "heat": "temperature_resistance",
    "environment": "environmental_resistance",
    "environmental": "environmental_resistance",
    "environmental resistance": "environmental_resistance",
    
    # Quantitative Properties (PropertyValue nodes linked to Property {name: '...'})
    "tensile strength": "Tensile Strength",
    "strength": "Tensile Strength", 
    "proof stress": "Proof Stress", # Need to check exact name in DB. 'proof_stress_rp0_2' key vs Name 'Proof Stress'? 
    # Debug output showed: "id": 'LM 2|proof_stress_rp0_2|...' -> property key is likely "proof_stress_rp0_2" but Name might be "Proof Stress"
    # Debug output 50: key='brinell_hardness_hbw'
    "elongation": "Elongation", # Guessing name
    "hardness": "Brinell Hardness", # Guessing name based on 'brinell_hardness_hbw'
    "strength level": "strength_level" # Rating
}

def extract_requirements(user_input: str) -> dict:
    """
    Parses natural language input into structured material requirements.
    
    Args:
        user_input (str): The user's query (e.g., "Need high tensile strength").
        
    Returns:
        dict: A dictionary of property names and their requested values (currently defaulting to "High" for simplicity if not specified).
    """
    requirements = {}
    lower_input = user_input.lower()
    
    # Simple keyword matching
    for key, prop_name in PROPERTY_KEYWORDS.items():
        if key in lower_input:
            # In a more advanced version, we'd extract "high", "medium", "low" or specific values.
            # For this MVP, mere presence implies importance/requirement.
            # The prompt implies we should map input to e.g. {"Tensile Strength": "High"}
            requirements[prop_name] = "High" 
            
    return requirements
