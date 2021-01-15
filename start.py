from flask import Flask, request, send_file
import io
import walksat
from api_pb2 import Cnf

app = Flask(__name__)

if __name__ == "__main__":

    @app.route('/', methods=['GET', 'POST'])
    def post():
        cnf = Cnf()
        cnf.ParseFromString(request.data)
        solution = walksat.ok(cnf=cnf)
        return send_file(
            io.BytesIO(solution.SerializeToString()),
            as_attachment=True,
            attachment_filename='abc.abc',
            mimetype='attachment/x-protobuf'
        )

    app.run(host='0.0.0.0', port=8080)