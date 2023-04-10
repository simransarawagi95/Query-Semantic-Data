from SPARQLWrapper import SPARQLWrapper, JSON
import webbrowser
endpoint_url = "http://dbpedia.org/sparql"
sparql = SPARQLWrapper(endpoint_url)

# take input from user
# search_term = input("Enter search term: ")

# create a SPARQL query using the input
sparql_query = """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

select REPLACE(str(?moviename),'"','') AS ?movietitle, REPLACE(str(?directorname),'"','') AS ?directortitle,
(GROUP_CONCAT(?actorname; separator=", ") as ?starcast), ?releaseDate
where {
?movie rdf:type dbo:Film.
?movie rdfs:label ?moviename.
?movie dbo:director ?director.
?director foaf:name ?directorname.
?movie dbo:starring ?actors.
?actors foaf:name ?actorname.
?movie dbp:releaseDate ?releaseDate.
FILTER((lang(?moviename)="en") && (lang(?directorname)="en")).
} GROUP BY ?moviename ?releaseDate ?directorname 
ORDER BY ?releaseDate 
LIMIT 10
""" 
# % search_term FILTER((?releaseDate <= %s))
# sparql.setQuery("""
# PREFIX dbo: <http://dbpedia.org/ontology/>
# PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
# PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

# select REPLACE(str(?moviename),'"','') AS ?movietitle, REPLACE(str(?directorname),'"','') AS ?directortitle,
# (GROUP_CONCAT(?actorname; separator=", ") as ?starcast), ?releaseDate
# where {
# ?movie rdf:type dbo:Film.
# ?movie rdfs:label ?moviename.
# ?movie dbo:director ?director.
# ?director foaf:name ?directorname.
# ?movie dbo:starring ?actors.
# ?actors foaf:name ?actorname.
# ?movie dbp:releaseDate ?releaseDate.
# FILTER((lang(?moviename)="en") && (lang(?directorname)="en")).
# FILTER((?releaseDate>={})
# } GROUP BY ?moviename ?releaseDate ?directorname 
# ORDER BY ?releaseDate 
# LIMIT 10
# """)

sparql.setQuery(sparql_query)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
# for result in results["results"]["bindings"]:
#     print(result["Concept"]["value"])

# Format the results as an HTML table
table = "<table style='border-collapse: collapse; width: 100%;'>\n"
table += "<tr style='background-color: #eee;'><th style='border: 1px solid black; padding: 5px;'>Movie</th>"
table += "<th style='border: 1px solid black; padding: 5px;'>Director</th>"
table += "<th style='border: 1px solid black; padding: 5px;'>Star Cast</th>"
table += "<th style='border: 1px solid black; padding: 5px;'>Release Date</th></tr>\n"
# table = "<table><tr><th>Movie</th><th>Director</th><th>Star Cast</th><th>Release Date</th></tr>"
for result in results["results"]["bindings"]:
    title = result["movietitle"]["value"]
    director = result["directortitle"]["value"]
    star = result["starcast"]["value"]
    date = result["releaseDate"]["value"]
    table += "<tr><td style='border: 1px solid black; padding: 5px;'>%s</td>" % title
    table += "<td style='border: 1px solid black; padding: 5px;'>%s</td>" % director
    table += "<td style='border: 1px solid black; padding: 5px;'>%s</td>" % star
    table += "<td style='border: 1px solid black; padding: 5px;'>%s</td></tr>\n" % date
    # table += f"<tr><td>{title}</td><td>{director}</td><td>{star}</td><td>{date}</td></tr>"
table += "</table>"

# Write the HTML file and open it in a web browser
with open("movies.html", "w") as f:
    f.write(table)
webbrowser.open("movies.html")
