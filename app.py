from flask import Flask, request, jsonify, render_template
import pipeline

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate() -> tuple:
    data = request.json
    user_input = data.get("input", "").strip()

    if not user_input:
        return jsonify({"status": "error", "message": "No input provided"}), 400

    try:
        pipeline.run(user_input)
        return jsonify({"status": "ok"})
    except ConnectionError as e:
        return jsonify({"status": "error", "message": str(e)}), 503


if __name__ == "__main__":
    app.run(debug=True)