import json
import os
import subprocess

from flask import Flask, render_template, request, redirect, url_for, send_file
from waitress import serve

app = Flask(__name__)


@app.route('/')
def index():
    """
    The homepage. Network graph and data preview.
    """
    global listener
    text = None
    image = None
    if listener is not None:
        # we have some data to preview
        d = listener.getData()
        print(d)
        if d['type'] == 'txt':
            text = d['data'] 
        # TODO handle and implement more types of data
    
    return render_template('index.html',zport=config['zmqservport'], isdebug=config['debug'],text=text,image=image)



# NON-PAGE HELPERS: do other tasks in the program =============================

def loadConfig():
    with open('./src/data/config.json', 'r') as c:
        try:
            config = json.load(c)
        except:
            print('unable to load config. Exiting')
            config = None
    return config


if __name__ == '__main__':
    # Load config

    config = loadConfig()
    version = subprocess.check_output("git describe --tags", shell=True).decode().strip().split('-')[0]

    # start web server
    if config is not None:
        if config['debug']:
            app.run(debug=True, port=config['flaskport'])
        else:
            # This is the 'production' WSGI server
            serve(app, port=config['flaskport'])