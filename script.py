#!/usr/bin/env python3

import argparse
import requests
import xml.etree.ElementTree as ET
import pandas as pd

# Function to fetch PubMed data
def fetch_pubmed(query):
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "xml",
        "retmax": 10  # Number of results
    }

    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        print("Error: Failed to fetch data")
        return None

    return response.text

# Function to parse XML and extract IDs
def parse_pubmed(xml_data):
    root = ET.fromstring(xml_data)
    ids = [id_elem.text for id_elem in root.findall(".//Id")]
    return ids

# Function to save results
def save_results(paper_ids, filename):
    df = pd.DataFrame({"PubMed_ID": paper_ids})
    df.to_csv(filename, index=False)
    print(f"Results saved to {filename}")

# Argument parser
def get_arguments():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed")
    parser.add_argument("query", type=str, help="Search query for PubMed API")
    parser.add_argument("-f", "--file", type=str, help="Output filename (CSV)", default="results.csv")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    return parser.parse_args()

# Main function
if __name__ == "__main__":
    args = get_arguments()
    
    print(f"Query: {args.query}")
    print(f"Output File: {args.file}")
    print(f"Debug Mode: {'Enabled' if args.debug else 'Disabled'}")

    xml_data = fetch_pubmed(args.query)
    if xml_data:
        paper_ids = parse_pubmed(xml_data)
        save_results(paper_ids, args.file)

