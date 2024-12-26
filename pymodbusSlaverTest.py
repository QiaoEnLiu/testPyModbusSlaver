import asyncio, logging, serial
from pymodbus.server.async_io import ModbusSerialServer
from pymodbus.datastore import ModbusSlaveContext, ModbusSequentialDataBlock, ModbusServerContext
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.framer import ModbusRtuFramer


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

# 設定串口參數
serial_port = 'COM11'  # 根據需要設置 COM 埠
baud_rate = 9600
bytesize = 8
parity = 'N'
stopbits = 1
timeout = 0.065

# 創建資料儲存區
co = ModbusSequentialDataBlock(1, [1, 0, 1, 0, 1, 0, 1, 0, 1, 0])  # 初始化 10 個線圈，交替 1 和 0
hr = ModbusSequentialDataBlock(1, [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000])  # 初始化 10 個保持寄存器，數值從 100 到 1000
di = ModbusSequentialDataBlock(1, [1, 0, 1, 0, 1, 0, 1, 0, 1, 0])  # 初始化 10 個離散輸入，交替 1 和 0
ir = ModbusSequentialDataBlock(1, [1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400])  # 初始化 10 個輸入寄存器，數值從 1500 到 2400

store = ModbusSlaveContext(
    di=di,  # Discrete Inputs
    co=co,  # Coils
    hr=hr,  # Holding Registers
    ir=ir   # Input Registers
)

# 設定伺服器上下文
context = ModbusServerContext(slaves={1: store}, single=False)

# 設定伺服器信息
identity = ModbusDeviceIdentification()
identity.VendorName = 'Modbus Slave'
identity.ProductCode = 'RTU'
identity.VendorUrl = 'http://modbus.org'
identity.ProductName = 'Modbus RTU Server'
identity.ModelName = 'RTU-Model'
identity.MajorMinorRevision = '1.0'

# 創建回調函數，顯示收到的請求
def request_handler(request):
    logger.info(f"Received request: {request}")

# 重寫 ModbusSerialServer，添加日誌打印
class CustomModbusSerialServer(ModbusSerialServer):
    async def _handle_request(self, request, context):
        # 在處理每個請求時打印
        logger.debug(f"Handling request: {request}")
        # 呼叫父類的方法來處理請求
        await super()._handle_request(request, context)

# 使用自定義的 Modbus RTU 伺服器，並指定回調函數來顯示請求
async def start_server():
    server = ModbusSerialServer(
        context=context, 
        port=serial_port, 
        baudrate=baud_rate,
        bytesize=bytesize,
        parity=parity,
        stopbits=stopbits,
        timeout=timeout,
        identity=identity, 
        framer=ModbusRtuFramer
    )
    await server.serve_forever()  # 啟動伺服器，並開始處理請求

# 手動啟動事件循環
if __name__ == "__main__":
    loop = asyncio.get_event_loop()  # 取得事件循環
    loop.run_until_complete(start_server())  # 啟動伺服器
