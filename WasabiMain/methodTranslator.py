def rowDist(wella, wellb):
    row_a = ord(wella[0].lower()) - ord('a')  
    row_b = ord(wellb[0].lower()) - ord('a')  

    return abs(row_a-row_b)

def columnDist(wella, wellb):
    column_a = int(wella[1:])
    column_b = int(wellb[1:])
    return abs(column_a - column_b)

def gradient(info):
    wells = info["wells"]
    direction = info["direction"]
    contents = info["contents"]
    increment = info["increment"]
    intital_volume = info["intitalVolume"]
    volumeMap = {}

    match direction:
        case "right":
            for well in wells:
                volume = columnDist(wells[0], well) * increment + intital_volume # distance between initial and final columns * increment + intitial 
                volumeMap[well] = {contents:contents, volume:volume} 
        case "down":
            for well in wells:
                volume = rowDist(wells[0], well) * increment + intital_volume # well row (from 0) * increment + initial 
                volumeMap[well] = {contents:contents, volume:volume} 
        case "left":
            for well in wells:
                volume = columnDist(wells[-1], well) * increment + intital_volume
                volumeMap[well] = {contents:contents, volume:volume} 
        case"up":
            for well in wells:
                volume = rowDist(wells[-1], well) * increment + intital_volume
                volumeMap[well] = {contents:contents, volume:volume}
    return volumeMap

def constant_volume(info):
    contents = info["contents"]
    wells = info["wells"]
    volume = ["volume"]
    volumeMap = dict.fromkeys(wells, {contents:contents, volume:volume} )
    return volumeMap


def translate(info):
    method = info["method"]
    match method:
        case "gradient":
            return gradient(info)
        case "constantVolume":
            return constant_volume(info)
