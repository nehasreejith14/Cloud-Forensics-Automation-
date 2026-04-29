import os
import csv
import hashlib
from datetime import datetime

# Folders to scan
scan_folders = ["data", "uploads"]

# Output file
output_file = "output/evidence_report.csv"

def get_file_hash(file_path):
    """Calculate SHA256 hash of a file."""
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception:
        return "ERROR"

def get_file_details(file_path):
    """Get metadata for a single file."""
    if not os.path.exists(file_path):
        return None
    
    # Get timestamps
    created_time = datetime.fromtimestamp(os.path.getctime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
    modified_time = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
    
    # Get SHA256 Hash
    file_hash = get_file_hash(file_path)
    
    return {
        "File Name": os.path.basename(file_path),
        "File Path": file_path,
        "Created Time": created_time,
        "Last Modified Time": modified_time,
        "SHA256 Hash": file_hash
    }

def run_forensic_scan():
    # Create output folder if not exists
    os.makedirs("output", exist_ok=True)

    all_files = []

    # Scan directories
    for folder in scan_folders:
        if not os.path.exists(folder):
            continue
            
        print(f"Scanning directory: {folder}...")
        for root, dirs, files in os.walk(folder):
            for f in files:
                file_path = os.path.join(root, f)

                # Get details
                created_time = datetime.fromtimestamp(os.path.getctime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
                modified_time = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
                file_hash = get_file_hash(file_path)

                all_files.append({
                    "name": f,
                    "path": file_path,
                    "created": created_time,
                    "modified": modified_time,
                    "hash": file_hash,
                    "mtime_raw": os.path.getmtime(file_path) # Store raw mtime for sorting
                })

    # Sort files by modification time descending (most recent first)
    all_files.sort(key=lambda x: x["mtime_raw"], reverse=True)

    # Open CSV file and perform scan
    with open(output_file, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Write header
        writer.writerow(["File Name", "File Path", "Created Time", "Last Modified Time", "SHA256 Hash"])

        for file_info in all_files:
            writer.writerow([
                file_info["name"],
                file_info["path"],
                file_info["created"],
                file_info["modified"],
                file_info["hash"]
            ])

    print(f"Evidence report generated successfully with {len(all_files)} files!")
    return output_file

if __name__ == "__main__":
    run_forensic_scan()
