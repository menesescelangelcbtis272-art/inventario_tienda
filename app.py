from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET", "clave_secreta")

client = MongoClient("mongodb+srv://menesescelangelcbtis272_db_user:admin1243@inventario.daylvqt.mongodb.net/")
db = client.inventario
productos = db.productos

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
