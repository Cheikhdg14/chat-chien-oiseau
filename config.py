"""Paramètres de l'application. Ils doivent correspondre à l'entraînement Kaggle."""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

IMG_SIZE = (224, 224)                       # taille d'entrée d'EfficientNetB0
MODEL_PATH = os.path.join(BASE_DIR, "model.tflite")   # modèle converti (léger)
LABELS_PATH = os.path.join(BASE_DIR, "labels.json")   # ["bird", "cat", "dog"]
UPLOAD_DIR = os.path.join(BASE_DIR, "static", "uploads")

# Noms des classes du dataset (anglais) -> noms affichés (français)
FRENCH_NAMES = {"bird": "oiseau", "cat": "chat", "dog": "chien"}
DISPLAY_NAMES = {"bird": "un oiseau", "cat": "un chat", "dog": "un chien"}

# En dessous de ce seuil de confiance, l'application dit qu'elle n'est pas sûre
CONFIDENCE_THRESHOLD = 0.60
