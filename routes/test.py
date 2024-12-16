from flask import Blueprint, jsonify

# Crear un Blueprint para el nuevo endpoint
json_endpoint = Blueprint("test", __name__)

@json_endpoint.route("/", methods=["GET"])
def get_json_data():
    """
    Endpoint para devolver un JSON con datos de ejemplo.
    """
    try:
        # Datos que quieres devolver como respuesta
        data = {
            "name": "John Doe",
            "age": 30,
            "city": "New York"
        }

        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
