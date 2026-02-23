import argparse
import sys
from .engine import RateLimitEngine
from .storage import JSONStorage
from .config import DB_FILE, WINDOW_SECONDS


def main() -> None:
    parser = argparse.ArgumentParser(
        description="API Rate Limit Engine - Sliding Window Simulator"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # ---- request command ----
    request_parser = subparsers.add_parser(
        "request",
        help="Simulate an API request for a client"
    )
    request_parser.add_argument(
        "clientid",
        help="Alphanumeric client identifier"
    )

    # ---- status command ----
    status_parser = subparsers.add_parser(
        "status",
        help="Check rate limit status for a client"
    )
    status_parser.add_argument(
        "clientid",
        help="Alphanumeric client identifier"
    )

    # ---- list command ----
    subparsers.add_parser(
        "list",
        help="List all known clients"
    )

    args = parser.parse_args()

    # Initialize engine
    storage = JSONStorage(DB_FILE)
    engine = RateLimitEngine(storage)

    # ---- Handle Commands ----

    if args.command == "request":
        if not args.clientid.isalnum():
            print("Error: Client ID must be alphanumeric.")
            sys.exit(1)

        code, message = engine.handle_request(args.clientid)
        print(f"Response: {code}")
        print(message)

    elif args.command == "status":
        if not args.clientid.isalnum():
            print("Error: Client ID must be alphanumeric.")
            sys.exit(1)

        info = engine.get_status(args.clientid)

        print(f"\n--- Status for Client: {args.clientid} ---")
        print(f"Rate Limit:        {info['limit']} requests / {WINDOW_SECONDS}s")
        print(f"Current Usage:     {info['usage']}")
        print(f"Blocked?:          {'YES' if info['is_limited'] else 'No'}")

        if info['usage'] > 0:
            print(f"Time to Unblock:   {info['time_left']}s")
        else:
            print("Time to Unblock:   0s (Ready for request)")

    elif args.command == "list":
        clients = engine.data.keys()

        print("\nKnown Clients:")
        if not clients:
            print("  (No clients found)")
        else:
            for client in clients:
                print(f"  - {client}")


if __name__ == "__main__":
    main()
