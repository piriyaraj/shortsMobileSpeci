from distutils.log import debug
import os
from flask import Flask, render_template
from threading import Thread
import main
app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/postvideo')
def postvideo():
    thread_a = Thread(target=main.run, args=())
    thread_a.start()
    return render_template("timepage.html", title="start uploading")


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)