from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import threading
import time

class IBApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.connection_ready = threading.Event()  # signals connection
        self.data_received = threading.Event()    # signals at least one price tick received

    # Called when the connection is fully established
    def nextValidId(self, orderId):
        print(f"✅ Connection ready, next valid order ID: {orderId}")
        self.connection_ready.set()

    # Called for each price update
    def tickPrice(self, reqId, tickType, price, attrib):
        print(f"Tick Price. ReqId: {reqId}, Type: {tickType}, Price: {price}")
        self.data_received.set()  # mark that at least one price tick arrived

    # Handle errors
    def error(self, reqId, errorCode, errorString, contract=None):
        print(f"⚠️ Error. ReqId: {reqId}, Code: {errorCode}, Msg: {errorString}")


# 1️⃣ Connect to TWS
app = IBApp()
# Change port to 7497 if you are using paper trading TWS
app.connect("127.0.0.1", 7496, clientId=1)

# 2️⃣ Start event loop in a thread
def run_loop():
    app.run()

api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()

# 3️⃣ Wait until connection is ready
if not app.connection_ready.wait(timeout=10):
    print("❌ Failed to connect to TWS")
    app.disconnect()
    exit(1)

# 4️⃣ Define a contract (Apple stock)
contract = Contract()
contract.symbol = "AAPL"
contract.secType = "STK"
contract.exchange = "SMART"
contract.currency = "USD"

# 5️⃣ Request market data
print("Requesting market data for AAPL...")
app.reqMktData(1, contract, "", False, False, [])

# 6️⃣ Wait until at least one tick arrives or timeout after 10 seconds
if not app.data_received.wait(timeout=10):
    print("⚠️ No market data received within 10 seconds")

# 7️⃣ Disconnect
app.disconnect()
print("Disconnected from TWS")
