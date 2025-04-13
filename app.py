import agents.wiki_agent as wiki_agent

from flask import Flask, request, jsonify

app = Flask(__name__)

# ------------------ FLASK ENDPOINT ------------------
@app.route('/ask', methods=['POST'])
def ask_wiki():
    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({"error": "Permintaan tidak valid. Harap sertakan 'query' dalam JSON."}), 400

    query = data['query']
    response = wiki_agent.agent_respond(query)
    
    # return response
    
    return jsonify({
        "response": response
    })


# ------------------ MAIN (for local testing) ------------------
if __name__ == "__main__":
    print("Flask app is running on http://127.0.0.1:5000/")
    app.run(debug=True)