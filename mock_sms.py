from flask import Flask, request, jsonify


app = Flask(__name__)
PLAYLISTS = []


@app.route('/api/playlists', methods=('POST',))
def save_playlists():
    playlist_data = request.json
    PLAYLISTS.append(playlist_data)
    return jsonify(message='SUCCESS', playlists_added=len(playlist_data))


@app.route('/api/playlists', methods=('GET',))
def get_playlists():
    return jsonify(playlists=PLAYLISTS), 200


if __name__ == '__main__':
    app.run('0.0.0.0', 9090, debug=True)
