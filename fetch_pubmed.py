import requests
import pandas as pd
import argparse

# PubMed API base URL
PUBMED_API_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_SUMMARY_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

def fetch_pubmed_papers(query, output_file):
    """
    Fetch research papers from PubMed API based on the user query and save the results to a CSV file.
    """
    # Step 1: Get the PubMed IDs (PMIDs) matching the search query
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": 10  # Fetch top 10 papers (You can increase this)
    }
    response = requests.get(PUBMED_API_URL, params=params)

    if response.status_code != 200:
        print("❌ Failed to fetch data from PubMed API")
        return

    data = response.json()
    pmids = data.get("esearchresult", {}).get("idlist", [])

    if not pmids:
        print("❌ No papers found for the query:", query)
        return

    # Step 2: Get details for each paper
    paper_details = []
    for pmid in pmids:
        summary_params = {
            "db": "pubmed",
            "id": pmid,
            "retmode": "json"
        }
        summary_response = requests.get(PUBMED_SUMMARY_URL, params=summary_params)

        if summary_response.status_code != 200:
            print(f"⚠️ Failed to fetch details for PMID: {pmid}")
            continue

        summary_data = summary_response.json()
        result = summary_data.get("result", {}).get(pmid, {})

        paper_details.append({
            "PubmedID": pmid,
            "Title": result.get("title", "N/A"),
            "Publication Date": result.get("pubdate", "N/A"),
            "Authors": ", ".join([author["name"] for author in result.get("authors", [])]) if result.get("authors") else "N/A"
        })

    # Step 3: Save results to CSV
    df = pd.DataFrame(paper_details)
    df.to_csv(output_file, index=False)
    print(f"✅ Results saved successfully to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch PubMed research papers")
    parser.add_argument("query", type=str, help="Search query for PubMed")
    parser.add_argument("-o", "--output", type=str, default="pubmed_results.csv", help="Output CSV file name")
    args = parser.parse_args()

    fetch_pubmed_papers(args.query, args.output)
