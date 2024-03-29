from flask import Flask, render_template, url_for, request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///prueba.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    tarea = db.Column(db.String(200), nullable = False)
    completada = db.Column(db.Integer, default = 0)
    fecha = db.Column(db.DateTime, default = datetime.utcnow)

    def __resp__(self):
        return '<Tareas %r>' % self.id

@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
       tarea = request.form['tarea'] 
       nueva_tarea = Todo(tarea = tarea)
       try:
           db.session.add(nueva_tarea)
           db.session.commit()
           return redirect('/')
       except:
            return 'Ocurrio un error al agregar la tarea'
    else:
        tareas = Todo.query.order_by(Todo.fecha).all()
        return render_template('index.html', tareas = tareas)


@app.route('/borrar/<int:id>')
def borrar(id):
    tarea_a_eliminar = Todo.query.get_or_404(id)
    db.session.delete(tarea_a_eliminar)
    db.session.commit()
    return redirect('/')

@app.route('/actualizar/<int:id>')
def actualizar(id):
    tarea = Todo.query.get_or_404(id)
    if request.method == 'POST':
        pass
    else:
        return render_template('actualizar.html', tarea = tarea)
    
    



if __name__ == "__main__":
    app.run(debug=True)
