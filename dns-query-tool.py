import dns.resolver
import json
import csv
import pandas as pd
import argparse
import logging
import os
import sys

# Setup logging to file in script directory
log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dns_tool_errors.log')
logging.basicConfig(filename=log_file,
                    filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.WARNING)

def query_dns_records(domain, record_types):
    results = {}
    for rtype in record_types:
        try:
            answers = dns.resolver.resolve(domain, rtype)
            if rtype == 'TXT':
                results[rtype] = [''.join([part.decode() if isinstance(part, bytes) else part for part in rdata.strings]) for rdata in answers]
            else:
                results[rtype] = [rdata.to_text() for rdata in answers]
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers):
            results[rtype] = []
        except Exception as e:
            logging.warning(f"Error querying {rtype} records for {domain}: {e}")
            results[rtype] = []
    return results

def display_results(domain, results):
    print(f"\nResults for {domain}:")
    for rtype, records in results.items():
        print(f"\n{rtype} Records:")
        if records:
            for rec in records:
                print(f"  - {rec}")
        else:
            print("  No records found.")

def preview_csv(all_data):
    rows = []
    for domain, data in all_data.items():
        for rtype, values in data.items():
            if values:
                for val in values:
                    rows.append({'Domain': domain, 'Record Type': rtype, 'Record': val})
            else:
                rows.append({'Domain': domain, 'Record Type': rtype, 'Record': 'No records found'})
    df = pd.DataFrame(rows)
    print("\nCSV Preview:")
    print(df)

def save_results_to_json(data, filename):
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        logging.warning(f"Failed to save JSON to {filename}: {e}")
        print(f"Error saving JSON file: {e}")

def save_results_to_csv(data, filename):
    try:
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            # Write header
            writer.writerow(['domain', 'record type', 'record info'])
            for domain, records in data.items():
                for record_type, values in records.items():
                    if values:
                        for val in values:
                            writer.writerow([domain, record_type, val])
                    else:
                        writer.writerow([domain, record_type, 'No records found'])
    except Exception as e:
        logging.warning(f"Failed to save CSV to {filename}: {e}")
        print(f"Error saving CSV file: {e}")

def prompt_record_types(available_types):
    print(f"Record types found: {', '.join(available_types)}")
    user_input = input("Enter record types to display separated by comma (default: all): ").strip()
    if user_input == '':
        chosen = available_types
    else:
        chosen = [r.strip().upper() for r in user_input.split(',') if r.strip().upper() in available_types]
        if not chosen:
            print("No valid record types selected, showing all.\n")
            chosen = available_types
    return chosen

def main():
    parser = argparse.ArgumentParser(description="DNS Query Tool")
    parser.add_argument('domains', nargs='?', help='Comma-separated list of domains to query')
    parser.add_argument('-r', '--records', default=None,
                        help="Comma-separated DNS record types to query (e.g., A,AAAA,MX). If not provided, defaults to A,CNAME,AAAA,TXT with interactive selection.")
    args = parser.parse_args()

    if args.domains:
        domains = [d.strip() for d in args.domains.split(',') if d.strip()]
        if not domains:
            print("No valid domains provided. Exiting.")
            return

        if args.records:
            record_types = [r.strip().upper() for r in args.records.split(',') if r.strip()]
        else:
            record_types = ['A', 'CNAME', 'AAAA', 'TXT']

        all_results = {}

        for domain in domains:
            print(f"\nQuerying {domain} for records: {', '.join(record_types)}")
            results = query_dns_records(domain, record_types)

            if args.records:
                filtered = results
            else:
                available = [rtype for rtype, vals in results.items() if vals]
                if not available:
                    print(f"No DNS records found for {domain}.")
                    continue
                chosen = prompt_record_types(available)
                filtered = {k: results[k] for k in chosen}

            display_results(domain, filtered)
            all_results[domain] = filtered

        if not all_results:
            print("No results to save. Exiting.")
            return

        preview_csv(all_results)

        print("\nJSON Preview:")
        print(json.dumps(all_results, indent=2))

        save = input("\nSave results? Enter 'json', 'csv', or press Enter to skip: ").strip().lower()
        if save in ['json', 'csv']:
            filename = input(f"Enter filename (default: dns_results.{save}): ").strip()
            if not filename:
                filename = f"dns_results.{save}"
            elif not filename.lower().endswith(f".{save}"):
                filename += f".{save}"
            if save == 'json':
                save_results_to_json(all_results, filename)
            else:
                save_results_to_csv(all_results, filename)
            print(f"Results saved to {filename}")
        else:
            print("Results not saved.")

    else:
        print("No domains specified. Entering interactive mode.")
        while True:
            domain = input("Enter a domain (or press Enter to exit): ").strip()
            if not domain:
                print("Exiting interactive mode.")
                break

            record_types = ['A', 'CNAME', 'AAAA', 'TXT']
            print(f"\nQuerying DNS records for {domain}...\n")
            results = query_dns_records(domain, record_types)

            available = [rtype for rtype, vals in results.items() if vals]
            if not available:
                print("No DNS records found for this domain.\n")
                continue

            chosen = prompt_record_types(available)
            filtered = {k: results[k] for k in chosen}

            display_results(domain, filtered)
            preview_csv({domain: filtered})

            print("\nJSON Preview:")
            print(json.dumps(filtered, indent=2))

            save = input("\nSave results? Enter 'json', 'csv', or press Enter to skip: ").strip().lower()
            if save in ['json', 'csv']:
                filename = input(f"Enter filename (default: {domain}_dns_results.{save}): ").strip()
                if not filename:
                    filename = f"{domain}_dns_results.{save}"
                elif not filename.lower().endswith(f".{save}"):
                    filename += f".{save}"
                if save == 'json':
                    save_results_to_json(filtered, filename)
                else:
                    save_results_to_csv({domain: filtered}, filename)
                print(f"Results saved to {filename}\n")
            else:
                print("Results not saved.\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nProcess interrupted by user. Exiting.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}", exc_info=True)
        print(f"An unexpected error occurred: {e}. Check the log file for details.")
        sys.exit(1)
