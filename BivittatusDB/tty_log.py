import time, threading, inspect, os

class logger:
    def __init__(self, table_name:str) -> None:
        self.table_name=table_name
        self._stop=threading.Event()
        self.logfile=table_name+".dbl" #dbl is for database log (minimal conflict found)
        self.end=False
        self.thread=self.thread_logger()

    def __del__(self):
        if hasattr(self, "fd"):
            os.remove(self.logfile)

    def thread_logger(self):
        thread=threading.Thread(target=self.logger, daemon=True)
        return thread

    def logger(self):
        open(self.logfile, "w").close() #init empty log file
        with open(self.logfile, "r") as log:
            self.fd=log.fileno()
            while self.end==False:
                line=log.readline()
                if not line:
                    time.sleep(0.1)
                    continue
                print(line)

    def start(self):
        self.thread.start()

    def write(self, message:str, log_level="INFO"):
        timestamp=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        frame=inspect.currentframe().f_back
        function_name=frame.f_code.co_name
        line_number=frame.f_lineno

        entry=f"[{timestamp}] [{log_level}] [{function_name}:{line_number}] {message}"

        with open(self.logfile, "a") as log:
            log.write(entry)
        time.sleep(0.1) #sleep because the logger can't catch up if it ends immediatley

    def stop(self):
        self.end=True
        self._stop.set()
        self.thread.join()
        del self

if __name__=='__main__':
    Logger=logger("testing")
    Logger.start()
    Logger.write("Hello World")
    time.sleep(10)
    Logger.write("Something happened", log_level="ERROR")
    Logger.stop()