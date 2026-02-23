import argparse
import sys
from .engine import RateLimitEngine
from .storage import JSONStorage
from .config import DB_FILE, WINDOW_SECONDS


def main():
    parser = argparse.ArgumentParser(description="API Rate Limit Engine")

    subparsers = parser.add_subparsers(dest="command")

    req = subparsers.add_parser("request")
    req.add_argument("clientid")

    stat = subparsers.add_parser("status")
    stat.add_argument("clientid")

    subparsers.add_parser("list")

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    storage = JSONStorage(DB_FILE)
    engine = RateLimitEngine(storage)

    if args.command == "request":
        code, msg = engine.handle_request(args.clientid)
        print(f"{code} - {msg}")

    elif args.command == "status":
        info = engine.get_status(args.clientid)
        print(f"Limit: {info['limit']}/{WINDOW_SECONDS}s")
        print(f"Usage: {info['usage']}")
        print(f"Blocked: {info['is_limited']}")
        print(f"Time Left: {info['time_left']}s")

    elif args.command == "list":
        print("\n".join(engine.data.keys()))
