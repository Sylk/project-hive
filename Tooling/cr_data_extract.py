import dolphin_memory_engine as dolphin

partType = int(input("Part type (0-4): "))
dolphin.hook()
baseAddress = 0x8024e120
partTypeOffsets = [0x1b98, 0x1e28, 0x28d48, 0x2e2e8, 0x33308]

baseAddress += partTypeOffsets[partType]
output = ""
if (not dolphin.is_hooked()) :
    print("not hooked")
    quit()
if (partType == 0):
    #TODO: put in better order (ground, air, dash, CJ)
    dataOffsets = {
        0x40: 2, #Down
        0x42: 1, #Defense
        0x43: 1, #Knockback
        0x44: 1, #Hitstun
        0x46: 1, #Full down time
        0x47: 1, #Mash down time reduction
        0x48: 1, #Down gun damage
        0x49: 1, #Down bomb damage
        0x4A: 1, #Down pod damage
        0x4B: 1, #Down charge damage
        0x4C: 1, #Gun damage
        0x4F: 1, #Gun endlag
        0x4D: 1, #Bomb damage
        0x4E: 1, #Pod damage
        0xD2: 2, #Charge damage?
        0x56: 1, #Dash type
        0x60: 1, #Air dash angle
        0xA2: 2, #Gravity
        0x51: 1, #Dash startup
        0x54: 1, #Dash landing lag
        0x62: 1, #Dash duration
        0x66: 2, #Dash speed
        0x72: 2, #Run speed
        0x78: 2, #Ground accel
        0x7E: 2, #Ground turning
        0x84: 2, #Jump height
        0x5A: 2, #Air jump height
        0x8A: 2, #Jump duration
        0x90: 2, #Lateral air speed
        0x96: 2, #Air accel
        0x9C: 2, #Jump landing lag
    }

    for key in dataOffsets:
        addr = baseAddress + key
        value = int.from_bytes(dolphin.read_bytes(addr, dataOffsets[key]))
        if (key == 0x56): #dash type
            addr -= key
            if (value == 1):
                airMovType = "Continuous Jump"
                airMovs = dolphin.read_byte(addr + 0x57)
            elif value == (0):
                airMovType = "Air Dash"
                airMovs = dolphin.read_byte(addr + 0x5E)
                if (dolphin.read_byte(addr + 0x5F) == 1):
                    airMovType += " (SV)"
            elif value == (2):
                airMovType = "Sky Dash"
                airMovs = dolphin.read_byte(addr + 0x5E)
            output += airMovType + "," + str(airMovs) + ","
        else:
            output += str(value) + ","
        if (key in [0xA2, 0x51, 0x54, 0x62, 0x66, 0x72, 0x78, 0x7E, 0x84, 0x5A, 0x8A, 0x90, 0x96, 0x9C]): #reduced/boosted values
            rVal = int.from_bytes(dolphin.read_bytes(addr - dataOffsets[key], dataOffsets[key]))
            red = value - rVal
            bVal = int.from_bytes(dolphin.read_bytes(addr + dataOffsets[key], dataOffsets[key]))
            boo = bVal - value
            output += str(red) + "," + str(boo) + ","

elif (partType == 1):
    baseAddress += 0xA1
    output += str(dolphin.read_byte(baseAddress)) + "," #Slideshot duration
    baseAddress += 0x3B
    baseStatOffsets = {
        0x00: 1, #Startup
        0x01: 1, #Number of shots
        0x02: 1, #Rounds per shot
        0x03: 1, #Spread direction
        0x04: 1, #Delay between shots
        0x05: 1  #Endlag
    }
    phaseStatOffsets = {
        0x16: 2, #Damage
        0x18: 2, #Down
        0x1E: 2  #Hitstun
    }
    for i in range(2):
        for key in baseStatOffsets:
            addr = baseAddress + key
            value = dolphin.read_byte(addr)
            if (key == 0x03): #spread direction
                if (value == 0):
                    output += "Vertical,"
                else:
                    output += "Horizontal,"
            else:
                output += str(value) + ","
        baseAddress += 0x10
        for key in phaseStatOffsets:
            for j in range(5):
                addr = baseAddress + key + j*0x28
                value = int.from_bytes(dolphin.read_bytes(addr, 2))
                output += str(value) + ","
        baseAddress += 0xC8

elif (partType == 2):
    dataOffsets = {
        0xA1: 1,  #Bombs fired
        0xAC: 1,  #Number of explosions
        0xA5: 1,  #Reload
        0xA8: 2,  #Projectile speed
        0xC0: 2,  #Damage
        0xC2: 2,  #Down
        0xC8: 2,  #Hitstun
        0xF5: 1,  #Reload
        0xF8: 2,  #Projectile speed
        0x110: 2, #Damage
        0x112: 2, #Down
        0x118: 2, #Hitstun
    }
    for key in dataOffsets:
        addr = baseAddress + key
        value = int.from_bytes(dolphin.read_bytes(addr, dataOffsets[key]))
        output += str(value) + ","

elif (partType == 3):
    dataOffsets = {
        0xE1: 1,  #Pod count
        0xE2: 1,  #Pods per shot
        0xEA: 2,  #Fuse time
        0xF5: 1,  #Roaming homing
        0xF6: 1,  #Locked on homing
        0xF8: 2,  #Roaming speed
        0xFA: 2,  #Locked on speed
        0x103: 1, #Lock on range
        0x128: 2, #Damage
        0x12A: 2, #Down
        0x130: 2  #Hitstun
    }
    for key in dataOffsets:
        addr = baseAddress + key
        value = int.from_bytes(dolphin.read_bytes(addr, dataOffsets[key]))
        output += str(value) + ","

elif (partType == 4):
    dataOffsets = [
        0x81, #Run speed
        0x82, #Ground accel
        0x83, #Ground turning
        0x84, #Jump height
        0x85, #Jump speed
        0x86, #Lateral air speed
        0x87, #Air accel
        0x88, #Landing lag
        0x89, #Gravity
        0x8A, #Dash startup
        0x8B, #Dash landing lag
        0x8C, #Continuous jump length
        0x8D, #Dash duration
        0x8E  #Dash speed
    ]
    for i in range(len(dataOffsets)):
        value = dolphin.read_byte(baseAddress + dataOffsets[i])
        output += str(value) + ","

print(output)