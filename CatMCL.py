import minecraft_launcher_lib, subprocess, sys 
from PyQt5.QtWidgets import QApplication, QMainWindow, QProgressBar, QVBoxLayout, QWidget 
from PyQt5.QtCore import QThread, pyqtSignal 
class DownloadThread(QThread): 
    progress_changed = pyqtSignal(int) 
    forge_ver = ""
    letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "_", "-", "к", "о", "т", "я", "р", "а", "п", "/"]
    def get_username(self, filename):
        newFilename = ""
        name = ""
        if ".txt" in filename:
            for i in range(0, len(filename)):
                if filename[i] == "." and filename[i+1] = "t" and filename[i+2] = "x" and filename[i+3] = "t":
                    break
                else:
                    newFilename += filename[i]    
        else:
            pass
        file = open(newFilename + ".txt", "r")
        nameOld = file.read().lower()
        for i in range(0, len(nameOld)):
            if nameOld[i] == " ":
                continue
            else:
                if nameOld[i] in letters:
                    name += nameOld[i]
                else:
                    continue
        file.close()
        return name
    def run(self): 
        options = { 
            "username": self.get_username("username"), 
            "uuid": "user-uuid", 
            "token": "user-token", 
            "version": f"forge {self.forge_ver}", 
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
