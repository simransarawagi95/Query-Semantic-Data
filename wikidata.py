from SPARQLWrapper import SPARQLWrapper, JSON
import webbrowser
endpoint_url = "https://query.wikidata.org/sparql"
sparql = SPARQLWrapper(endpoint_url)

# take input from user
#search_term = input("Enter your query: ")

# create a SPARQL query using the input
sparql_query = """
SELECT DISTINCT ?movieLabel (GROUP_CONCAT(DISTINCT ?actorname; separator=", ") AS ?cast) 
WHERE {
  ?movie wdt:P31 wd:Q11424.
  ?movie wdt:P57 wd:Q25191.
  ?movie wdt:P1657 wd:Q18665339.
  ?movie wdt:P161 ?actors.
   SERVICE wikibase:label {
    bd:serviceParam wikibase:language "en".
    ?movie rdfs:label ?movieLabel.
     ?actors rdfs:label ?actorname.
  }
  }GROUP BY ?movieLabel

""" 


sparql.setQuery(sparql_query)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

# Format the results as an HTML table
table = "<table style='border-collapse: collapse; width: 100%;'>\n"
table += "<tr style='background-color: #eee;'><th style='border: 1px solid black; padding: 5px;'>Movie</th>"
table += "<th style='border: 1px solid black; padding: 5px;'>Star Cast</th>\n"
for result in results["results"]["bindings"]:
    title = result["movieLabel"]["value"]
    star = result["cast"]["value"]
    table += "<tr><td style='border: 1px solid black; padding: 5px;'>%s</td>" % title
    table += "<td style='border: 1px solid black; padding: 5px;'>%s</td>\n" % star
table += "</table>"

# Write the HTML file and open it in a web browser
with open("movies.html", "w") as f:
    f.write(table)
webbrowser.open("movies.html")
