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
    api_url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits?per_page=100"

    req = Request(
        api_url,
        headers={
            "User-Agent": "montoute-metrics-app",
            "Accept": "application/vnd.github+json"
        }
    )

    try:
        with urlopen(req) as response:
            raw = response.read().decode("utf-8")
            commits_json = json.loads(raw)

    except HTTPError as e:
        # ex: 403, 429...
        return jsonify({"error": f"HTTPError {e.code}", "results": []}), 200
    except URLError as e:
        return jsonify({"error": f"URLError {str(e)}", "results": []}), 200
    except Exception as e:
        return jsonify({"error": f"Exception: {str(e)}", "results": []}), 200

    # Si GitHub renvoie une erreur (dict), pas une liste
    if isinstance(commits_json, dict):
        msg = commits_json.get("message", "Erreur GitHub inconnue")
        return jsonify({"error": msg, "results": []}), 200

    counter = {}

    for c in commits_json:
        date_str = c.get("commit", {}).get("author", {}).get("date")
        if not date_str:
            continue

        dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        key = dt.strftime("%Y-%m-%d %H:%M")
        counter[key] = counter.get(key, 0) + 1

    results = [{"minute": k, "count": counter[k]} for k in sorted(counter.keys())]
    return jsonify({"error": None, "results": results})

  
if __name__ == "__main__":
  app.run(debug=True)
