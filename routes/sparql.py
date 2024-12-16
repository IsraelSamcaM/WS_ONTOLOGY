from flask import Blueprint, request, jsonify
from config import g # Importamos el grafo desde config.py

# Crear un Blueprint para el endpoint SPARQL
sparql_endpoint = Blueprint("sparql", __name__)

@sparql_endpoint.route("/", methods=["POST"])
def handle_sparql():
    """
    Endpoint para ejecutar consultas SPARQL genéricas.
    """
    try:
        # Obtener la consulta SPARQL
        query = request.json.get("query", "").strip()
        if not query:
            return jsonify({"error": "SPARQL query is required"}), 400

        # Ejecutar la consulta
        results = g.query(query)

        # Formatear los resultados
        output = []
        for row in results:
            result_dict = {str(var): str(row[var]) for var in results.vars}
            output.append(result_dict)

        return jsonify({"results": output})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
