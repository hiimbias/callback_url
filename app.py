from flask import Flask, request
import secrets, hashlib, base64
import requests
from flask import jsonify
import logging

app = Flask(__name__)


# Tạo code_verifier
code_verifier = secrets.token_urlsafe(43)
print("code_verifier:", code_verifier)

# Tạo code_challenge
hashed = hashlib.sha256(code_verifier.encode('ascii')).digest()
code_challenge = base64.urlsafe_b64encode(hashed).decode('utf-8').rstrip("=")
print("code_challenge:", code_challenge)


@app.route("/oauth/callback")
def zalo_callback():
    # Zalo redirect về với các tham số
    code = request.args.get("code")
    state = request.args.get("state")  # nếu bạn dùng state để xác minh
    if not code:
        return "No authorization code received", 400

    # ✅ Gửi POST request để đổi authorization code lấy access token
    token_url = "https://oauth.zaloapp.com/v4/oa/access_token"
    payload = {
        "app_id": "2195510840276531594",
        "grant_type": "authorization_code",
        "code": code,
        "code_verifier": code_verifier
    }

    response = requests.post(token_url, data=payload)
    
    return jsonify(response.json())

@app.route("/home")
def index():
    return "Welcome to Zalo OAuth Callback Handler! Please visit /oauth/callback to authorize your app."


if __name__ == "__main__":
    port = 2111
    app.run(host='0.0.0.0', port=port, debug=True)
