from flask import Flask, jsonify
import sys

app = Flask(__name__)

@app.route('/rest/api/3/issue/PROJ-123')
def get_ticket():
    sys.stdout.write("Returning jira ticket\n")
    return jsonify({
        "summary": "Implement login page",
        "acceptance_criteria": "Create a login form with username and password. It should call /api/login. Show error messages on failure."
    })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
