from agent import MaterialsAgent

def test_workflow():
    print("Testing Intelligent Materials Engineering Agent...")
    agent = MaterialsAgent()
    
    with open("test_output.txt", "w", encoding='utf-8') as f:
        # Test 1: Standard Query
        input1 = "Need high tensile strength and good corrosion resistance"
        f.write(f"--- Test 1: {input1} ---\n")
        resp1 = agent.process_request(input1)
        f.write(f"{resp1}\n\n")
        
        # Test 2: Ambiguity (Simulation)
        # It's hard to force ambiguity without mocking score return, 
        # but let's try a broad query that might yield similar results.
        input2 = "Need good strength" 
        f.write(f"--- Test 2: {input2} ---\n")
        resp2 = agent.process_request(input2)
        f.write(f"{resp2}\n\n")
        
        # Check if it asked for clarification
        if "?" in resp2:
            input3 = "corrosion resistance"
            f.write(f"--- Test 3: Clarification Reply '{input3}' ---\n")
            resp3 = agent.process_request(input3)
            f.write(f"{resp3}\n\n")

    agent.close()
    print("Test run complete. Check test_output.txt")

if __name__ == "__main__":
    test_workflow()
