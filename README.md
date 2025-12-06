# Raspberry Pi Script: Sports API Display

Setting up the code to display the sports scores from [the API](https://github.com/codemis/sports-api).

## Install Python

First install all necessary libraries.

### update packages

```
sudo apt update && sudo apt upgrade -y
```

### install build tools and Python deps

```
sudo apt install -y git build-essential python3-dev python3-pip python3-pillow libgraphicsmagick++-dev libwebp-dev cython3 python3-setuptools python3-pip python3-wheel python3-distutils-extra
```

### clone the rpi-rgb-led-matrix repo

```
sudo su
cd ~
git clone https://github.com/hzeller/rpi-rgb-led-matrix.git
cd rpi-rgb-led-matrix
```

### initialize submodules (important)

```
git submodule update --init --recursive
```

### build the C++ code & python bindings

```
make build-python
```

### install python bindings system-wide

```
sudo make install-python
```

## Some Settings Updates

### Disable OnBoard Audio

Onboard audio causes conflicts.

```
# add dtparam=audio=off
sudo nano /boot/firmware/config.txt
# add blacklist snd_bcm2835
sudo nano /etc/modprobe.d/disable-bcm-audio.conf
sudo update-initramfs -u
```

```
# add isolcpus=3
sudo nano /boot/firmware/cmdline.txt
sudo reboot
```

## Demo Text Script

### Set Up Directory

```
sudo su
mkdir -p /opt/matrix_test
cd /opt/matrix_test
mkdir fonts
cp ~/rpi-rgb-led-matrix/fonts/7x13.bdf /opt/matrix_test/fonts/
nano run.py
```

Here is the basing code for a 4mm pitch:

```
#!/usr/bin/env python3
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import time

# --- configure matrix here ---
options = RGBMatrixOptions()
options.rows = 32                # panel height
options.cols = 64                # panel width
options.chain_length = 1         # number of chained panels
options.parallel = 1             # usually 1 for single bonnet
options.gpio_slowdown = 2        # adjust if display is garbled
options.hardware_mapping = 'adafruit-hat-pwm'  # <-- correct attribute
# --------------------------------

matrix = RGBMatrix(options=options)
canvas = matrix.CreateFrameCanvas()

font = graphics.Font()
font.LoadFont("fonts/7x13.bdf")

text = "Hello There!"
text_color = graphics.Color(255, 128, 0)

pos = canvas.width

try:
    while True:
        canvas.Clear()
        len_text = graphics.DrawText(canvas, font, pos, 20, text_color, text)
        pos -= 1
        if (pos + len_text < 0):
            pos = canvas.width
        canvas = matrix.SwapOnVSync(canvas)
        time.sleep(0.03)
except KeyboardInterrupt:
    matrix.Clear()
```

### Run the script

First make it executable:

```
chmod +x /opt/matrix_test/run.py
```

Then run the script:

```
cd /opt/matrix_test
sudo ./run.py
```

### Demo Image Script

First, we need to install some libraries. First create a virtual environment for the script:

```
cd /opt/matrix_test/
# Important allow the virtual environment to access the system install packages
python3 -m venv --system-site-packages venv
source ./venv/bin/activate
```

Now that you are using that environment, you can install the necessary libraries:

```
pip3 install --upgrade pip
pip3 install pillow
```

Move an image to be used using scp:

```
scp path/to/cow.png [USER]@[IP ADDRESS]:~/
# ssh, and move it to an images directory
mkdir /opt/matrix_test/images/
sudo su
mv cow.png /opt/matrix_test/images/
chown -R root:root /opt/matrix_test
```

#### The Script

```
cd /opt/matrix_test/
nano run.py
```

Add this code:

```
#!/usr/bin/env python3
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from PIL import Image
import time
import os

# --- Base directory ---
BASE_DIR = "/opt/matrix_test"  # change this if your folder moves

# --- Matrix configuration ---
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat-pwm'
options.gpio_slowdown = 2

matrix = RGBMatrix(options=options)
canvas = matrix.CreateFrameCanvas()

# --- Load image ---
image_path = os.path.join(BASE_DIR, "images", "cow.png")
image = Image.open(image_path).convert("RGB")
matrix_height = 32
image_ratio = image.width / image.height
new_height = matrix_height
new_width = int(matrix_height * image_ratio)  # keep aspect ratio

# Optionally, limit width to half the matrix width (e.g., 32 for a 64-wide matrix)
new_width = min(new_width, 32)

image = image.resize((new_width, new_height))

# --- Load font ---
font_path = os.path.join(BASE_DIR, "fonts", "7x13.bdf")
font = graphics.Font()
font.LoadFont(font_path)

text_pos = canvas.width
text_color = graphics.Color(0, 255, 0)
text = "Mooooo!"

# --- Display loop ---
try:
    while True:
        canvas.Clear()

        # --- Draw the text first ---
        graphics.DrawText(canvas, font, text_pos, 20, text_color, text)

        # --- Draw the image on top ---
        canvas.SetImage(image, 0, 0)

        canvas = matrix.SwapOnVSync(canvas)

        # Move text left
        text_pos -= 1
        text_width = graphics.DrawText(canvas, font, 0, 0, text_color, text)
        if text_pos + text_width < 0:
            text_pos = canvas.width  # reset to right side

        time.sleep(0.03)
except KeyboardInterrupt:
    matrix.Clear()
```

Now run the script using the environment:

```
source ./venv/bin/activate
sudo ./venv/bin/python run.py
```

## Security

We now need to secure the Pi from outside threats.

## Enable SSH Key Login

```
sudo su
cd /home/[USER]
mkdir .ssh
chmod 700 .ssh
#  Add your key to the file
nano .ssh/authorized_keys
chmod 600 .ssh/authorized_keys
chown -R [USER]:[USER] .ssh/
```

- From a different Terminal window, try logging in.
- Remove root ssh access

```
sudo su
nano /etc/ssh/sshd_config
# SyslogFacility AUTHPRIV
# LogLevel INFO
# Set PermitRootLogin no
# Set PasswordAuthentication no
rm /root/.ssh/authorized_keys
```

- Restart ssh

```
sudo systemctl restart ssh
```

- In anther terminal, verify you can login.

### Set Up UFW

```
sudo apt install ufw
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow OpenSSH
sudo ufw enable
```

## Set Up the Code

First you need to install all the pp libraries.

```
sudo su
cd /opt/
mkdir sports_display
```

Move the code into the folder.

```
cd sports_display
python3 -m venv --system-site-packages .venv
source ./.venv/bin/activate
pip install -r requirements.txt
```

### Linting

You can lint check the code with the following commands:

```
# Check for issues
ruff check .

# Auto-fix issues
ruff check --fix .

# Format code
ruff format .

# Type checking
mypy .
```
