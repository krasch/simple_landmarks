import argparse
from app.app import app

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start the annotation server")
    parser.add_argument('--host', default="localhost")
    parser.add_argument('--port', default=5000)

    args = parser.parse_args()
    app.run(host=args.host, port=args.port, debug=False)
