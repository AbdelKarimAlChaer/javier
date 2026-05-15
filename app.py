import pathlib

from flask import Flask, request, jsonify, render_template
import pipeline
import tag_manager

app = Flask(__name__)

def extract_title(content: str) -> str:
    for line in content.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return "Untitled"
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


@app.route("/tags", methods=["GET"])
def tags() -> tuple:
    tags = list(tag_manager.load_tags().keys())
    return jsonify({"tags": tags}), 200

@app.route("/tags/<tag>", methods=["GET"])
def notes_by_tag(tag: str) -> tuple:
    all_tags = tag_manager.load_tags()
    if tag not in all_tags:
        return jsonify({"error": "tag not found"}), 404

    notes = []
    for filepath in all_tags[tag]:
        path = pathlib.Path(filepath)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            notes.append({
                "filename": path.name,
                "filepath": filepath,
                "title": extract_title(content)
            })
        except FileNotFoundError:
            continue

    return jsonify({"notes": notes}), 200

@app.route("/note", methods=["GET"])
def get_note() -> tuple:
    filepath = request.args.get("path")
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return jsonify({"content": f.read()}), 200
    except FileNotFoundError:
        return jsonify({"error": "note not found"}), 404




if __name__ == "__main__":
    app.run(debug=True)