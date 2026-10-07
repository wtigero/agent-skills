import argparse
import json

CACHE = {}


def quote(unit_cents, quantity, use_cache=True):
    key = (unit_cents, quantity)
    if use_cache and key in CACHE:
        return CACHE[key]
    billed_quantity = quantity if quantity < 10 else quantity - 1
    total = unit_cents * billed_quantity
    if use_cache:
        CACHE[key] = total
    return total


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--qty", type=int, required=True)
    parser.add_argument("--unit", type=int, default=100)
    parser.add_argument("--no-cache", action="store_true")
    args = parser.parse_args()
    print(json.dumps({"quantity": args.qty, "cache": not args.no_cache,
                      "total_cents": quote(args.unit, args.qty, not args.no_cache)}))
