import argparse
import json
import sys
from .yield_engine import NetYieldCalculator

def main():
    parser = argparse.ArgumentParser(description='Model explicit rental assumptions from JSON; no market defaults.')
    parser.add_argument('scenario', help='JSON file or - for stdin')
    args = parser.parse_args()
    try:
        if args.scenario == '-':
            scenario = json.load(sys.stdin)
        else:
            with open(args.scenario, encoding='utf-8') as source:
                scenario = json.load(source)
        currency = scenario.pop('currency')
        if not isinstance(currency, str) or len(currency) != 3 or not currency.isascii() or not currency.isupper() or not currency.isalpha():
            raise ValueError('currency must be an uppercase three-letter label')
        result = NetYieldCalculator.audit_yield(**scenario)
        result['currency'] = currency
        print(json.dumps(result, allow_nan=False, indent=2))
    except (OSError, ValueError, TypeError, KeyError) as error:
        parser.exit(2, f'Invalid scenario: {error}\n')

if __name__ == '__main__':
    main()
