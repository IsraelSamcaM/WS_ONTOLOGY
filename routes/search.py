# search_endpoint.py
from flask import Blueprint, request, jsonify
from config import g, query_dbpedia  # Importamos el grafo y la función de consulta a DBpedia
from googletrans import Translator  # Librería para traducción automática

# Crear un Blueprint para el endpoint Search
semantic_search = Blueprint("search", __name__)

# Instanciar el traductor
translator = Translator()

# Diccionario para mapear los códigos de idioma
LANGUAGE_MAP = {
    "1": "es",  # Español
    "2": "en",  # Inglés
    "3": "fr",  # Francés
    "4": "pt"   # Portugués
}

@semantic_search.route("/<string:term>/<string:language>", methods=["GET"])  # Añadir idioma como parámetro
def handle_search(term, language):
    """
    Endpoint para buscar un término semántico en la ontología local y DBpedia con soporte multilingüe.
    """
    try:
        # Validar el término de búsqueda
        search_term = term.strip()
        if not search_term:
            return jsonify({"error": "Search term is required"}), 400

        # Validar el idioma
        target_language = LANGUAGE_MAP.get(language)
        if not target_language:
            return jsonify({"error": "Invalid language code"}), 400

        # Crear la consulta SPARQL para la ontología local
        local_query = f"""
        SELECT ?subject ?label ?comment ?type ?predicate ?object
        WHERE {{
            {{
                ?subject rdfs:label ?label . 
                FILTER(CONTAINS(LCASE(?label), LCASE("{search_term}"))).
            }} UNION {{
                ?subject ?predicate ?object . 
                FILTER(CONTAINS(LCASE(STR(?object)), LCASE("{search_term}"))).
            }}
            OPTIONAL {{
                ?subject rdfs:comment ?comment . 
            }}
            OPTIONAL {{
                ?subject rdf:type ?type . 
            }}
        }}
        LIMIT 20
        """

        # Ejecutar la consulta en la ontología local
        local_results = g.query(local_query)
        local_output = []
        for row in local_results:
            label = str(row["label"]) if row.get("label") else str(row["object"]) if row.get("object") else None
            comment = str(row["comment"]) if row.get("comment") else None

            # Traducir `label` y `comment` al idioma solicitado
            label_translated = translator.translate(label, src="en", dest=target_language).text if label else None
            comment_translated = translator.translate(comment, src="en", dest=target_language).text if comment else None

            local_output.append({
                "subject": str(row["subject"]),
                "label": label_translated,
                "comment": comment_translated,
                "type": str(row["type"]) if row.get("type") else None,
                "predicate": str(row["predicate"]) if row.get("predicate") else None,
                "object": str(row["object"]) if row.get("object") else None
            })

        # Consultar a DBpedia y traducir los resultados
        dbpedia_results = query_dbpedia(search_term)
        translated_dbpedia_results = []
        for result in dbpedia_results:
            translated_dbpedia_results.append({
                "subject": result["subject"],
                "label": translator.translate(result["label"], src="en", dest=target_language).text if result.get("label") else None,
                "comment": translator.translate(result["comment"], src="en", dest=target_language).text if result.get("comment") else None,
                "type": result["type"]
            })

        # Combinar resultados y retornarlos
        return jsonify({
            "local_results": local_output,
            "dbpedia_results": translated_dbpedia_results
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
