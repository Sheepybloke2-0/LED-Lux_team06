# Running the LED-Lux Demo on the NVidia TK1
#### By Reuben Lewis, Anna Little, Evan Hill, and Melanie Fox

## Materials
 - Three light boxes each containing
   - [Infinion XMC1200 Arduino Shield](https://www.infineon.com/cms/en/product/evaluation-boards/kit_led_xmc1202_as_01/)
   - Arduino Uno
   - [XBee S2C Radio](https://www.digikey.com/product-detail/en/digi-international/XB24CAWIT-001/602-1891-ND/6010100) and XBee Arduino Shield
   - Two 3000K Marktech LEDS and two 6000K Marktech LEDs
   - Two power supplies, one for the Arduino and one for the Infinion board to power the LEDs
 - One NVidia TK1 => Username = "ubuntu", Password = "ubuntu"
   - Power supply
   - 64GB microSD card with USB 3.0 SD card reader
   - Anker USB 3.0 expander
   - Logitech C920 Webcam
   - XBee S2C Radio with SparkFun FTDI USB adapter

## Lights Setup
 1. Ensure that the XBee shield is set to `Xbee` mode by checking the switch on the shield.
 2. Place the light boxes in three different areas, spaced so that each box is in
    a different region of intrest (ROI).
 3. Plug the lights in starting wih the LED driver's power cord, then the Arduino's.
 4. That's it! The lights should connect with the coordinater node once it's powered.

## Vision System Setup
 1. Connect the Anker USB 3.0 expander, monitor via HDMI, a keyboard, and mouse to
    the TK1 board and boot it.
 2. Connect and position the webcam so that it can see the light boxes and that each
    box is in it's own ROI.
 3. Connect the coordinater node XBee. This node is connected to the SparkFun FDTI USB
    adapter, and [setup](#XBeeSetup) to coordinate communication from the outside to
    the other nodes on the mesh.
 4. Open a terminal window. The files are structured like so:
    ```
    |root
    |___ media/extraSpace
                        |___ swapfile
                        |___ tensorflow
                                      |___ bin
                                      |___ models/research/object_detection/
                                                                           |___ LED-Lux_team06/WebApp/new-webapp
     ```
 5. Move to the SD card's filesystem and activate the Tensorflow virtual environment.
    Then, active the extra swap space, since the object detection loads a couple of
    large models into memory. Finally, open `/dev/ttyUSB0` to allow the program to
    access the connected XBee.
     ```
     cd /media/extraSpace
     . tensorflow/bin/activate
     sudo swapon swapfile
     sudo chmod 777 /dev/ttyUSB0
     ```
 6. Move to the `object_detection` folder and start the program. It should do a
    quick test of the lights, turning them on, dimming them, then turning them off.
    Afterwards, it loads the models into memory, meaning that it will take a bit of
    time to fully launch the system.
     ```
     cd tensorflow/models/research/object_detection
     python multithread_mobilenetv2.py
     ```
 7. Adjust the webcam to fit the lights into the ROIs.
 8. To end the demo, click on the image screen and hit `ESC`, or use `CTRL + C`
     in the terminal window.
## Webapp Setup
 1. The webapp is powered by Flask. To run it, follow the [Vison System Setup](#VisionSystemSetup)
    up to Step 6. Then, go to the webapp folder and launch it. We provide the `--host=0.0.0.0`
    option to launch the webapp on the local network so any machine on the local network
    can access it.
     ```
     cd tensorflow/models/research/object_detection/LED-Lux_team06/WebApp/new-webapp
     export FLASK_APP=app.py
     flask run --host=0.0.0.0
     ```
 2. Connect to the webapp using the IP address of the TK1 board and appending port 5000.

## Creating the TK1 Tensorflow Environment
The TK1 board uses a version of Ubuntu 14.04 that is created by NVidia. To flash the
board, you have to use NVidia's JetPack SDK. You can get access to all of it through
[here](https://developer.nvidia.com/linux-tegra-rel-21). [This post](https://devtalk.nvidia.com/default/topic/1020701/jetson-tk1/step-to-step-for-flash-jetson-tk1-/)
is pretty helpful, pointing out some stumbling blocks.
#### Building Tensorflow
Unfortunately, Tensorflow doesn't like being built on the TK1, so we have to build it
ourselves. Mostly, I followed a combination of two guides, [guide one](http://cudamusing.blogspot.jp/2015/11/building-tensorflow-for-jetson-tk1.html)
and [guide two](https://github.com/Lisandro79/JetsonCaffe/wiki/Install-Tensorflow-on-TK1).
The steps are mostly the same, except that I got the newer versions of Bazel, Protobuf,
and Tensorflow, and that I dropped the GPU support. While I tried to follow their
instructions on how to do add support, it seemed like the newer version of Tensorflow
didn't like the old GPU libraries, and trying to trick it into liking it was failing.
Following the steps as outlined in the guides will allow yout to build it.
 1. Use `/media/extraSpace/swapspace` for your swapspace
 2. Update the Bazel and Protobuf libraries to the newest versions and build them
 3. Pull down the latest version of Tensorflow as well. The vision work needs 1.4 or higher.
 4. The prompts when you're configuring the Tensorflow build will be different than
    what's written, but are pretty simple to follow.
 5. Ignore the GPU/CUDA steps to change the files.
 6. Google any issues you've have, there's a lot of support out there, and sometimes
    it's just a small config change that is hard to predict.
 7. The build command I used is this:
    ```
    $ bazel build -c opt --local_resources 2048,0.5,1.0 --verbose_failures //tensorflow/tools/pip_package:build_pip_package

    $ bazel-bin/tensorflow/tools/pip_package/build_pip_package /tmp/tensorflow_pkg

    # The name of the .whl file will depend on your platform.
    $ sudo pip install /tmp/tensorflow_pkg/tensorflow-0.5.0-cp27-none-linux_armv7l.whl
    ```

Good luck!

#### Building OpenCV
[PyImageSearch's building OpenCV tutorial](https://www.pyimagesearch.com/2015/07/20/install-opencv-3-0-and-python-3-4-on-ubuntu/)
is a great tutorial on how to build OpenCV. Before you start, ensure that you are in
in your Tensorflow virtual environment(`. /media/ubnutu/extraSpace/tensorflow/bin/activate`).
This just makes it so that OpenCV compiles into the the virutal environment automatically.
Otherwise, you may have to copy the binary from the location to the virtual environment's
binary container. Follow the examples, but be sure to install OpenCV version 3.4 or higher.
Also, when running the `cmake` command, include the
`	-D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \` line, since that adds
extra modules useful for location tracking. Other than that, following the instructions
will get OpenCV properly installed on the board.

#### Installing the FTDI Driver
To communicate with the XBee radio, you need to have the FDTI driver, which is not
standard on the image. To add, you simply have to compile a kernel driver to get it.
The process is outlined [here](https://elinux.org/Jetson/Tutorials/Program_An_Arduino).
NOTE: Ensure that the version numbers between the kernel and the driver are the
same, otherwise it won't work.

#### List of Other Packages
 - Web App
   - Flask
   - Flask wtf
   - Serial
   - Threading
   - Atexit
   - json
   - WTForms
 - Machine Vision Program
   - Numpy
   - OS
   - Time
   - Sys
   - Threading
   - Multiprocessing
   - Serial

## Reconfiguring the XBees
The XBees are configured with the `ZigBee TH Reg` function set and firmware version
`4060`. There are a total four XBee radios in the system, one coordinater and three
routers configured in a mesh network. Below are instructions to reconfigure the XBees
incase one fails.
 1. Download the [XTCU configuration program](https://www.digi.com/products/xbee-rf-solutions/xctu-software/xctu)
 2. Connect the XBee radio you want to configure to the SparkFun FTDI to USB adapter
    and plug it into your machine.
 3. Open the XTCU program in administrator mode and add a radio by clicking the
    XBee radio icon with a plus in the upper left hand corner. Select the correct
    port and add the radio.
 4. Click on the radio to read the settings into the GUI.
 5. If the issues is the firmware, click on the `Update` button and select `ZigBee TH Reg`
    and `4060` as the version.
 6. Next, configure the settings. Most default settings can stay; however, some
    need to be configured specifically for our network. Below is a list of settings
    for both the coordinator and the routers.

    For the Coordinator
    ```
    PAN ID                      = 12
    Channel Varification        = Enabled [1]
    Coordinator Enable          = Enabled [1]
    DH Destination Address High = 0
    DL Destination Address Low  = FFFF # Set it to send all routers
    NI Node Identifier          = Coordinator
    AP API Enable               = Transparent Mode [0]
    ```

    For the Routers
    ```
    PAN ID                      = 12
    Channel Varification        = Enabled [1]
    Coordinator Enable          = Disabled [0]
    DH Destination Address High = 0
    DL Destination Address Low  = 0 # Set it to send messages to the coordinator
    NI Node Identifier          = First Node # or Second, or Third
    AP API Enable               = Transparent Mode [0]
    ```
 7. Finally, write the configs and connect the XBee radios to the Arduinos. Using
    shields, the different pins should connect automatically. However, these are
    the important pins that are connected.

| XBee Connection | Arduino Pin |
|-----------------|-------------|
| Vcc Pin 1       | 3.3v        |
| GND Pin 10      | GND         |
| DOUT Pin 2      | RX Pin 0    |
| DIN Pin 3       | TX Pin 1    |

#### Other Useful Things with XCTU
XCTU is really powerful in XBee development. Some useful resources include the
console (`ALT+SHIFT+s`), which allows you to send out serial signals to the other
connected XBee radios. You can also do a range test, analyze the spectrum sent,
and recover a broke XBee radio.
## Using the LED Driver
