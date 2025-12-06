# Choisir l'image Python officielle (compatible avec Django 5.x)
FROM python:3.11-slim

# Empêcher Python d'écrire des fichiers .pyc & désactiver le buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Créer et définir le dossier de l'application
WORKDIR /app

# Installer les dépendances
COPY requirements.txt /app/
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application dans l'image
COPY . /app/

# Exposer le port (OKD acceptera ce port)
EXPOSE 8000

# Lancer les migrations et démarrer le serveur
# (Pour dev, on utilise runserver; pour prod, remplacer par gunicorn)
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
