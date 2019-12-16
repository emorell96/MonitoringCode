import time
from datetime import datetime
import serial
from threading import Event, Thread, Timer
class RepeatedTimer:

    """Repeat `function` every `interval` seconds."""

    def __init__(self, interval, max_runs, function, closefunc, *args, **kwargs):
        #set max_runs = -1 to inf
        self.max_runs = max_runs
        self.interval = interval
        self.closefunc = closefunc
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.runs = 0
        self.start = time.time()
        self.event = Event()
        self.thread = Thread(target=self._target)
        self.thread.start()


    def _target(self):
        while not self.event.wait(self._time):
            self.function(*self.args, **self.kwargs)
            self.runs += 1
            if(not self.runs % 100):
                print("Function {2} has run {0} times, {1} times to go.".format(self.runs, self.max_runs - self.runs if self.max_runs > 0 else "infinity", self.function.__name__))
                print("To stop press Ctrl C")
            if(self.max_runs > 0 and self.runs >= self.max_runs):
                print("Closing: calling {0}".format(self.closefunc.__name__))
                self.closefunc()
                print("Closed: called {0} succesfully".format(self.closefunc.__name__))
                self.stop()
                break
            


    @property
    def _time(self):
        return self.interval - ((time.time() - self.start) % self.interval)

    def stop(self):
        self.event.set()
        #self.thread.join()
        #agilent.close()
        #update config file
        #configParser.set('Output Settings', 'next_out', '{0}'.format(next_out+1))
        #with open(config_file, 'w') as configfile:
        #    configParser.write(configfile)
def test():
    print("test ran")
    
#RepeatedTimer(2, 4, test, test)