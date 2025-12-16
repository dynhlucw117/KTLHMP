import serial
import time
import sys

DEFAULT_PORT = 'COM3'
DEFAULT_BAUDRATE = 115200

class UbootController:
    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate
        self.ser = None
        
    def connect(self):
        try:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=1
            )
            print(f"[SUCCESS] {self.port} @ {self.baudrate} bps")
            time.sleep(1)
            
            # Clear buffer
            if self.ser.in_waiting > 0:
                self.ser.read(self.ser.in_waiting)
            
            return True
        except Exception as e:
            print(f"[ERROR]: {e}")
            return False
    
    def read_serial(self, timeout=3):
        start_time = time.time()
        data = ""
        
        while time.time() - start_time < timeout:
            if self.ser.in_waiting > 0:
                chunk = self.ser.read(self.ser.in_waiting).decode('utf-8', errors='ignore')
                data += chunk
                # sys.stdout.write(chunk) # output
                # sys.stdout.flush()
            time.sleep(0.05)
        
        return data
    
    def send_command(self, command, wait_time=1):
        print(f"[COMMAND] : {command}")
        self.ser.write(command.encode('utf-8') + b'\r\n')
        time.sleep(wait_time)
        response = self.read_serial(timeout=2)
        return response
    
    def send_commands(self, commands, delay_between_commands=1):
        results = []
        
        for i, command in enumerate(commands, 1):
            result = self.send_command(command, delay_between_commands)
            results.append({
                'command': command,
                'response': result
            })
            # print("-" * 50)
        
        return results
    
def execute_cmdArray():
    controller = UbootController(DEFAULT_PORT, DEFAULT_BAUDRATE)
    if not controller.connect():
        return
    try:
        commands = [
            "cd /tmp",
            "tftp -l busybox -r busybox -g 192.168.1.100 & chmod 777 busybox",
            "./busybox telnetd -l /bin/sh -p 23",
            "tftp -l gdbserver -r gdbserver -g 192.168.1.100 & chmod 777 gdbserver",
            "tftp -l strace -r strace -g 192.168.1.100 & chmod 777 strace",
            "tftp -l remote.sh -r remote.sh -g 192.168.1.100 & chmod 777 remote.sh"
        ]
        results = controller.send_commands(commands, delay_between_commands=1)          
    except KeyboardInterrupt:
        print("\nSTOP")

if __name__ == "__main__":
    execute_cmdArray()
