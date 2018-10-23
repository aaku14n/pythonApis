from flask import jsonify
def partialResponse(message):
    return jsonify({"status":304,"message":message})

def successResponse(message):
    return jsonify({'status':200,'message':message})