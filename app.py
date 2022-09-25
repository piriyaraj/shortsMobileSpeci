import os
from flask import Flask
import main
app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/postvideo')
def postvideo():
    main.run()


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)