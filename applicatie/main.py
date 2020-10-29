from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("test.html")

@app.route("/test")
def test():
    return render_template("new.html")
# @app.route("/<name>")
# def user(name):
#     return f"Hello {name}!"
#
# @app.route("/admin/")
# def admin():
#     return redirect(url_for("user", name="Admin"))

if __name__ == "__main__":
    app.run(debug=True)