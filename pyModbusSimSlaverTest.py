from pymodbus.server import StartTcpServer, StartSerialServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.device import ModbusDeviceIdentification
import logging

# 設定日誌紀錄
logging.basicConfig(level=logging.DEBUG)

# 初始化寄存器數據
store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock(0, [1] * 10),  # 離散輸入 (Discrete Inputs)
    co=ModbusSequentialDataBlock(0, [0] * 10),  # 線圈 (Coils)
    hr=ModbusSequentialDataBlock(0, [100] * 10),  # 保持寄存器 (Holding Registers)
    ir=ModbusSequentialDataBlock(0, [200] * 10),  # 輸入寄存器 (Input Registers)
)

context = ModbusServerContext(slaves=store, single=True)

# 設定伺服器的標識
identity = ModbusDeviceIdentification()
identity.VendorName = "pymodbus"
identity.ProductCode = "PM"
identity.VendorUrl = "https://github.com/pymodbus-dev/pymodbus"
identity.ProductName = "Modbus Simulator"
identity.ModelName = "Modbus Server"
identity.MajorMinorRevision = "1.0"

def start_tcp_server():
    # 啟動 TCP 模擬伺服器
    print("Starting Modbus TCP Simulator Server on localhost:5020")
    StartTcpServer(context = context, identity=identity, address=("localhost", 5020))

def start_rtu_server():
    # 啟動 RTU 模擬伺服器
    port = input("Starting Modbus RTU Simulator Server on COM* or /dev/ttyUSB* (9600bps):")
    StartSerialServer(context = context, identity=identity, port=port, baudrate=9600)

if __name__ == "__main__":
    # 讓用戶選擇 TCP 或 RTU 模式
    mode = input("請選擇模擬模式（TCP/RTU，預設為RTU）：").strip().upper()

    if mode == "TCP":
        start_tcp_server()
    else:
        start_rtu_server()