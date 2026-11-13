# Chat, chien ou oiseau ? — Flask

Application web Flask qui identifie un **chat**, un **chien** ou un **oiseau** sur une photo.
Le modèle (EfficientNetB0 pré-entraîné sur ImageNet, *transfer learning*) est entraîné sur Kaggle
avec le notebook `CAT-DOG-BIRD.ipynb`.

## Structure

```
chat_chien_oiseau/
├── app.py             # routes / et /predict
├── config.py          # taille d'image 224x224, chemins, noms français, seuil
├── requirements.txt
├── model.tflite       # modèle converti depuis model.keras (convert_to_tflite.py)
├── labels.json        # <- à télécharger depuis Kaggle (Output) : ["bird", "cat", "dog"]
├── templates/         # base.html, main.html, result.html
└── static/            # style.css, main.js, uploads/
```

## 1. Entraîner le modèle sur Kaggle

1. Importer le notebook : **File → Import Notebook**.
2. **Session options** : Accelerator **GPU T4 x2**, Internet **On**.
3. **Add Input** : *High-resolution Cat/Dog/Bird Image Dataset (13000)*.
4. **Run All**, puis télécharger `model.keras` et `labels.json` dans **Output**.
5. Noter la version de TensorFlow affichée par la première cellule.

## 2. Lancer l'application en local (PyCharm)

1. Convertir le modèle une fois (TensorFlow requis) : `python convert_to_tflite.py`
   (le `model.tflite` fourni est déjà converti).
2. Sous Windows, LiteRT n'existe pas : l'app utilise alors l'interpréteur TFLite de TensorFlow
   (déjà installé dans votre `.venv`). Lancer :
   ```
   pip install flask pillow numpy tensorflow==2.21.0
   python app.py
   ```
3. Ouvrir http://127.0.0.1:5000
