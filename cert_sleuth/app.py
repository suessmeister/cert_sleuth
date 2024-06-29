# providing the interface for the user. static site.

from methods import start_time, end_time, alive_sites
from flask import Flask, render_template, url_for



app = Flask(__name__, static_url_path='/static')

@app.route("/")
def test():

    return render_template('index.html', start=start_time, end=end_time)

if __name__ == "__main__":
    app.run(debug=True)