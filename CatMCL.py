import minecraft_launcher_lib, subprocess
import sys 
from PyQt5.QtWidgets import QApplication, QMainWindow, QProgressBar, QVBoxLayout, QWidget 
from PyQt5.QtCore import QThread, pyqtSignal 
import minecraft_launcher_lib 
def get_username(filename):
    file = open(filename + ".txt", "r")
    name = file.read()
    file.close()
    return name
class DownloadThread(QThread): 
    progress_changed = pyqtSignal(int) 
    def run(self): 
        options = { 
            "username": get_username("username.txt"), 
            "uuid": "user-uuid", 
            "token": "user-token", 
            "version": "launcher_version", 
            "path": ".CatLaunchMC" # minecraft_launcher_lib.utils.get_minecraft_directory().replace('minecraft', 'CatMCLauncher')
            "callback": { 
                "setStatus": self.set_status, 
                "setProgress": self.set_progress, 
            } 
        } 
        # minecraft_launcher_lib.install.install_minecraft_version(versionid=options["version"], minecraft_directory=options["path"], callback=options["callback"]) 
        subprocess.call(minecraft_launcher_lib.command.get_minecraft_command(version=options["version"], minecraft_directory=options["path"], options=options))
    def set_status(self, text): 
        print(text) 
    def set_progress(self, progress): 
        self.progress_changed.emit(int(progress * 100)) 
class MainWindow(QMainWindow): 
    def __init__(self): 
        super().__init__() 
        self.setWindowTitle("CatMCLaunch") 
        self.setGeometry(100, 100, 400, 200) 
        self.progress_bar = QProgressBar(self) 
        self.progress_bar.setGeometry(50, 80, 300, 30) 
        self.progress_bar.setMaximum(100) 
        self.download_thread = DownloadThread() 
        self.download_thread.progress_changed.connect(self.update_progress) 
        self.download_thread.start() 
    def update_progress(self, value): 
        self.progress_bar.setValue(value) 
if __name__ == "__main__": 
    app = QApplication(sys.argv) 
    window = MainWindow() 
    window.show() 
    sys.exit(app.exec_())