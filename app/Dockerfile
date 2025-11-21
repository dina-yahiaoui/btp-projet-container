FROM python:3.9-slim

WORKDIR /app

# Copier les dépendances
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste de l'application
COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
