from flask import jsonify

def register_error_handlers(current_app):

    @current_app.errorhandler(429)
    def ratelimit_handler(e):
        return jsonify({
            "error":"ratelimit_exceeded",
            "message": f'Whoa there! You have exceeded your rate limit. {e.description}'
        }), 429