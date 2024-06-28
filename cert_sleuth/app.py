# providing the interface for the user. static site.

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def test():
    return render_template('This is a test! ')

if __name__ == "__main__":
    app.run(debug=True)