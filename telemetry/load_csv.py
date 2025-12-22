import csv 
from packet import Packet
from stati import Packetstat


FILEPATH = "dataset.csv"

stati = Packetstat()

f = open(FILEPATH,"r")

reader = csv.reader(f)


def csv_to_dict(row):
    try:
        return {
        "t": int(row[0]),
        "pre": float(row[1]),
        "ax": float(row[2]),
        "ay": float(row[3]),
        "az": float(row[4])

    }

    except (ValueError,IndexError):
        return None
    


next(reader)
for row in reader:
    data = csv_to_dict(row)

    if data is None:
        print("reject: malformed row")
        continue
    packet = Packet(data["t"],data["pre"],data["ax"],data["ay"],data["az"])
    
    if packet.validate():
        alti = packet.altitude()
        print(alti)
        stati.accept(packet) #also add to accept.csv
    else:
        print("reject")
        stati.reject(packet) # to reject.csv
        continue
stati.summary()


