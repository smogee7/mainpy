import requests

TOKEN = "7966482365:AAFVQjmqscxKZClLJjjbCPwbzPTLfA2t_7I"  # твой токен
url = f"https://api.telegram.org/bot{TOKEN}/deleteWebhook"
resp = requests.post(url)
print(resp.json())
