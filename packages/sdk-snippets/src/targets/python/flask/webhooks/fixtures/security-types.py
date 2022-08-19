import os
import sys
from flask import Flask, request
from readme_metrics.VerifyWebhook import VerifyWebhook

if os.getenv("README_API_KEY") is None:
    sys.stderr.write("Missing `README_API_KEY` environment variable")
    sys.stderr.flush()
    sys.exit(1)

app = Flask(__name__)


@app.post("/webhook")
def webhook():
    # Verify the request is legitimate and came from ReadMe
    signature = request.headers.get("readme-signature", None)

    # Your ReadMe secret
    secret = os.getenv("README_API_KEY").encode("utf8")

    try:
        VerifyWebhook(request.get_json(), signature, secret)
    except Exception as error:
        return (
            {"error": str(error)},
            401,
            {"Content-Type": "application/json; charset=utf-8"},
        )

    return (
        {
            # OAS Security variables
            "api_key": "default-api_key-key",
            "http_basic": {"user": "user", "pass": "pass"},
            "http_bearer": "default-http_bearer-key",
            "oauth2": "default-oauth2-key",
        },
        200,
        {"Content-Type": "application/json; charset=utf-8"},
    )


if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port=os.getenv("PORT", "4000"))