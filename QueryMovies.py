from SPARQLWrapper import SPARQLWrapper, JSON
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Define the HTML template for the web page
html_template = '''
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>SPARQL Query</title>
  </head>
  <body>
    <h1>SPARQL Query</h1>
    <form method="POST">
      <label for="query">Enter your SPARQL query:</label><br>
      <textarea id="query" name="query" rows="10" cols="100"></textarea><br>
      <input type="submit" value="Submit">
    </form>
    {% if result %}
      <h2>Result:</h2>
      {{ result|safe }}
    {% endif %}
  </body>
</html>
'''

# Define the function that will run the SPARQL query
def run_query(query):
    # Set up the SPARQL endpoint
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    # Execute the query and get the results
    results = sparql.query().convert()
    # Parse the results and format them as an HTML table
    rows = []
    for result in results["results"]["bindings"]:
        row = []
        for key in result.keys():
            row.append(result[key]["value"])
        rows.append(row)
    headers = results["results"]["bindings"][0].keys()
    table_html = '<table border="1"><thead><tr>'
    for header in headers:
        table_html += "<th>" + header + "</th>"
    table_html += "</tr></thead><tbody>"
    for row in rows:
        table_html += "<tr>"
        for item in row:
            table_html += "<td>" + item + "</td>"
        table_html += "</tr>"
    table_html += "</tbody></table>"
    return table_html

# Define the function that will handle requests to the web page
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # If a query was submitted, run it and display the results
        query = request.form.get("query")
        result = run_query(query)
        return render_template_string(html_template, result=result)
    else:
        # If no query was submitted, display the form
        return render_template_string(html_template)

if __name__ == "__main__":
    app.run(debug=True)
