import json
import os
import threading
import uuid

import numpy as np
from flask import Flask, redirect, render_template, request, url_for
from PIL import Image
from werkzeug.utils import secure_filename

try:                                    # serveur Linux (Render) : LiteRT, léger
    from ai_edge_litert.interpreter import Interpreter
except ImportError:                     # PC Windows : LiteRT n'existe pas, on prend celui de TensorFlow
    from tensorflow.lite.python.interpreter import Interpreter

from config import (CONFIDENCE_THRESHOLD, DISPLAY_NAMES, FRENCH_NAMES, IMG_SIZE,
                    LABELS_PATH, MODEL_PATH, UPLOAD_DIR)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024    # 8 Mo max par image
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Modèle TFLite : mêmes prédictions que model.keras, sans TensorFlow (~90 Mo de RAM)
interpreter = Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()
INPUT = interpreter.get_input_details()[0]["index"]
OUTPUT = interpreter.get_output_details()[0]["index"]
model_lock = threading.Lock()                          # l'interpréteur n'est pas thread-safe

with open(LABELS_PATH, encoding="utf-8") as f:
    CLASS_NAMES = json.load(f)                          # ['bird', 'cat', 'dog']


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def predict_image(path):
    # Même prétraitement qu'à l'entraînement : RGB, 224x224 (interpolation nearest), pixels 0-255
    img = Image.open(path).convert("RGB").resize(IMG_SIZE, Image.NEAREST)
    x = np.asarray(img, dtype=np.float32)[np.newaxis, ...]
    with model_lock:
        interpreter.set_tensor(INPUT, x)
        interpreter.invoke()
        probs = interpreter.get_tensor(OUTPUT)[0]
    return {name: float(p) for name, p in zip(CLASS_NAMES, probs)}


@app.route("/")
def home():
    return render_template("main.html", error=request.args.get("error"))


@app.route("/predict", methods=["POST"])
def predict():
    file = request.files.get("file")
    if not file or file.filename == "":
        return redirect(url_for("home", error="Choisissez une image avant de lancer l'identification."))
    if not allowed_file(file.filename):
        return redirect(url_for("home", error="Format non accepté. Utilisez JPG, PNG ou WEBP."))

    ext = secure_filename(file.filename).rsplit(".", 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"               # nom unique, pas d'écrasement
    file_path = os.path.join(UPLOAD_DIR, filename)
    file.save(file_path)

    try:
        scores = predict_image(file_path)
    except Exception:
        os.remove(file_path)
        return redirect(url_for("home", error="Image illisible. Essayez un autre fichier."))

    best = max(scores, key=scores.get)
    confidence = scores[best]

    if confidence >= CONFIDENCE_THRESHOLD:
        label = f"C'est {DISPLAY_NAMES.get(best, best)}"
    else:
        label = "Pas sûr : ni chat, ni chien, ni oiseau ?"

    ranked = [(FRENCH_NAMES.get(n, n), p)
              for n, p in sorted(scores.items(), key=lambda kv: kv[1], reverse=True)]
    return render_template("result.html", label=label, best=best, confidence=confidence,
                           best_fr=FRENCH_NAMES.get(best, best), ranked=ranked,
                           image_url=url_for("static", filename=f"uploads/{filename}"))


@app.errorhandler(413)
def too_large(_):
    return redirect(url_for("home", error="Image trop lourde (8 Mo maximum)."))


if __name__ == "__main__":
    app.run(debug=True)
