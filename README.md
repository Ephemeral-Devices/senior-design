# Adaptive Correlative Microscopy System
2022 Senior Design Project by Tyler Wright and Jack Hymowitz. 

Proof of concept that can be adapted to support additional hardware for a correlative microscopy system.
- Python code for controlling electron and optical microscopes
- Designed to interface with Thorlabs scientific equipment
- Can be run locally or remotely through OPC-UA

The OPC-UA architecture contains four nodes:
- `opcua-microscope-server` can live on a remote or local machine and can send movement instructions to the client
- `opcua-microscope-client` interfaces with a machine that is connected to the stage and will tell the hardware to move
- `camclient` interfaces with the camera and streams the live feed to `camserver`
- `camserver` tells `camclient` to start and receives the camera feed

# Setup
1. Clone this repo in your desired project directory on a computer with direct access to the microscope stage and camera
2. Download the Thorlabs Kinesis Example Projects from [here](https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=10285) and edit the DLL paths in `opcua-microscope-client` to match your download path
3. Download the [Thorlabs Windows SDK for Scientific Cameras](https://www.thorlabs.com/software_pages/viewsoftwarepage.cfm?code=ThorCam) and extract into your project directory. Navigate to `Scientific Camera Interfaces/Python_README.txt` and follow the instructions
4. Note that the IP addresses of each node will need to be slightly different. It is recommended to pick an address for one node and have each subsequent node be similar, ie `10.0.1.1` and `10.0.1.2` for client and server respectively 
5. You should now be able to run `opcua-microscope-client` and `camclient`! `opcua-microscope-server` and `camserver` may either be run on the same or a separate machine, and need only be clone and run

Special thanks to Prof. Kevin Lu and Terrence McGuckin for helping us make this happen!
