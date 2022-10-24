from flask import Flask, render_template, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import os
from celery import Celery


UPLOAD_FOLDER = './users_files'
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testdb.sqlite3'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.update(CELERY_CONFIG={
    'broker_url': 'redis://172.18.0.2:6379/0',
    'result_backend': 'redis://172.18.0.2:6379/0',
})
db = SQLAlchemy(app)


celery = Celery(
    __name__,
    broker="redis://172.18.0.2:6379/0",
    backend="redis://172.18.0.2:6379/0"
)


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    link = db.Column(db.String(150), unique=True)
    file_path = db.Column(db.String(150), unique=True)


@app.route('/', methods=["POST", "GET"])
def home():
    if request.method == 'POST':
        file = request.files['files']
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
    # celery.send_task('tasks.longtime_add', kwargs={'x': 1, 'y': 2})
    return render_template('index.html')


@app.route('/files/<filename>')
def load_file(filename):
    print(filename)
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               path=filename,
                               as_attachment=True
                               )


if __name__ == '__main__':
    app.run()


