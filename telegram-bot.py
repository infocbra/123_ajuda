import requests

TELEGRAM_API_TOKEN = "1856607725:AAFtHus3lxRHHMI2yZr6iVAPoxohOQwkE1s"
WEBHOOK_URL = "https://123ajuda.tech:5005/webhook"

url = f"https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/setWebhook"
payload = {
    "url": WEBHOOK_URL
}

response = requests.post(url, data=payload)
print(response.text)
