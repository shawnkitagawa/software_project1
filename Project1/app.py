from flask import Flask, render_template, request
import sys
from flask_socketio import SocketIO
import finnhub
import time
import json
finnhub_client = finnhub.Client(api_key="cn3hfjpr01qvutcdb680cn3hfjpr01qvutcdb68g")

# print(finnhub_client.stock_symbols('US'))
available_symbol = finnhub_client.stock_symbols('US')
# available_symbol = json.dumps(available_symbol, indent=2)
print(type(available_symbol))

display_symbol = [data["displaySymbol"] for data in available_symbol]

# data = {
#     "symbol":display_symbol

# }

with open('available_symbol.txt', 'w') as f:
    json.dump(display_symbol, f, indent = 4)
app = Flask(__name__)
socket = SocketIO(app)



@app.route("/")
def index():
    return render_template('index.html', stock_availability = display_symbol)


# def task_background(data):

#     quotes = finnhub_client.quote(data)

#     print(quotes)
#     sys.stdout.flush()

#     socket.emit('response_event',quotes)
#     time.sleep(10)
@app.route("/market_status")
def market():
    market_status = finnhub_client.market_status(exchange='US')
    return render_template('market_status.html', market_status = market_status)
    
active_sockets = {}


@socket.on("data")
def stock_data(data):
    # if prev_ticker != "9999":
    #     print(f"the previous ticker is {prev_ticker}")
    #     sid = active_sockets[prev_ticker]
    #     print(f"the sid is {sid}")
    #     socket.emit("disconnect_old",namespace='/', room=sid)


    # active_sockets[data] = request.sid
    # print(active_sockets[data])
    print(f"User {data}!")
    connect = True
    news = finnhub_client.company_news(data, _from="2023-12-01", to="2024-02-10")
    socket.emit("news", news)


    while connect:
        socket.sleep(15)
        quote = finnhub_client.quote(data)
        socket.emit("quotes", quote)
        socket.emit("check_connection")
        # if (connection == False):
        #     print("disconnectekjafsdkljasl;kdjklas;jfkdlas;j")
        #     socket.emi("disconnect")



if __name__ == "__main__":
    app.run(debug=True)