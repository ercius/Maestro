import sys
import tkinter as tk
import time
import zmq
import json
import threading

sys.path.append('c:/users/supervisor/utilities/maestro/')
import maestro

"""
position_neutral = 7080
position_TIA = 6532 TIA2 = 6400
position_Gatan = 8000
"""

class ZMQServer:
    def __init__(self, app, port=5555):
        self.app = app
        self.port = port
        self.running = False
        self.thread = None

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._run_server, daemon=True)
        self.thread.start()
        print(f"ZMQ server started on port {self.port}")

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=1)
        print("ZMQ server stopped")

    def _run_server(self):
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind(f"tcp://*:{self.port}")
        socket.setsockopt(zmq.RCVTIMEO, 1000)

        while self.running:
            try:
                message = socket.recv_string()
                response = self._handle_command(message)
                socket.send_string(json.dumps(response))
            except zmq.Again:
                continue
            except Exception as e:
                error_response = {"status": "error", "message": str(e)}
                try:
                    socket.send_string(json.dumps(error_response))
                except:
                    pass

        socket.close()
        context.term()

    def _handle_command(self, message):
        try:
            command = json.loads(message)
            action = command.get("action")

            if action == "set_TIA":
                self.app.set_TIA()
                return {"status": "success", "action": "set_TIA"}
            elif action == "set_TIA2":
                self.app.set_TIA2()
                return {"status": "success", "action": "set_TIA2"}
            elif action == "set_Gatan":
                self.app.set_Gatan()
                return {"status": "success", "action": "set_Gatan"}
            elif action == "set_neutral":
                self.app.set_neutral()
                return {"status": "success", "action": "set_neutral"}
            elif action == "set_value":
                value = command.get("value")
                if value is None:
                    return {"status": "error", "message": "value parameter required"}
                self.app.set_value(value)
                return {"status": "success", "action": "set_value", "value": value}
            else:
                return {"status": "error", "message": f"Unknown action: {action}"}
        except json.JSONDecodeError:
            return {"status": "error", "message": "Invalid JSON"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

class App(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()
        
        self.button_TIA = tk.Button(text="TIA", width=25, height=5, bg="yellow",fg="black",command=self.set_TIA2)
        self.button_TIA.pack()
        
        self.button_Gatan = tk.Button(text="Gatan", width=25, height=5, bg="gray",fg="black",command=self.set_Gatan)
        self.button_Gatan.pack()
        
        self.set_TIA2()
        
    def set_TIA(self,):
        with maestro.Controller(ttyStr='COM4') as servo:
            position = 6532
            # 10 is a good speed
            servo.setSpeed(1, 10)

            x = servo.getPosition(1) #get the current position of servo 1
            print('Starting position = {}'.format(x))
        
            servo.setTarget(1, position)
            time.sleep(3)
            y = servo.getPosition(1) #get the current position of servo 1
            print('new position = {}'.format(y))
            
        self.button_TIA['background'] = 'yellow'
        self.button_Gatan['background'] = 'gray'
            
    def set_TIA2(self,):
        with maestro.Controller(ttyStr='COM4') as servo:
            position = 6400
            # 10 is a good speed
            servo.setSpeed(1, 10)

            x = servo.getPosition(1) #get the current position of servo 1
            print('Starting position = {}'.format(x))
        
            servo.setTarget(1, position)
            time.sleep(3)
            y = servo.getPosition(1) #get the current position of servo 1
            print('new position = {}'.format(y))
            
        self.button_TIA['background'] = 'yellow'
        self.button_Gatan['background'] = 'gray'
            
            
    def set_Gatan(self,):
        with maestro.Controller(ttyStr='COM4') as servo:
            position = 8000

            # 10 is a good speed
            servo.setSpeed(1, 10)

            x = servo.getPosition(1) #get the current position of servo 1
            print('Starting position = {}'.format(x))
        
            servo.setTarget(1, position)
            time.sleep(3)
            y = servo.getPosition(1) #get the current position of servo 1
            print('new position = {}'.format(y))
        
        self.button_Gatan['background'] = 'yellow'
        self.button_TIA['background'] = 'gray'
            
    def set_neutral(self,):
        with maestro.Controller(ttyStr='COM4') as servo:
            position = 7080

            # 10 is a good speed
            servo.setSpeed(1, 10)

            x = servo.getPosition(1) #get the current position of servo 1
            print('Starting position = {}'.format(x))

            servo.setTarget(1, position)

            time.sleep(3)

            y = servo.getPosition(1) #get the current position of servo 1
            print('new position = {}'.format(y))

        self.button_TIA['background'] = 'gray'
        self.button_Gatan['background'] = 'gray'
            
    def set_value(self,val):
        with maestro.Controller(ttyStr='COM4') as servo:
            position = val

            # 10 is a good speed
            servo.setSpeed(1, 10)

            x = servo.getPosition(1) #get the current position of servo 1
            print('Starting position = {}'.format(x))
        
            servo.setTarget(1, position)
            
            time.sleep(3)
            
            y = servo.getPosition(1) #get the current position of servo 1
            print('new position = {}'.format(y))
    
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Scan selector")
    #root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file=r'C:\Users\Supervisor\Pictures\TIA-Gatan.ico')
    myapp = App(root)

    # Start ZMQ server
    zmq_server = ZMQServer(myapp, port=5555)
    zmq_server.start()

    # Ensure server stops when window closes
    def on_closing():
        zmq_server.stop()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    myapp.mainloop()