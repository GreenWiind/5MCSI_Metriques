from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)

@app.route("/contact/")
def contact():
    return render_template("contact.html")

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html') #comm

@app.route("/commits-data/")
def commits_data():
    url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits?per_page=100"

    response = urlopen(url)
    raw_content = response.read()
    commits_json = json.loads(raw_content.decode("utf-8"))

    results = []

    for commit in commits_json:
        date_str = commit.get("commit", {}).get("author", {}).get("date")
        if not date_str:
            continue

        # "2024-02-11T11:57:27Z"
        dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")

        results.append({
            "minute": dt.strftime("%Y-%m-%d %H:%M")
        })

    return jsonify(results=results)
@app.route("/commits/")
def commits():
    return render_template("commits.html")

  
if __name__ == "__main__":
  app.run(debug=True)
