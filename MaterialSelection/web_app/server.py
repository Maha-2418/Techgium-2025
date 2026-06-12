from flask import Flask, render_template, request, jsonify
from agent import MaterialsAgent
import os

app = Flask(__name__)
# Initialize agent globally or per-request? 
# Global is better for keeping connection open, but context handling (state) is per-user.
# Since this is a simple demo, we'll instantiate per request OR handle session.
# For simplicity with 'process_request' relying on instance state, we need a session.
# But for a robust API, we should pass state back and forth.
# Let's keep it simple: Single global agent supports Single user. 
# Multi-user needs session-based agent storage.
# Given "local tool" usage, global is fine, but let's be safe and make a new agent per request for now,
# BUT we lose multi-turn context (clarification).
# Solution: simple in-memory session store by IP or Session ID.

agents = {}

def get_agent(session_id):
    if session_id not in agents:
        agents[session_id] = MaterialsAgent()
    return agents[session_id]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/query', methods=['POST'])
def query():
    data = request.json
    user_input = data.get('query')
    session_id = request.remote_addr # Simple session key
    
    if not user_input:
        return jsonify({"type": "error", "message": "No query provided."})
        
    agent = get_agent(session_id)
    try:
        response = agent.process_request(user_input)
        return jsonify(response)
    except Exception as e:
        return jsonify({"type": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
