from flask import Flask, request
import walksat

app = Flask(__name__)

if __name__ == "__main__":

    @app.route('/', methods=['GET', 'POST'])
    def post():
        cnf = request.json.get('cnf')
        solution = walksat.ok(cnf=cnf)
        return {'interpretation':solution}

    app.run(host='0.0.0.0', port=8080)