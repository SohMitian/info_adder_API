from flask import Flask, request, send_file
from flask_cors import CORS
import proc_gml as AI

app = Flask(__name__)
CORS(app)

@app.route("/gml", methods=['POST'])
def add_info():
  if request.method == 'POST':
    # POSTされたデータ
    gml_data = request.files['file']
    # データのファイル名
    file_name = gml_data.filename
    
    out_file_name = AI.add_info_gml(gml_data, file_name)

    download_file = out_file_name
    MIMETYPE = 'application/octet-stream'
    return send_file(download_file, as_attachment=True,
                     download_name=out_file_name,
                     mimetype=MIMETYPE)
  else: 
    return 'Not POST'

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='8888')