from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(inventario)
app.secret_key = os.getenv("FLASK_SECRET", "dev-secret")

MONGO_URI = os.environ.get(
    "MONGO_URI", "mongodb+srv://menesescelangelcbtis272_db_user:admin1243@inventario.daylvqt.mongodb.net/")

try:
   
    client = MongoClient(
        MONGO_URI,
        tls=True,
        tlsAllowInvalidCertificates=False,
        serverSelectionTimeoutMS=10000
    )
    db = client.get_default_database("inventario")
    print("Conexión segura establecida con MongoDB Atlas")
except Exception as e:
   
    print("Conexión segura falló, intentando modo escolar...")
try:
    client = MongoClient(
        MONGO_URI,
        tls=True,
        tlsAllowInvalidCertificates=True,
        serverSelectionTimeoutMS=10000
    )
    db = client.get_default_database("inventario")
    print(" Conexión establecida con MongoDB Atlas (modo escolar sin SSL)")
except Exception as e:
    db = None
    print(" No se pudo conectar con MongoDB Atlas:", e)
@app.route("/")
def index():
    items = list(productos.find())
    return render_template("index.html", items=items)

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        nombre = request.form["nombre"]
        precio = float(request.form["precio"])
        cantidad = int(request.form["cantidad"])
        proveedor = request.form["proveedor"]
        descripcion = request.form["descripcion"]
        imagen = request.form["imagen"] or "productos1.jpg"

        if not nombre:
            flash("El nombre del producto es obligatorio.", "danger")
            return redirect(url_for("create"))

        productos.insert_one({
            "nombre": nombre,
            "precio": precio,
            "cantidad": cantidad,
            "proveedor": proveedor,
            "descripcion": descripcion,
            "imagen": imagen
        })
        flash("Producto agregado correctamente.", "success")
        return redirect(url_for("index"))
    return render_template("create.html")

@app.route("/edit/<id>", methods=["GET", "POST"])
def edit(id):
    producto = productos.find_one({"_id": ObjectId(id)})
    if not producto:
        flash("Producto no encontrado.", "danger")
        return redirect(url_for("index"))

    if request.method == "POST":
        nombre = request.form["nombre"]
        precio = float(request.form["precio"])
        cantidad = int(request.form["cantidad"])
        proveedor = request.form["proveedor"]
        descripcion = request.form["descripcion"]
        imagen = request.form["imagen"] or producto.get("imagen")

        productos.update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "nombre": nombre,
                "precio": precio,
                "cantidad": cantidad,
                "proveedor": proveedor,
                "descripcion": descripcion,
                "imagen": imagen
            }}
        )
        flash("Producto actualizado correctamente.", "info")
        return redirect(url_for("index"))

    return render_template("edit.html", producto=producto)

@app.route("/delete/<id>", methods=["POST"])
def delete(id):
    productos.delete_one({"_id": ObjectId(id)})
    flash("Producto eliminado.", "warning")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
