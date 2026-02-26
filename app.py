from flask import Flask, request, jsonify
from flask_cors import CORS
from src.rag_pipeline import AgenticRAGPipeline

app      = Flask(__name__)
CORS(app)
pipeline = AgenticRAGPipeline(pdf_dir="data")


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status":        "ok",
        "chunks_loaded": pipeline.store.collection.count()
    })


@app.route("/ask", methods=["POST"])
def ask():
    data     = request.get_json()
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "No question provided"}), 400

    result = pipeline.ask(question)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
