from flask import Flask, redirect, url_for, render_template, request, session
# from predictions.main import DecisionTreeRPredict, dtr

app = Flask(__name__)
app.secret_key = "StormIsDik"

# features_2 = [[10, 12, 2, 120, 432]]
# DecisionTreeRPredict(dtr, features_2)


@app.route("/", methods=["POST", "GET"])
def home():
    if 'table' not in session:
        session['table'] = []
        return render_template("base.html", table=session['table'])
    else:
        if request.method == "POST":
            distance = request.form["kmtm"]
            date = request.form["datum"]
            pi = request.form["pi"]
            oc = request.form["oc"]

            features = [distance, date, pi, oc]

            return render_template("base.html")
        else:
            return render_template("base.html", table=session['table'])


def add_to_table():
    location = request.args['location']
    time = request.args['time']
    ti = {"location": location, "time": time, "duration": 20}
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
