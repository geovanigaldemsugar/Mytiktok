import requests

url = 'https://snaptik.app/getHdLink.php?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjczNTAzODc4NjAxNTI5MTMxOTgifQ.bAnJxIr1XVxWtGPLPUB89akMRln-n2rGH28xTcZ5Dy4'

response  = requests.get(url)
print(response.json())