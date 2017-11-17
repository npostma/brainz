import sys, time
from PyQt4 import QtGui

from Drawable import Label, Point
from MRI import GUI, Canvas
from AI import Brain

brain = Brain.Brain(9, 3)
app = QtGui.QApplication(sys.argv)

canvas = Canvas.Canvas()
gui = GUI.GUI(brain, canvas)

for (index) in range(0, 1000):
    # Traning set 0, No shipment and some order changes: Order won't go to the accountant. Order does not get changed anymore
    #brain.learn([1, 0.09, 0, 0.04, 0.01, 0.00], [0, 0.3])
    # brain.learn([1, 0.13, 0, 0.04, 0.01, 0.00], [0, 0.4])
    brain.learn([0, 0.09, 0, 0.04, 0.01, 0.00, 2,3,4], [1, 0.3, 1])
    brain.learn([0, 0.14, 0, 0.04, 0.01, 0.00,8,9,10], [1, 0.4, 1])

    gui.update();


    # Prevent main application from freezing!
    app.processEvents()


    # time.sleep(0.01)


sys.exit(app.exec_())
