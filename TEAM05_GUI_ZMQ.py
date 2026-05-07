import sys
import argparse
import tkinter as tk
import time
import zmq
import json
import threading

# sys.path.append('c:/users/supervisor/utilities/maestro/')
import maestro


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
            elif action == "set_Gatan":
                self.app.set_Gatan()
                return {"status": "success", "action": "set_Gatan"}
            elif action == "set_Arina":
                self.app.set_Arina()
                return {"status": "success", "action": "set_Arina"}
            else:
                return {"status": "error", "message": f"Unknown action: {action}"}
        except json.JSONDecodeError:
            return {"status": "error", "message": "Invalid JSON"}
        except Exception as e:
            return {"status": "error", "message": str(e)}


class App(tk.Frame):
    def __init__(self, master, com_port, channels, engaged, neutrals):
        super().__init__(master)
        self.com_port = com_port
        self.channels = channels  # {"TIA": int, "Gatan": int, "Arina": int}
        self.engaged = engaged    # {"TIA": int, "Gatan": int, "Arina": int}
        self.neutrals = neutrals  # {"TIA": int, "Gatan": int, "Arina": int}
        self.pack()

        self.button_TIA = tk.Button(text="TIA", width=25, height=5, bg="gray", fg="black", command=self.set_TIA)
        self.button_TIA.pack()

        self.button_Gatan = tk.Button(text="Gatan", width=25, height=5, bg="gray", fg="black", command=self.set_Gatan)
        self.button_Gatan.pack()

        self.button_Arina = tk.Button(text="Arina", width=25, height=5, bg="gray", fg="black", command=self.set_Arina)
        self.button_Arina.pack()

    def _move_all(self, positions):
        with maestro.Controller(ttyStr=self.com_port) as servo:
            for channel, position in positions.items():
                servo.setSpeed(channel, 10)
                x = servo.getPosition(channel)
                print(f"Channel {channel} starting position = {x}")
                servo.setTarget(channel, position)
            time.sleep(3)
            for channel in positions:
                y = servo.getPosition(channel)
                print(f"Channel {channel} new position = {y}")

    def _highlight(self, active):
        active_colors = {"TIA": "yellow", "Gatan": "cyan", "Arina": "orange"}
        for name, button in [("TIA", self.button_TIA), ("Gatan", self.button_Gatan), ("Arina", self.button_Arina)]:
            button["background"] = active_colors[name] if name == active else "gray"

    def set_TIA(self):
        self._move_all({
            self.channels["TIA"]:   self.engaged["TIA"],
            self.channels["Gatan"]: self.neutrals["Gatan"],
            self.channels["Arina"]: self.neutrals["Arina"],
        })
        self._highlight("TIA")

    def set_Gatan(self):
        self._move_all({
            self.channels["TIA"]:   self.neutrals["TIA"],
            self.channels["Gatan"]: self.engaged["Gatan"],
            self.channels["Arina"]: self.neutrals["Arina"],
        })
        self._highlight("Gatan")

    def set_Arina(self):
        self._move_all({
            self.channels["TIA"]:   self.neutrals["TIA"],
            self.channels["Gatan"]: self.neutrals["Gatan"],
            self.channels["Arina"]: self.engaged["Arina"],
        })
        self._highlight("Arina")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scan selector GUI with ZMQ server")
    parser.add_argument("--com-port", default="COM10", help="Serial COM port (default: COM10)")
    parser.add_argument("--zmq-port", type=int, default=5555, help="ZMQ server port (default: 5555)")

    # Servo channels
    parser.add_argument("--tia-channel",   type=int, default=1, help="Servo channel for TIA (default: 1)")
    parser.add_argument("--gatan-channel", type=int, default=2, help="Servo channel for Gatan (default: 2)")
    parser.add_argument("--arina-channel", type=int, default=3, help="Servo channel for Arina (default: 3)")

    # Engaged positions (set these once servos are installed)
    parser.add_argument("--tia-engaged",   type=int, default=6400, help="TIA engaged position (default: 6400)")
    parser.add_argument("--gatan-engaged", type=int, default=8000, help="Gatan engaged position (default: 8000)")
    parser.add_argument("--arina-engaged", type=int, default=6000, help="Arina engaged position (default: 6000)")

    # Neutral positions (can differ per servo)
    parser.add_argument("--tia-neutral",   type=int, default=7080, help="TIA neutral position (default: 7080)")
    parser.add_argument("--gatan-neutral", type=int, default=7080, help="Gatan neutral position (default: 7080)")
    parser.add_argument("--arina-neutral", type=int, default=7080, help="Arina neutral position (default: 7080)")

    args = parser.parse_args()

    channels = {"TIA": args.tia_channel,   "Gatan": args.gatan_channel,   "Arina": args.arina_channel}
    engaged  = {"TIA": args.tia_engaged,   "Gatan": args.gatan_engaged,   "Arina": args.arina_engaged}
    neutrals = {"TIA": args.tia_neutral,   "Gatan": args.gatan_neutral,   "Arina": args.arina_neutral}

    root = tk.Tk()
    root.title("Scan selector")
    myapp = App(root, args.com_port, channels, engaged, neutrals)

    zmq_server = ZMQServer(myapp, port=args.zmq_port)
    zmq_server.start()

    def on_closing():
        zmq_server.stop()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    myapp.mainloop()
