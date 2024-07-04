# ShinobiShell

ShinobiShell is a simple tool for automated shellcode generation using MSFVenom and execution via C++ templates. It includes detections for virtual machines and sandboxes to help evade analysis environments.

## Features

- Automated shellcode generation with MSFVenom.
- Detection of virtual machine and sandbox environments.
- Two modes of operation:
  - Hardcoded shellcode embedding.
  - Download and execute shellcode from a remote server.

## Requirements

- Python 3
- MSFVenom
- MinGW-w64 (for cross-compiling to Windows)

## Installation

1. **Clone the repository**:
   ```sh
   git clone https://github.com/yourusername/ShinobiShell.git
   cd ShinobiShell
   ```

2. **Install dependencies**:
   Ensure you have Python 3, MSFVenom, and MinGW-w64 installed on your system.

## Usage

1. **Hardcoded Shellcode**:
   Run the tool with the `hardcoded` option and specify the LHOST.
   ```sh
   python3 shinobishell.py hardcoded <LHOST>
   ```

2. **HTTP Shellcode**:
   Run the tool with the `http` option and specify the LHOST.
   ```sh
   python3 shinobishell.py http <LHOST>
   ```

   After running the above command, the tool will:
   - Generate shellcode using MSFVenom.
   - Update the C++ template with the new shellcode.
   - Compile the C++ code to a Windows executable.
   - Move the compiled executable to the `running` directory.
   - Start a simple HTTP server to serve the shellcode.

## TO-DO

- [ ] Add more robust VM and sandbox detection techniques.
- [ ] Implement additional payload options.
- [ ] Improve error handling and user feedback.
- [ ] Add support for more payload formats and targets.
- [ ] Enhance documentation and add more usage examples.

