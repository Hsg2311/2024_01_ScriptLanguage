from tkinter import *
from threading import Thread, Semaphore
from GIFAnimation import *
import GuiConfig

class Loading:
    def initGif():
        Loading.gif = GIFAnimation('res/richard.gif', 364, 248)

    def __init__(self, master, task, callback):
        self.master = master
        self.callback = callback
        self.sem = Semaphore(0)  # Initialize with 0 to block
        self.result = None
        self.taskThread = Thread(target=self.__runTask, args=(task,))
        self.taskThread.start()
        self.elapsedMs = 0

        self.window = None
        self.master.after(15, self.__checkDone)  # Start periodic check

    def __initWindow(self):
        self.window = Toplevel(self.master)
        self.window.title("Loading")
        
        self.gif = Loading.gif
        self.gifLabel = Label(self.window, image=self.gif.image())
        self.gifLabel.pack(padx=20)
        self.window.after(100, self.update)

        self.txtLoading = StringVar()
        self.txtLoading.set("Loading")
        self.txtLabel = Label(self.window, textvariable=self.txtLoading,
            font=GuiConfig.cFont
        )
        self.txtLabel.pack(pady=20)
        self.txtFrame = 0

    def update(self):
        self.gif.advance()
        self.gifLabel.configure(image=self.gif.image())

        self.txtFrame = (self.txtFrame + 1) % 20
        txtDotCnt = self.txtFrame // 5
        self.txtLoading.set("Loading" + "." * txtDotCnt)

        self.window.after(100, self.update)

    def __runTask(self, task):
        self.result = task()
        self.sem.release()

    def __checkDone(self):
        self.elapsedMs += 15
        if self.sem.acquire(blocking=False):
            if self.window is not None:
                self.window.destroy()
            self.callback(self.result)  # 작업 완료 후 콜백 호출
        else:
            if self.window is None and self.elapsedMs >= 150:
                self.__initWindow()
            self.master.after(15, self.__checkDone)

# Test task
def test_task():
    import time
    time.sleep(3)
    return "Task completed"

# Task completion callback
def on_task_complete(result):
    print('Task result:', result)
    label.config(text=f"Result: {result}")


if __name__ == "__main__":
    # Test Tkinter window
    root = Tk()
    root.title("Main Window")

    label = Label(root, text="Click the button to start the task")
    label.pack(pady=20)

    button = Button(root, text="Start Task", command=lambda: Loading(root, test_task, on_task_complete))
    button.pack(pady=20)

    root.mainloop()