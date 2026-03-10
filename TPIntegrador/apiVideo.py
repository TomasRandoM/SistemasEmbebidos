from flask import Flask, request, jsonify
from flask_cors import CORS



app = Flask(__name__)
CORS(app)

names = ["WoW Lich King", 
         "Cosmere Reading Order", 
         "Show Me How To Live", 
         "Project Hail Mary", 
         "Dune", 
         "Worlds League of Legends 2025",
         "Cooking meat",
         "Cooking burger",
         "Te Para Tres",
         "Monster truck"
         ]
videos = [
    "https://www.youtube.com/watch?v=tyNgbHX9p2U",
    "https://www.youtube.com/watch?v=0mC8dsQJK7w",
    "https://www.youtube.com/watch?v=vVXIK1xCRpY",
    "https://www.youtube.com/watch?v=m08TxIsFTRI",
    "https://www.youtube.com/watch?v=n9xhJrPXop4",
    "https://www.youtube.com/watch?v=2GWz9PqiywM",
    "https://www.youtube.com/watch?v=05f8sG4OhZs",
    "https://www.youtube.com/watch?v=IItSCWUndgM",
    "https://www.youtube.com/watch?v=1mbBQPBGP1g",
    "https://www.youtube.com/watch?v=PHGwHp86Y1o"
]

@app.route("/video/<int:id>", methods=["GET"])
def getVideo(id):
    
    if (int(id) > len(videos) or int(id) < 1):
        return jsonify({"error": "Video not found"}), 404
    else:
        return jsonify({
            "video": videos[int(id) - 1],
            "name": names[int(id) - 1],
            "id": id
        }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3001, debug=True, use_reloader=False)