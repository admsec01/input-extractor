import requests
from bs4 import BeautifulSoup
import argparse
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser = argparse.ArgumentParser(description="Extract input fields with empty values from a URL or a list of URLs.")
parser.add_argument("--url", "-u", dest="url", help="Enter a URL")
parser.add_argument("--list", "-l", dest="file_path", help="Path to the file containing URLs")
args = parser.parse_args()

urls = []

if args.url:
    urls.append(args.url)

if args.file_path:
    with open(args.file_path, 'r') as file:
        urls.extend(file.read().splitlines())

if not urls:
    print("Please provide a URL with -u or a file with -l.")
else:
    for url in urls:
        try:
            print(f"\nFetching URL: {url}")
            response = requests.get(url, verify=False) 
            soup = BeautifulSoup(response.content, "html.parser")
            inputs = soup.find_all('input')
            empty_value_names = [input_element.get("name") for input_element in inputs if input_element.get("value") == ""]
            
            if empty_value_names:
                print("Input fields with empty values:")
                for name in empty_value_names:
                    print(f"- {name}")
            else:
                print("No input fields with empty values found.")
                
        except requests.exceptions.RequestException as e:
            print(f"Error fetching the URL: {e}")


