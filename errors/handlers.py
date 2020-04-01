from main import app,jsonify

# bad request
@app.errorhandler(400)
def bad_request(e):
    # note that we set the 400 status explicitly
    return jsonify({"message":"server cannot or will not process the request due to an apparent client error"}), 400

# unauthorized
@app.errorhandler(401)
def unauthorized(e):
    return jsonify({"message":"unauthorized"}), 401

# forbidden
@app.errorhandler(403)
def forbidden(e):
    return jsonify({"message":"Forbidden"}), 403

# resource not found
@app.errorhandler(404)
def resource_not_found(e):
    # note that we set the 404 status explicitly
    return jsonify({"message":"requested resource cannot be found"}), 404


# method not allowes
@app.errorhandler(405)
def bad_request(e):
    # note that we set the 400 status explicitly
    return jsonify({"message":"The request method is not supported for the requested resource"}), 405


# internal server error
@app.errorhandler(500)
def internal_server_error(e):
    # note that we set the 404 status explicitly
    return jsonify({"message":"There was a problem with the server"}), 500