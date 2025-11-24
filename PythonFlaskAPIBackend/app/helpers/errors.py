from flask import jsonify

def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'error': 'Not found', 'message': str(e)}), 404

    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({'error': 'Bad request', 'message': str(e)}), 400

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500

    @app.errorhandler(403)
    def forbidden(e):
        # Commonly browsers return CORS related failures as blocked requests.
        # Provide a clear JSON response for explicit 403 responses from the server.
        return jsonify({'error': 'Forbidden', 'message': str(e)}), 403