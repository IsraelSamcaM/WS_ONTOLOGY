from rdflib import Graph
from SPARQLWrapper import SPARQLWrapper, JSON

#conexion a el archivo .owl de nuestra ontology 
ONT_FILE = "computadora.owl"
g = Graph()
g.parse(ONT_FILE, format="xml")

# Configuración para DBpedia SPARQL Endpoint
DBPEDIA_SPARQL_ENDPOINT = "http://dbpedia.org/sparql"
dbpedia = SPARQLWrapper(DBPEDIA_SPARQL_ENDPOINT)

def query_dbpedia(search_term):
    """
    Consulta a DBpedia con un término de búsqueda.
    """
    query = f"""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX dbo: <http://dbpedia.org/ontology/>

    SELECT ?subject ?label ?comment ?type WHERE {{
        {{
            ?subject rdfs:label ?label .
            FILTER(CONTAINS(LCASE(?label), LCASE("{search_term}")))
        }}
        OPTIONAL {{
            ?subject rdfs:comment ?comment .
        }}
        OPTIONAL {{
            ?subject rdf:type ?type .
        }}
        FILTER (lang(?label) = "en" && (lang(?comment) = "en" || !bound(?comment)))
    }}
    LIMIT 20
    """
    
    dbpedia.setQuery(query)
    dbpedia.setReturnFormat(JSON)
    results = dbpedia.query().convert()

    output = []
    for result in results["results"]["bindings"]:
        output.append({
            "subject": result["subject"]["value"],
            "label": result["label"]["value"],
            "comment": result.get("comment", {}).get("value"),
            "type": result.get("type", {}).get("value"),
        })
    return output