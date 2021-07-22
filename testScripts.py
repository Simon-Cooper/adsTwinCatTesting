def pointMoves(axis,velocity):
    while True:
        print("Input target position")
        pos = input()
        try:
            pos = float(pos)
        except ValueError:
            print("Not a valid position. Exiting routine...")
            break
        axis.moveRelative(pos,velocity)
        if axis.waitForDone() == False:
            break
