import argparse
# PubMed Fetcher
A Python script to fetch research papers from PubMed.


def get_arguments():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed")
    
    parser.add_argument("query", type=str, help="Search query for PubMed API")
    parser.add_argument("-f", "--file", type=str, help="Output filename (CSV/Excel)", default="results.csv")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    
    return parser.parse_args()

args = get_arguments()

print(f"Query: {args.query}")
print(f"Output File: {args.file}")
print(f"Debug Mode: {'Enabled' if args.debug else 'Disabled'}")
