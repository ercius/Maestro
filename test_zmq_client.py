"""
Test client for the ZMQ servo controller
"""
import zmq
import json
import time

def send_command(socket, command):
    """Send a command and print the response"""
    print(f"\n>>> Sending: {command}")
    socket.send_string(json.dumps(command))
    response = json.loads(socket.recv_string())
    print(f"<<< Response: {response}")
    return response

def main():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    print("=" * 50)
    print("ZMQ Servo Controller Test Client")
    print("=" * 50)

    try:
        # Test all the predefined positions
        print("\n[TEST 1] Set to TIA2 position")
        send_command(socket, {"action": "set_TIA2"})
        time.sleep(0.5)

        print("\n[TEST 2] Set to Gatan position")
        send_command(socket, {"action": "set_Gatan"})
        time.sleep(0.5)

        print("\n[TEST 3] Set to TIA position")
        send_command(socket, {"action": "set_TIA"})
        time.sleep(0.5)

        print("\n[TEST 4] Set to neutral position")
        send_command(socket, {"action": "set_neutral"})
        time.sleep(0.5)

        print("\n[TEST 5] Set to custom value (7500)")
        send_command(socket, {"action": "set_value", "value": 7500})
        time.sleep(0.5)

        # Test error handling
        print("\n[TEST 6] Invalid action (should fail)")
        send_command(socket, {"action": "invalid_action"})

        print("\n[TEST 7] Missing value parameter (should fail)")
        send_command(socket, {"action": "set_value"})

        print("\n" + "=" * 50)
        print("All tests completed!")
        print("=" * 50)

    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
    except Exception as e:
        print(f"\nError: {e}")
    finally:
        socket.close()
        context.term()

if __name__ == "__main__":
    main()
