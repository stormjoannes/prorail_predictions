from flask import Flask, redirect, url_for, render_template, request, session
import datetime as dt
from predictions.main import DecisionTreeRPredict, dtr, rmse, stdv, gemm

app = Flask(__name__)
app.secret_key = "StormIsDik"


@app.route("/", methods=["POST", "GET"])
def home():
    if 'table' not in session:
        session['table'] = []
        return render_template("base.html", table=session['table'], rmse=round(rmse,1))
    else:
        if request.method == "POST":
            pi = int(request.form["pi"])
            date = request.form["datum"].replace('T', " ")
            distance = int(request.form["kmtm"])
            oc = int(request.form["oc"])

            date_values = split_date(['h', 'm'], date)
            features = [pi, distance, oc]

            pred = get_prediction(features, date_values)

            table_dict = {"pred": pred, "pi": pi, "date": date, "distance": distance, "oc": oc}
            add_to_table(table_dict)

            return render_template("base.html", pred=pred, pi=pi, hour=date_values[1], month=date_values[0], distance=distance, oc=oc, rmse=round(rmse, 1), table=session['table'])
        else:
            return render_template("base.html", table=session['table'], rmse=round(rmse,1))


def split_date(timestamps, var):
    if not isinstance(var, dt.datetime):
        date = dt.datetime.strptime(var, "%Y-%m-%d %H:%M")
        values = []
        for i in timestamps:
            if i == "y":
                stamp = date.year
            elif i == "m":
                stamp = date.month
            elif i == "d":
                stamp = date.day
            elif i == "h":
                stamp = date.hour
            else:
                stamp = date.minute

            values.append(stamp)

        return values


def get_prediction(features, date_values):
    all_features = []

    if len(date_values) > 1:
        for i in date_values:
            all_features.append(i)
    else:
        all_features.append(date_values)

    for i in features:
        all_features.append(i)

    pred = DecisionTreeRPredict(dtr, [all_features], stdv, gemm)

    pred = str(pred).lstrip('[').rstrip(']')

    pred = float(pred)

    return round(pred, 1)


def add_to_table(features):
    ti = dict()
    for key, value in features.items():
        ti[key] = value

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

