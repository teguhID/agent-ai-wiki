from flask import Flask, request, jsonify

import agents.wiki_agent as wiki_agent
import services.genai_service as genai_service


# Initialize Flask app
app = Flask(__name__)


# API endpoint
@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    query = data.get("query")

    if not query:
        return jsonify({"error": "Missing 'input' in request"}), 400

    try:
        result = wiki_agent.agent_respond(query, '1', genai_service.chain_with_history)
        
        return result
        
        # return jsonify({
        #     "response": result
        # })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, port=5001)
