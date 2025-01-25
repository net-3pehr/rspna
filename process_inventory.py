import re
import pandas as pd

# Define input and output file paths
inventory_file = "inventory.txt"  # Replace with actual inventory file path
ip_plan_file = "IPplan.txt"  # Replace with actual IP plan file path
output_file = "inventory_with_customers.xlsx"

# Function to infer city and popsite based on conditions
def infer_city_and_popsite(hostname):
    city, popsite = "Unknown", "Unknown"
    if "sessions\\A\\" in hostname:
        city = "City A"
    if "sessions\\B" in hostname:
        popsite = "Branch B"
    return city, popsite

# Load IP plan data for customer mapping
ip_plan_data = pd.read_csv(ip_plan_file, sep="\t", names=["IP Address", "Description"], usecols=[0, 1])
ip_to_customer = {row["IP Address"]: row["Description"] for _, row in ip_plan_data.iterrows()}

# Parse the inventory file
data = []
with open(inventory_file, "r") as file:
    for line in file:
        # Match relevant lines with IP and Hostname
        match = re.match(r"^(.*)%([0-9.]+)%.*%se.emami.*$", line.strip())
        if match:
            hostname, ip_address = match.groups()
            city, popsite = infer_city_and_popsite(hostname)
            customer = ip_to_customer.get(ip_address, "Unknown")
            data.append({
                "IP Address": ip_address,
                "Hostname": hostname.strip(),
                "City": city,
                "Popsite": popsite,
                "Customer": customer
            })

# Create a DataFrame and export to Excel
df = pd.DataFrame(data)
df.to_excel(output_file, index=False)

print(f"Inventory processed and saved to {output_file}")
