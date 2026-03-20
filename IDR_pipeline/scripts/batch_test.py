import boto3
import base64
import json
import os
import time
import requests
from datetime import datetime

API_ENDPOINT = "https://0r8p6ap199.execute-api.us-east-1.amazonaws.com/prod"
DOCS_DIR = "test-documents/mock_documents"

results = {
    "passed": [],
    "failed": [],
    "errors": []
}

files = [f for f in os.listdir(DOCS_DIR) if f.endswith('.pdf')]
total = len(files)

print(f"Starting batch test — {total} documents")
print(f"Started at: {datetime.now().strftime('%H:%M:%S')}\n")

for i, filename in enumerate(files, 1):
    filepath = os.path.join(DOCS_DIR, filename)
    
    try:
        # Encode
        with open(filepath, 'rb') as f:
            encoded = base64.b64encode(f.read()).decode()
        
        # Upload
        upload_response = requests.post(
            f"{API_ENDPOINT}/upload",
            json={"fileName": filename, "fileContent": encoded, "contentType": "application/pdf"}
        )
        
        if upload_response.status_code != 200:
            results["failed"].append({"file": filename, "reason": "upload failed", "status": upload_response.status_code})
            print(f"[{i}/{total}] ❌ UPLOAD FAILED — {filename}")
            continue
        
        doc_id = upload_response.json()["documentId"]
        
        # Poll for results — max 30 seconds
        for attempt in range(6):
            time.sleep(5)
            results_response = requests.get(f"{API_ENDPOINT}/results?documentId={doc_id}")
            if results_response.status_code == 200:
                confidence = results_response.json().get("extraction", {}).get("extraction_confidence", 0)
                results["passed"].append({"file": filename, "documentId": doc_id, "confidence": confidence})
                print(f"[{i}/{total}] ✅ {filename} — {confidence:.2f}% confidence")
                break
            elif attempt == 5:
                results["failed"].append({"file": filename, "documentId": doc_id, "reason": "results timeout"})
                print(f"[{i}/{total}] ❌ TIMEOUT — {filename}")
        
        # Respect rate limit
        time.sleep(0.5)
    
    except Exception as e:
        results["errors"].append({"file": filename, "error": str(e)})
        print(f"[{i}/{total}] ❌ ERROR — {filename}: {e}")

# Summary
passed = len(results["passed"])
failed = len(results["failed"])
errors = len(results["errors"])
avg_confidence = sum(r["confidence"] for r in results["passed"]) / passed if passed else 0

print(f"\n{'='*50}")
print(f"BATCH TEST COMPLETE")
print(f"{'='*50}")
print(f"Total:   {total}")
print(f"Passed:  {passed} ({passed/total*100:.1f}%)")
print(f"Failed:  {failed} ({failed/total*100:.1f}%)")
print(f"Errors:  {errors}")
print(f"Avg Confidence: {avg_confidence:.2f}%")
print(f"Finished at: {datetime.now().strftime('%H:%M:%S')}")

# Save results
with open("test-results-phase7.json", "w") as f:
    json.dump(results, f, indent=2)

print(f"\nFull results saved to test-results-phase7.json")