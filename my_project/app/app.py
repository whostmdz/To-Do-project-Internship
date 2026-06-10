import os
from datetime import datetime
from prometheus_client import Gauge
from flask import *

from flask_sqlalchemy import SQLAlchemy


# Création de l'application Flask
app = Flask(__name__)

from prometheus_flask_exporter import PrometheusMetrics
metrics = PrometheusMetrics(app)
tasks_gauge = Gauge('todo_tasks_total', 'Nombre de taches dans la base de données')
# Configuration de la base de données
database_url = os.environ.get("DATABASE_URL")

if database_url:
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# Création de l'objet base de données
db = SQLAlchemy(app)


# Modèle Todo = une tâche dans la base de données
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(200), nullable=False)
    fait = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# Création des tables dans la base de données
with app.app_context():
    db.create_all()


# Page principale
@app.route("/")
def index():
    filtre = request.args.get("filtre")

    if filtre is None:
        filtre = "toutes"

    if filtre == "actives":
        todos = Todo.query.filter_by(fait=False).order_by(Todo.created_at.desc()).all()
    elif filtre == "terminees":
        todos = Todo.query.filter_by(fait=True).order_by(Todo.created_at.desc()).all()
    else:
        todos = Todo.query.order_by(Todo.created_at.desc()).all()

    total = Todo.query.count()
    terminees = Todo.query.filter_by(fait=True).count()
    tasks_gauge.set(Todo.query.count())
    return render_template(
        "index.html",
        todos=todos,
        filtre=filtre,
        total=total,
        terminees=terminees
    )


# Ajouter une tâche
@app.route("/ajouter", methods=["POST"])
def ajouter():
    titre = request.form.get("titre")

    if titre is not None:
        titre = titre.strip()

        if titre != "":
            nouvelle_tache = Todo()
            nouvelle_tache.titre = titre
            nouvelle_tache.fait = False

            db.session.add(nouvelle_tache)
            db.session.commit()

    return redirect(url_for("index"))


# Marquer une tâche comme terminée ou non terminée
@app.route("/terminer/<int:id>")
def terminer(id):
    todo = Todo.query.get_or_404(id)

    if todo.fait == True:
        todo.fait = False
    else:
        todo.fait = True

    db.session.commit()

    return redirect(url_for("index"))


# Supprimer une tâche
@app.route("/supprimer/<int:id>")
def supprimer(id):
    todo = Todo.query.get_or_404(id)

    db.session.delete(todo)
    db.session.commit()

    return redirect(url_for("index"))


# Supprimer toutes les tâches terminées
@app.route("/supprimer-terminees")
def supprimer_terminees():
    todos_termines = Todo.query.filter_by(fait=True).all()

    for todo in todos_termines:
        db.session.delete(todo)

    db.session.commit()

    return redirect(url_for("index"))


# Lancement de l'application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
