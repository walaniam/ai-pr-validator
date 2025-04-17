import logging
from flask import Flask, jsonify, request

app = Flask(__name__)
# Set up logging
app.logger.setLevel(logging.DEBUG)

@app.route('/rest/api/2/issue/PROJ-100')
def get_ticket100():
    app.logger.debug("Returning jira ticket PROJ-100")
    return jsonify({
        "fields": {
            "summary": "Implement login page",
            "description": "Create a login form with username and password. It should call /api/login. Show error messages on failure."
        }
    })

@app.route('/rest/api/2/issue/PROJ-101')
def get_ticket101():
    app.logger.debug("Returning jira ticket PROJ-101")
    return jsonify({
        "fields": {
            "summary": "Implement logout action",
            "description": "Create a logout button on a page header. It should call /api/logout. Redirect to home page on failure."
        }
    })

@app.route('/testorg/testrepo/pulls/1')
def get_github_pr():
    accept_header = request.headers.get('Accept')
    if accept_header == 'application/vnd.github.v3.diff':
        app.logger.debug("Returning github diff")
        diff = """
diff --git a/pom.xml b/pom.xml
index 47c1134..42a1b05 100321
--- a/pom.xml
+++ b/pom.xml
@@ -4,6 +4,8 @@
     xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
     <modelVersion>4.0.0</modelVersion>
 
+    <!-- just to raise a PR -->
+
     <groupId>com.test</groupId>
     <artifactId>login-component</artifactId>
     <version>0.0.1-SNAPSHOT</version>
@@ -66,4 +68,4 @@
         </plugins>
     </build>
 
-</project>
\ No newline at end of file
+</project>
"""
        return diff
    elif accept_header == 'application/vnd.github+json':
        app.logger.debug("Returning github json details")
        return jsonify({
            "title": "Implement login page"
        })
    else:
        return 'Bad Request', 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
