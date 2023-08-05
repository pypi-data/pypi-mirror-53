import mcpi.minecraft as mc
import time
import roboCommands.networking as nc

user = "user"

ip = "ip"

def startModding():
    ip = nc.findIP()
    mc = minecraft.Minecraft.create()
    mc.postToChat("Watch out, " + user + " at " + ip + " is in modding mode.")
    time.sleep(5)


def teleport(direction):
    direction = input("Which way do you want to teleport? (forward, backward, left, right, up, down)")

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
        xVal = 10
    elif direction in backward:
        xVal = -10
    elif direction in down:
        yVal = -10
    elif direction in up:
        yVal = 10
    if direction in left:
        zVal = -10
    elif direction in right:
        zVal = 10

    mc.player.setPos(playerPos.x + xVal, playerPos.y + yVal, playerPos.z + zVal)
    mc.postToChat("Dont look down")
    time.sleep(5)
