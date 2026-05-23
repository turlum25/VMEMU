# RAM.py

# virtual RAM bytes
# What this does:
# -> Waits for main WSIM to send command into this thing 
# by the EDR command (Edit Data RAM, eg: edr 0x0, 00000000 00000001)
# I will construct my own RAM manager and panicker later on.
# -> Yes this will be a module

memory = {
	"0x0": "00000000 00000000",
	"0x1": "00000000 00000000",
	"0x2": "00000000 00000000",
	"0x3": "00000000 00000000",
	"0x4": "00000000 00000000",
	"0x5": "00000000 00000000",
	"0x6": "00000000 00000000",
	"0x7": "00000000 00000000"
}

def EditRAM(address, byte1, byte2):
	try:
		address = address.lower()
		new_data = f"{byte1} {byte2}"
		
		if "0x0" in address:
			memory["0x0"] = new_data
		elif "0x1" in address:
			memory["0x1"] = new_data
		elif "0x2" in address:
			memory["0x2"] = new_data
		elif "0x3" in address:
			memory["0x3"] = new_data
		elif "0x4" in address:
			memory["0x4"] = new_data
		elif "0x5" in address:
			memory["0x5"] = new_data
		elif "0x6" in address:
			memory["0x6"] = new_data
		elif "0x7" in address:
			memory["0x7"] = new_data
	except:
		pass

def ReadRAM(address):
	try:
		address = address.lower()
		if "0x0" in address: return memory["0x0"]
		elif "0x1" in address: return memory["0x1"]
		elif "0x2" in address: return memory["0x2"]
		elif "0x3" in address: return memory["0x3"]
		elif "0x4" in address: return memory["0x4"]
		elif "0x5" in address: return memory["0x5"]
		elif "0x6" in address: return memory["0x6"]
		elif "0x7" in address: return memory["0x7"]
	except:
		pass
	return "00000000 00000000"