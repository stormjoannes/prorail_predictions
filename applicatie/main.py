from flask import Flask, redirect, url_for, render_template, request, session

app = Flask(__name__)
app.secret_key = "StormIsDik"

@app.route("/", methods= ["POST", "GET"])
def home():
    if 'table' not in session:
        session['table'] = []
        return render_template("base.html", table=session['table'])
    else:
        if request.method == "POST":
            table_location = request.form["locatie"]
            table_time = request.form["tijd"]
            # table_item = [table_location, table_time]
            return redirect(url_for("add_to_table", time=table_time, location=table_location))
        else:
            return render_template("base.html", table=session['table'])

@app.route("/table")
def add_to_table():
    location = request.args['location']
    time = request.args['time']
    ti = [location, time]
    if "table" in session:
        new_array = session['table']
        if ti is not None:
            new_array.append(ti)
        session['table'] = new_array
        return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
