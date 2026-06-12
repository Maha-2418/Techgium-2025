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
    # Only these ratings exist in DB based on debug output
    
    # Quantitative Properties (PropertyValue nodes)
    "tensile strength": "Tensile Strength",
    "strength": "Tensile Strength",
    "tensile": "Tensile Strength",
    "hardness": "Brinell Hardness (HBW)", # Updated name based on DB
    "brinell": "Brinell Hardness (HBW)",
    "hbw": "Brinell Hardness (HBW)",
    
    # Process
    "sand casting": "process:Sand Casting",
    "sand cast": "process:Sand Casting",
    "gravity": "process:Gravity Casting",
    "gravity die": "process:Gravity Casting",
    "pressure": "process:Pressure Die Casting",
    "pressure die": "process:Pressure Die Casting",
    "die casting": "process:Die Casting"
}

def extract_requirements(user_input: str) -> dict:
    requirements = {}
    lower_input = user_input.lower()
    
    for key, prop_name in PROPERTY_KEYWORDS.items():
        if key in lower_input:
            if prop_name.startswith("process:"):
                requirements["process"] = prop_name.split(":")[1]
            else:
                # Check for "low" qualifier before the key
                # Simple check: is "low " immediately before or " low" immediately after?
                # Actually, "low density" is the common phrase.
                # Let's check if the word "low" appears in the input near this key? 
                # Or simplistic: if "low [key]" in input set to Low, else High.
                
                req_value = "High" # Default
                
                # Check for explicit qualifiers
                if f"low {key}" in lower_input or f"low {prop_name.lower().replace('_', ' ')}" in lower_input:
                    req_value = "Low"
                elif f"medium {key}" in lower_input or f"medium {prop_name.lower().replace('_', ' ')}" in lower_input:
                    req_value = "Medium"
                elif f"high {key}" in lower_input:
                     req_value = "High"
                
                requirements[prop_name] = req_value
            
    return requirements
