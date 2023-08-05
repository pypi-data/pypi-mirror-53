import cv2
import threading
import numpy as np

class VideoCaptureThreading():
    """
    source: https://github.com/gilbertfrancois/video-capture-async
    """
    
    def __init__(self, src=0, width=640, height=480):
        """
        """
        
        self.src = src
        self.cap = cv2.VideoCapture(self.src)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.grabbed, self.frame = self.cap.read()
        self.started = False
        self.read_lock = threading.Lock()

    # def set(self, var1, var2):
    #     self.cap.set(var1, var2)

    def start(self):
        """
        """
        
        if self.started:
            print('[!] Threaded video capturing has already been started.')
            return
        
        self.started = True
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.start()
        
        return self

    def update(self):
        """
        """
        
        while self.started:
            
            grabbed, frame = self.cap.read()
            
            with self.read_lock:
                self.grabbed = grabbed
                self.frame = frame

    def read(self):
        """
        """
        
        with self.read_lock:
            frame = self.frame.copy()
            grabbed = self.grabbed
            tick = cv2.getTickCount()
            
        return grabbed, frame, tick

    def stop(self):
        """
        """
        
        self.started = False
        self.thread.join()

    def __exit__(self):
        """
        """
        
        self.cap.release()
        cv2.destroyAllWindows()
        
class PlayStationEye():
    """
    """
    
    def __init__(self, i=0, fps=60, res=(640,480), codec='XVID'):
        """
        """
        
        self.ticks = []
        self.timestamps = None
        self.intervals = None
        
        self.fps = fps
        self.res = res
        self.codec = codec
        
        self.started = False
        self.cap = VideoCaptureThreading(i,width=res[0],height=res[1])
    
    def start_video_capture(self, dst):
        """
        """
        
        fourcc = cv2.VideoWriter_fourcc(*self.codec)
        self.stream = cv2.VideoWriter(dst,fourcc,self.fps,self.res)
        self.cap.start()
        
        self.started = True
        self.thread = threading.Thread(target=self._video_capture_loop, args=())
        self.thread.start()
        
        return self
    
    def _video_capture_loop(self):
        """
        """
        
        cycle_offset = 0 # TODO: measure the difference of target and actual frame interval time
        cycle_dur = 1/self.fps*cv2.getTickFrequency()-cycle_offset
        cycle_end = cycle_dur+cv2.getTickCount()
        
        while self.started:
            
            while True:
                if cv2.getTickCount() >= cycle_end:
                    cycle_end = cv2.getTickCount()+cycle_dur
                    break
                    
            ret,frame,tick = self.cap.read()
            
            if ret == True:
                
                # write the frame
                self.stream.write(frame)
                
                # collect frame timestamp
                self.ticks.append(tick)
         
        self.cap.stop()   
        self.cap.__exit__()
    
    def stop_video_capture(self):
        """
        """
        
        self.started = False
        self.thread.join()
        
        self.ticks = np.array(self.ticks)
        self.timestamps = (self.ticks-self.ticks[0])/cv2.getTickFrequency()
        self.intervals = np.diff(self.timestamps)