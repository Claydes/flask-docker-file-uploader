from flask import Flask, render_template, request, send_from_directory
import os
from mongo_client import MongoClient

UPLOAD_FOLDER = './users_files'
app = Flask(__name__)


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = MongoClient()


def generate_link(file_id: int) -> str:
    return f"{file_id}-kappa"


@app.route('/', methods=["POST", "GET"])
def home():
    if request.method == 'POST':
        file = request.files['files']
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        print(db.find_last_doc_id())
        file_id = db.find_last_doc_id() + 1
        link = generate_link(file_id)
        db.insert(file_id, link, file.filename)
        file.save(file_path)
        return render_template('index.html', file_link=link)
    return render_template('index.html')


@app.route('/files/<link>')
def load_file(link):
    file_path = db.find_path(link)

    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               path=file_path,
                               as_attachment=True
                               )


if __name__ == '__main__':
    app.run(host='0.0.0.0')


