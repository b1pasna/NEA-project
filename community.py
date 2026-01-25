from flask import Flask, request, jsonify
from database import get_connection, init_db
from moderation import validate_comment
from news import news_update

app = Flask(__name__)
init_db()

# news
@app.route("/news", methods=["GET"])
def get_news():
    return jsonify(news_update())


# posts
@app.route("/posts", methods=["GET"])
def fetch_posts():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM posts")
    posts = cur.fetchall()
    conn.close()
    return jsonify(posts)


@app.route("/posts/refresh", methods=["GET"])
def refresh_posts():
    return fetch_posts()


@app.route("/posts", methods=["POST"])
def create_post():
    data = request.json
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO posts (author, content) VALUES (?, ?)",
        (data["author"], data["content"])
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Post created"})


@app.route("/posts/<int:post_id>", methods=["DELETE"])
def delete_posts(post_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM posts WHERE id=?", (post_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Post deleted"})


# comments
@app.route("/comments", methods=["POST"])
def add_comment():
    data = request.json
    if not validate_comment(data["content"]):
        return jsonify({"error": "Inappropriate content"}), 400

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO comments (post_id, author, content) VALUES (?, ?, ?)",
        (data["post_id"], data["author"], data["content"])
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Comment added"})


# likes
@app.route("/posts/<int:post_id>/like", methods=["POST"])
def like_post(post_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE posts SET likes = likes + 1 WHERE id=?",
        (post_id,)
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Post liked"})


# report
@app.route("/posts/<int:post_id>/report", methods=["POST"])
def report_post(post_id):
    data = request.json
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO reports (post_id, reason) VALUES (?, ?)",
        (post_id, data["reason"])
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Post reported"})


# reactions
@app.route("/posts/<int:post_id>/reaction", methods=["POST"])
def add_reactions(post_id):
    data = request.json
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO reactions (post_id, reaction) VALUES (?, ?)",
        (post_id, data["reaction"])
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Reaction added"})


if __name__ == "__main__":
    app.run(debug=True)
