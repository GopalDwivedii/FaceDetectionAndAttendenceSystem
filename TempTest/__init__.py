def TempTest():
    import serial
    import serial.tools.list_ports as stp
    ports = stp.comports()
    serialInst = serial.Serial()
    portList = []
    for onePort in ports:
        portList.append(str(onePort))
        print(str(onePort))
    val = 10
    for x in range(0, len(portList)):
        if portList[x].startswith("COM" + str(val)):
            portVar = "COM" + str(val)
            print(portList[x])
    serialInst.baudrate = 9600
    serialInst.port = 'COM' + str(val)
    serialInst.open()
    while True:
        if serialInst.in_waiting:
            packet = serialInst.readline()
            packet = serialInst.readline()
            packet = serialInst.readline()
            packet = serialInst.readline()
            return (packet.decode('utf'))
temp = TempTest()
def temprature():
    return temp