# dns-query-tool

## Description

A streamlined CLI tool for querying DNS records from any valid domain, returning A, AAAA, CNAME, MX, or TXT records — with optional CSV or JSON output for easy integration into analysis workflows.  

Built with **dnspython**, this project reflects practical skills in network automation, DNS querying, CLI design, error handling, and data processing — all wrapped in an efficient, no-frills script.  

Designed to deliver clear, actionable DNS insights, this tool serves as a valuable resource for network and security professionals, students, and enthusiasts alike. Whether used for research, troubleshooting, or learning, it offers a reliable and efficient way to extract meaningful domain information without unnecessary complexity.

---

## Features

- Query multiple domains at once with comma-separated input  
- Support for common DNS record types: A, AAAA, CNAME, MX, TXT  
- Interactive record type selection when no flags are provided  
- Save query results to JSON or CSV files with automatic extension handling  
- Preview of results in tabular CSV format and formatted JSON in CLI  
- Robust error handling and logging for reliable operation  
- Lightweight and easy to use with no complex dependencies beyond dnspython and pandas  

---

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/ajones1139/dns-query-tool.git
   cd dns-query-tool
2. Optional (but recommended) Create a Virtual Environment:
  python3 -m venv venv
  source venv/bin/activate  # Linux/macOS
  .\venv\Scripts\activate   # Windows

3. Install dependencies:
   pip install -r requirements.txt or pip install dnspython pandas

## Usage

Run the script with one or more domains:
    python dns-query-tool.py google.com,github.com -r A,MX
    -r or --records flag specifies which DNS record types to query.
    If -r is omitted, it defaults to querying A, CNAME, AAAA, and TXT records with an interactive prompt to select which records to display.

Can Run Interactively Also:
    python dns-query-tool.py

---

Saving Results:
    After queries complete, you can preview the results in CSV table or JSON formats directly in the terminal, then choose to save them as .csv or .json files. The tool automatically appends file extensions if omitted.

---

 Skills Demonstrated:
  -Network Automation and DNS querying using Python and dnspython external library.\
  -CLI design with argument parsing using argv\
  -Interactive user input handling\
  -Structured data processing and export to CSV and JSON formats\
  -Error handling and logging

---

Contributions & Feedback:
This is mainly a project where its efficient for simple queries, but also an invitation to expand and collaborate if you have any ideas of improvement or expanding functionality. Feedback is appreciated!
