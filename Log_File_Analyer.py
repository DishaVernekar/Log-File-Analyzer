import re
from collections import Counter

# Path to the web server log file
log_file_path = '/var/log/apache2/access.log'

def analyze_log_file():
    with open(log_file_path, 'r') as f:
        logs = f.readlines()

    # Initialize counters
    error_404_count = 0
    page_counter = Counter()
    ip_counter = Counter()

    # Regular expressions to capture relevant data
    ip_pattern = re.compile(r'(\d+\.\d+\.\d+\.\d+)')
    status_code_pattern = re.compile(r'"\s(\d{3})\s')
    request_pattern = re.compile(r'GET\s(/[^ ]*)')

    for log in logs:
        # Extract IP address
        ip_match = ip_pattern.match(log)
        if ip_match:
            ip_counter[ip_match.group(1)] += 1

        # Check for 404 errors
        status_code_match = status_code_pattern.search(log)
        if status_code_match and status_code_match.group(1) == '404':
            error_404_count += 1

        # Extract requested pages
        request_match = request_pattern.search(log)
        if request_match:
            page_counter[request_match.group(1)] += 1

    # Output results
    print(f"Total 404 errors: {error_404_count}")
    print("\nMost Requested Pages:")
    for page, count in page_counter.most_common(5):
        print(f"{page}: {count} requests")

    print("\nIP Addresses with Most Requests:")
    for ip, count in ip_counter.most_common(5):
        print(f"{ip}: {count} requests")

if __name__ == "__main__":
    analyze_log_file()