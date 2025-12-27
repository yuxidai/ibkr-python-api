from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import threading
import time

# 1️⃣ Create a class combining EWrapper and EClient
class IBApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    # 2️⃣ Callback to handle price updates
    def tickPrice(self, reqId, tickType, price, attrib):
        print(f"Tick Price. ReqId: {reqId}, Type: {tickType}, Price: {price}")

# 3️⃣ Connect to TWS or IB Gateway
app = IBApp()
app.connect("127.0.0.1", 7497, clientId=1)  # 7496 for live accounts

# 4️⃣ Start the network loop in a separate thread
def run_loop():
    app.run()

api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()

# 5️⃣ Define a contract (Apple stock)
contract = Contract()
contract.symbol = "AAPL"
contract.secType = "STK"
contract.exchange = "SMART"
contract.currency = "USD"

# 6️⃣ Request market data
app.reqMktData(1, contract, "", False, False, [])

# 7️⃣ Let it run for 10 seconds to receive some data
time.sleep(10)

# 8️⃣ Disconnect
app.disconnect()
print("Disconnected from TWS")
