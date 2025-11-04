# Inventario de Tienda (Flask + MongoDB)

Proyecto final CBTIS272 - Inventario de Tienda.

## Requisitos
- Python 3.10+
- MongoDB Atlas

## Variables de entorno
- MONGO_URI (cadena de conexión)
- FLASK_SECRET (clave secreta opcional)

## Instalación local
1. python -m venv venv
2. source venv/bin/activate (o venv\Scripts\activate en Windows)
3. pip install -r requirements.txt
4. export MONGO_URI="tu_mongo_uri"
5. flask run

## Deploy en Render
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`
- Env Vars: MONGO_URI, FLASK_SECRET
