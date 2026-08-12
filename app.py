from flask import Flask, request, jsonify
from dotenv import load_dotenv
from postmarker.models.messages import InboundMessage

load_dotenv()

from storage import upload_pdf

app = Flask(__name__)


@app.get("/")
def home():
    return "Flask app is running."


@app.route("/test-upload", methods=["GET", "POST"])
def test_upload():
    with open("test.pdf", "rb") as f:
        upload_pdf("test.pdf", f.read())
    return jsonify({"status": "uploaded test.pdf"}), 200

@app.route("/webhook/upload", methods=["POST"])
def inbound_webhook():
    message = InboundMessage.from_json(request.get_data())

    for attachment in message.Attachments:
        upload_pdf(attachment.Name, attachment.decoded)

    return jsonify({"status": "uploaded attachments"}), 200

@app.get("/health")
def health():
    return jsonify(status="ok")


if __name__ == "__main__":
    app.run(debug=True)
