from flask import Flask, redirect, url_for, render_template, request, session
import datetime as dt
import pandas as pd
from predictions.main import DecisionTreeRPredict,  dtr, rmse, stdv, gemm

app = Flask(__name__)
app.secret_key = "prorail_predictions"

# oorzaakcodes die we nodig hebben voor een dropdown menu..werkt wegens een parsererror niet met onze readfile func dus doen we het zo
oc_codes = pd.read_table('../files/Oorzaakcodes.csv')


@app.route("/", methods=["POST", "GET"])
def home():
    # geen table in session..maak het
    if 'table' not in session:
        session['table'] = []
        return render_template("base.html", table=session['table'], rmse=round(rmse, 1), oc_codes=oc_codes)
    else:
        # als je een voorspelling maakt en de features stuurt
        if request.method == "POST":
            # vorm inputs individueel ophalen om makkelijker individueel te tonen
            pi = int(request.form["pi"])
            date = request.form["datum"].replace('T', " ")
            distance = int(request.form["kmtm"])
            oc = int(request.form["oc"])

            # voor het model gebruiken we een functie die de datum opsplits in wat we willen
            # timestamps aangeven met kleiner letter (y,m,d,h,m)..geen seconde want die krijg je niet
            date_values = split_date(['h', 'm'], date)
            features = [pi, distance, oc]

            pred, trust = get_prediction(features, date_values)

            # table dict en add to tables is voor de visualisatie
            table_dict = {"pred": pred, "pi": pi, "date": date, "distance": distance, "oc": oc}
            add_to_table(table_dict)

            # dit doen we om alles te tonen bij de duur zoals de betrouwbaarheid, rmse en features
            return render_template("base.html", pred=pred, pi=pi, hour=date_values[0], month=date_values[1],
                                   distance=distance, oc=oc, rmse=round(rmse, 1), trust=trust,  table=session['table'],
                                   oc_codes=oc_codes)
        else:
            return render_template("base.html", table=session['table'], rmse=round(rmse, 1), oc_codes=oc_codes)


def split_date(timestamps, var):
    if not isinstance(var, dt.datetime):
        date = dt.datetime.strptime(var, "%Y-%m-%d %H:%M")
        values = []
        # eigenlijk een switch case
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
    # we hoeven er niet door te lopen als het er maar 1 is
    if len(date_values) > 1:
        for i in date_values:
            all_features.append(i)
    else:
        all_features.append(date_values)

    for i in features:
        all_features.append(i)

    # we maken hier gebruik van de predict func in de backend
    pred, trust = DecisionTreeRPredict(dtr, [all_features], stdv, gemm)

    # irritante blokhaken weghalen
    pred, trust = str(pred).lstrip('[').rstrip(']'), str(trust).lstrip('[').rstrip(']')

    # converten naar floats zodat we ze kunnen afronden
    pred, trust = float(pred), float(trust)

    return round(pred, 1), round(trust, 1)


def add_to_table(features):
    # we maken een nieuwe dictonary die alle zal bevatten, maar ook een index
    ti = dict()
    for key, value in features.items():
        ti[key] = value

    if "table" in session:
        new_array = session['table']
        # de index begint bij 1 maar als een lijst niks heeft zou de eerste item 0 als index hebben, daarom len + 1
        index = len(new_array) + 1
        if ti is not None:
            ti['index'] = index
            new_array.append(ti)
        session['table'] = new_array
        return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))


@app.route("/delete", methods=["POST", "GET"])
def delete_table():
    if request.method == "POST":
        index = request.form['index']
        current_list = session['table']
        for i in current_list:
            # zoek naar de index in current list als je die hebt pak je de index die in de array staat en delete je deze
            if i['index'] == int(index):
                arr_index = current_list.index(i)

        del current_list[arr_index]

        session['table'] = current_list

        return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)

