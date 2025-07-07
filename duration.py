from datetime import datetime
from collections import defaultdict

# Sample data
data = {
    "list": [
    ]
}

# Helper function to extract site from calcRund
def extract_site(calc_rund):
    parts = calc_rund.split("_")
    if len(parts) >= 2:
        return parts[1]
    return None

# Prepare containers
site_durations = defaultdict(list)

# Process each job
for job in data["list"]:
    site = extract_site(job["calcRund"])
    start = datetime.strptime(job["startTime"], "%Y-%m-%d %H:%M:%S")
    end = datetime.strptime(job["endTime"], "%Y-%m-%d %H:%M:%S")
    duration = (end - start).total_seconds() / 60  # duration in minutes
    site_durations[site].append(duration)

# Display result
print(f"{'SITE':<10} | {'Number of runs':<15} | {'Average duration (min)':<25}")
print("-" * 55)
for site, durations in site_durations.items():
    avg_duration = sum(durations) / len(durations)
    print(f"{site:<10} | {len(durations):<15} | {avg_duration:<25.2f}")
