from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

names = ["WoW Lich King", 
         "Cosmere Reading Order", 
         "Amazon Astro", 
         "Project Hail Mary", 
         "Dune", 
         "Worlds League of Legends 2025",
         "Cooking meat",
         "Cooking burger",
         "Lord of the Rings",
         "Monster truck"
        ]
videos = [
    "https://www.youtube.com/embed/tyNgbHX9p2U",
    "https://www.youtube.com/embed/0mC8dsQJK7w",
    "https://www.youtube.com/embed/6UjH5T-wy5Q",
    "https://www.youtube.com/embed/m08TxIsFTRI",
    "https://www.youtube.com/embed/n9xhJrPXop4",
    "https://www.youtube.com/embed/2GWz9PqiywM",
    "https://www.youtube.com/embed/05f8sG4OhZs",
    "https://www.youtube.com/embed/IItSCWUndgM",
    "https://www.youtube.com/embed/PZC6KCAQUks",
    "https://www.youtube.com/embed/PHGwHp86Y1o"
]

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/video/<int:id>", methods=["GET"])
def getVideo(id):

    if(int(id) > len(videos)):
        return jsonify({
            "video": videos[0],
            "name": names[0],
            "id": 1,
            "totalVideos": len(videos)
        }), 200
    elif (int(id) < 1):
        return jsonify({
            "video": videos[len(videos) - 1],
            "name": names[len(videos) - 1],
            "id": len(videos),
            "totalVideos": len(videos)
        }), 200
    else:
        return jsonify({
            "video": videos[int(id) - 1],
            "name": names[int(id) - 1],
            "id": id,
            "totalVideos": len(videos)
        }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3001, debug=True, use_reloader=False)