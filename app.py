import os
from flask import Flask, render_template, request, redirect, url_for , request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# CONFIGURACIÓN MySQL (phpMyAdmin)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL",
    "mysql+pymysql://root:@localhost/flask_db"  # fallback local
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# MODELO
class Denuncia(db.Model):
    __tablename__ = 'denuncia'  # nombre exacto de la tabla

    num_control = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fecha = db.Column(db.String(10), nullable=False)
    denuncia = db.Column(db.Text, nullable=False)
    ubicacion = db.Column(db.String(100), nullable=False)


# CREAR TABLAS
with app.app_context():
    db.create_all()

# ---------------- RUTAS ---------------- #

@app.route('/')
def carga():
    return render_template('carga.html')

@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']

        nueva = Denuncia(titulo=titulo, descripcion=descripcion)
        db.session.add(nueva)
        db.session.commit()

        return redirect(url_for('formulario'))

    denuncias = Denuncia.query.all()
    return render_template('formulario.html', denuncias=denuncias)

@app.route('/conceptos')
def conceptos():
    return render_template('conceptos.html')

@app.route("/emu", methods=["GET"])
def emu():
    return render_template("emu.html")

@app.route('/denuncias')
def denuncias():
    denuncias = Denuncia.query.all()
    return render_template('denuncias.html', denuncias=denuncias)


@app.route('/juego')
def juego():
    return render_template('juegodid.html')

@app.route("/contra", methods=["GET", "POST"])
def contra():
    if request.method == "POST":
        password = request.form.get("password")

        if password == "DOCNTA":
            return redirect(url_for("emu"))
        else:
            return render_template("contra.html", error=True)

    return render_template("contra.html", error=False)

@app.route("/version")
def version():
    return render_template("version.html")


# ---------------- EJECUCIÓN ---------------- #
if __name__ == '__main__':
    app.run(debug=True)


