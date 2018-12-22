from logic import *

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    w.initialize_game()
    sys.exit(app.exec_())
