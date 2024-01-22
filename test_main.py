import requests
url = "http://127.0.0.1:5000/volatility"

file_path = "NIFTY 50-22-01-2023-to-22-01-2024.csv"
with open(file_path, 'rb') as file:
    files = {'file': (file.name, file, 'text/csv')}
    response = requests.post(url, files=files)
print(response.text)
