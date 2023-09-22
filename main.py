import mido
import mido.backends.rtmidi
import requests
from datetime import datetime
import time

#Lower Thirds ON Trigger, Lower Thirds OFF Trigger, Slides, Main, Left, Split Screen, YT presenter ON, YT presenter OFF
#Lower Thirds forced OFF
MIDILoc = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
CompLoc = ["1/1", "1/2", "1/3", "1/4", "1/5", "1/6", "1/7", "1/8", "2/1", "2/2", "2/3", "2/4", "2/5", "2/6", "2/7", "2/8"]

def Log(e):
    with open("ProclaimAutomationLog.txt", "a") as f:
        f.write(str(datetime.now()) + str(e))
        return str(e)

def CompanionTrigger(MIDI):
    try:
        requests.get("http://127.0.0.1:8000/press/bank/" + CompLoc[MIDILoc.index(MIDI)])
    except Exception as e:
        print("Change the Companion interface to be running on 127.0.0.1:8000\n" + Log(e))
        time.sleep(20)

def main(LowerThirds):
    while True:
        while inport.closed:
            print(Log("LoopMIDI Not running 'ProclaimCompanion' correctly"))
        msg = inport.receive()
        MIDI = int(str(msg).split(" ")[2].split("=")[1])
        if MIDI in MIDILoc:
            if (MIDI == 1 and LowerThirds is True) or (MIDI == 2 and LowerThirds is False):
                break
            elif MIDI == 1:
                LowerThirds = True
                CompanionTrigger(MIDI)
            elif MIDI == 2:
                LowerThirds = False
                CompanionTrigger(MIDI)
            else:
                CompanionTrigger(MIDI)

if __name__ == "__main__":
    print("Just close the window to stop automation...")

    try:
        inport = mido.open_input("ProclaimCompanion 0")
        print(Log("Running..."))
        connected = True
    except Exception as e:
        print("LoopMIDI Not running 'ProclaimCompanion' correctly\nPlease re-run program\n" + Log(e))
        time.sleep(20)
        connected = False

    if connected:
        CompanionTrigger(9)
        main(LowerThirds = False)
