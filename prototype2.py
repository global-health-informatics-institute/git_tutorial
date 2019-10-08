from qrtools import QR

qr = QR()
qr.decode("/home/pi/sample2")

print(qr.data)