# providing the interface for the user. static site.

import cfg
from flask import Flask, render_template, url_for
from driver import main


app = Flask(__name__, static_url_path='/static')


# Because app.before first request is deprecated :(
with app.app_context():
    main()

@app.route("/")
def test():
    return render_template('index.html', start=cfg.start_time, end=cfg.end_time, sites=cfg.alive_sites)


if __name__ == "__main__":
    app.run(debug=False)