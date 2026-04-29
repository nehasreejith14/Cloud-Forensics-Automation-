from flask import Flask, jsonify, send_from_directory, request
import csv
import os
from werkzeug.utils import secure_filename
from main import run_forensic_scan, get_file_details

app = Flask(__name__, static_folder="ui")

# Paths
UPLOAD_FOLDER = 'uploads'
OUTPUT_FILE = "output/evidence_report.csv"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return send_from_directory('ui', 'index.html')

@app.route('/reports')
def reports():
    return send_from_directory('ui', 'reports.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('ui', path)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"success": False, "message": "No file part"})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"success": False, "message": "No selected file"})
    
    if file:
        filename = secure_filename(file.filename)
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(save_path)
        
        # Get details for THIS file specifically
        details = get_file_details(save_path)
        
        # Also run the full scan for the report in background
        run_forensic_scan()
        
        return jsonify({"success": True, "message": "Scanned successfully", "details": details})

@app.route('/api/scan', methods=['POST'])
def scan():
    try:
        run_forensic_scan()
        return jsonify({"success": True, "message": "Forensic report generated successfully."})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

@app.route('/api/data')
def get_data():
    if not os.path.exists(OUTPUT_FILE):
        return jsonify([])
    
    data = []
    try:
        with open(OUTPUT_FILE, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        return jsonify(data)
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

@app.route('/api/download_report')
def download_report():
    if os.path.exists(OUTPUT_FILE):
        return send_from_directory('output', 'evidence_report.csv', as_attachment=True)
    return jsonify({"success": False, "message": "Report not found"}), 404

@app.route('/api/delete_file', methods=['POST'])
def delete_file():
    data = request.json
    filename = data.get('filename')
    filepath = data.get('filepath')
    
    if not filepath or not os.path.exists(filepath):
        return jsonify({"success": False, "message": "File not found"}), 404
    
    try:
        os.remove(filepath)
        # Refresh the report after deletion
        run_forensic_scan()
        return jsonify({"success": True, "message": f"File {filename} deleted successfully"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

@app.route('/api/download_file/<filename>')
def download_file(filename):
    # Check uploads folder
    if os.path.exists(os.path.join(UPLOAD_FOLDER, filename)):
        return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)
    # Check data folder
    elif os.path.exists(os.path.join('data', filename)):
        return send_from_directory('data', filename, as_attachment=True)
    
    return jsonify({"success": False, "message": "File not found"}), 404

if __name__ == '__main__':
    print("Agriculture Forensics Backend starting at http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
