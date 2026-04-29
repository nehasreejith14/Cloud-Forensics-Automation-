================================================================
🌱 CLOUD FORENSICS AUTOMATION FOR AGRICULTURE BREACHES
================================================================

This project provides an automated tool for collecting file 
evidence in agriculture-related data systems. It scans directory 
metadata and calculates SHA256 hashes to ensure data integrity.

STRUCTURE:
- app.py                : Flask web server (Backend)
- main.py               : Forensic scanning logic (Python)
- data/                 : Sample agricultural data files
- output/               : Generated forensic reports (CSV)
- ui/                   : Dashboard interface (HTML/CSS)

HOW TO RUN:
1. Open terminal in the project folder.
2. Run the backend:
   python app.py
3. Open your browser and go to:
   http://127.0.0.1:5000
4. Click "Run Forensic Scan" to generate the report and view results.

SECURITY FEATURES:
- SHA256 Hashing: Detects if file contents have been tampered with.
- Timestamp Analysis: Tracks creation and modification times.
- Automated Reporting: Generates a secure CSV audit trail.

Developed for agricultural security and digital forensics analysis.
================================================================
