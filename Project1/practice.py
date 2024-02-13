import finnhub
finnhub_client = finnhub.Client(api_key="cn3hfjpr01qvutcdb680cn3hfjpr01qvutcdb68g")
quotes = finnhub_client.quote('AAPL')

print(quotes)
