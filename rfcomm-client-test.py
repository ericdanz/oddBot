import bluetooth

bd_addr = "68:94:23:A3:AD:36"
port = 1

sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sock.connect((bd_addr, port))

sock.send("hello!!")

sock.close()