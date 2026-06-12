from agent import MaterialsAgent

def main():
    print("Initializing Intelligent Materials Engineering Agent...")
    agent = MaterialsAgent()
    
    print("\n✅ System Ready. Enter your engineering requirements (or 'exit' to quit).")
    print("Example: 'Need high tensile strength and good corrosion resistance'")
    
    try:
        while True:
            user_input = input("\n👷 User Input: ")
            if user_input.lower() in ['exit', 'quit']:
                print("Shutting down provided connection.")
                break
                
            response = agent.process_request(user_input)
            print("-" * 50)
            print(response)
            print("-" * 50)
            
    except KeyboardInterrupt:
        print("\nForce close.")
    finally:
        agent.close()

if __name__ == "__main__":
    main()
