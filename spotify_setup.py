from flask import Flask, request
import requests
import base64
import webbrowser



CLIENT_ID = "ENTER YOUR CLIENT ID HERE"
CLIENT_SECRET = "ENTER YOUR CLIENT SECRET HERE"

REDIRECT_URI = "http://127.0.0.1:8888/callback"

SCOPES = (
    "user-read-playback-state "
    "user-modify-playback-state "
    "user-read-currently-playing "
    "user-read-playback-position"
)

app = Flask(__name__)


@app.route("/")
def home():
    return "Spotify Setup Running"


@app.route("/callback")
def callback():

    code = request.args.get("code")

    if not code:
        return "No authorization code received."

    auth = base64.b64encode(
        f"{CLIENT_ID}:{CLIENT_SECRET}".encode()
    ).decode()

    headers = {
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI
    }

    r = requests.post(
        "https://accounts.spotify.com/api/token",
        headers=headers,
        data=data
    )

    token = r.json()

    print("\n==============================")
    print("ACCESS TOKEN:\n")
    print(token["access_token"])

    print("\nREFRESH TOKEN:\n")
    print(token["refresh_token"])
    print("==============================\n")

    with open("refresh_token.txt", "w") as f:
        f.write(token["refresh_token"])

    return """
    <h1>Spotify Connected!</h1>
    <h2>You can close this window.</h2>
    """


if __name__ == "__main__":

    url = (
        "https://accounts.spotify.com/authorize"
        "?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope={SCOPES.replace(' ', '%20')}"
    )

    print("Opening Spotify login...")

    webbrowser.open(url)

    app.run(port=8888)