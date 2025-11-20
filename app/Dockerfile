# On part d'une image Python légère
FROM python:3.9-slim

# On se place dans le dossier de travail
WORKDIR /app

# On copie le fichier des dépendances
COPY requirements.txt .

# On installe les librairies (Flask, mysql-connector...)
RUN pip install --no-cache-dir -r requirements.txt

# On copie tout le reste du code (app.py)
COPY . .

# On dit que l'app écoute sur le port 5000
EXPOSE 5000

# La commande pour lancer l'app quand le conteneur démarre
CMD ["python", "app.py"]