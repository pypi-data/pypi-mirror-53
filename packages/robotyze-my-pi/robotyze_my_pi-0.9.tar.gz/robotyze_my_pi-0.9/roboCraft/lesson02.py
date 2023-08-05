import mcpi.minecraft as mc

def blockLine(direction,length, blockType):
    playerPos = mc.player.getPos()
    forward = ["forward", "Forward", "FORWARD", "STRAIGHT"]
    backward = ["back", "backward", "reverse", "BACK"]
    left = ["LEFT", "Left", "left"]
    right = ["RIGHT", "Right", "right"]
    up = ["UP", "Up", "up", "fly"]
    down = ["Lower", "low", "Down", "DOWN", "down"]

    xVal = 0
    yVal = 0
    zVal = 0

    if direction in forward:
        xVal = x + length
    elif direction in backward:
        xVal = x - length
    elif direction in up:
        yVal = y + length
    elif direction in down:
        yVal = y - length
    if direction in left:
        zVal = z + length
    elif direction in right:
        zVal = z - length

    block.setBlocks(playerPos.x, playerPos.y, playerPos.z, playerPos.x + xVal,
                    playerPos.y + yVal, playerPos.z + 5 + zVal, blockType)

def wall(length, height, blockType):
    playerPos = mc.player.getPos()
    block.setBlocks(playerPos.x, playerPos.y, playerPos.z + 5, playerPos.x + length,
                    playerPos.y + height, playerPos.z + 5, blockType)

def box(size, blockType):
    playerPos = mc.player.getPos()
    block.setBlocks(playerPos.x, playerPos.y, playerPos.z, playerPos.x + size,
                    playerPos.y + size, playerPos.z + size + 5, blockType)
