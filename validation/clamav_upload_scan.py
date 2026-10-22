# Python.ClamAV.json -> "ClamAV Python" [SecurityTools]
# Expected: import clamd
import io
import os

import clamd
from flask import Flask, abort, request

app = Flask(__name__)
scanner = clamd.ClamdNetworkSocket(host=os.environ.get("CLAMD_HOST", "clamav"), port=int(os.environ.get("CLAMD_PORT", "3310")))


@app.post("/attachments")
def upload_attachment():
    upload = request.files.get("file")
    if upload is None:
        abort(400)
    data = upload.read()
    result = scanner.instream(io.BytesIO(data))
    status, signature = result["stream"]
    if status == "FOUND":
        app.logger.warning("rejected upload %s: %s", upload.filename, signature)
        abort(422)
    return {"size": len(data)}, 201
