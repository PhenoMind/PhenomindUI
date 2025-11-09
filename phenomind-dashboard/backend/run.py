from app import create_app
from database import db
from models import Patient, EHR, Wearable, TimelineEvent, TrendData

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'Patient': Patient,
        'EHR': EHR,
        'Wearable': Wearable,
        'TimelineEvent': TimelineEvent,
        'TrendData': TrendData
    }

if __name__ == '__main__':
    import sys
    
    # Try port 5000, fallback to 5001 if busy
    port = 5001
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    
    print("=" * 50)
    print("Starting PhenoMind Flask Server")
    print("=" * 50)
    print(f"Server will be available at:")
    print(f"  - http://localhost:{port}")
    print(f"  - http://127.0.0.1:{port}")
    print("=" * 50)
    
    try:
        app.run(debug=True, host='0.0.0.0', port=port)
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"\n❌ Port {port} is already in use!")
            print(f"\nOptions:")
            print(f"1. Kill the process using port {port}:")
            print(f"   lsof -ti:{port} | xargs kill -9")
            print(f"2. Use a different port:")
            print(f"   python run.py 5001")
            print(f"3. On macOS, disable AirPlay Receiver:")
            print(f"   System Settings → General → AirDrop & Handoff → AirPlay Receiver → Off")
            print(f"\nTrying port 5001 instead...")
            app.run(debug=True, host='0.0.0.0', port=5001)
        else:
            raise

