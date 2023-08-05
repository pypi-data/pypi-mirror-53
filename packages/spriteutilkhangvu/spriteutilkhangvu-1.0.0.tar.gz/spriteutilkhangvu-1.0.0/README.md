## Intro:
&nbsp; The project is generally used for detecting sprites inside an sprite sheets, providing bounding box of each sprite. It can also detect most used color. It can also draw and colorize a mask from the initial image.

## Usage:
#### &ensp; Create a SpriteSheet object using:
##### &ensp;&nbsp; SpriteSheet(fd, background_color=None):

             @fd: the name and path (a string) that references an image file in the local file system;
             OR a pathlib.Path object that references an image file in the local file system ; a file object that MUST implement read(), seek(), and tell() methods, and be opened in binary mode;
             OR a Image object.

             @background_color: an integer if the mode is grayscale;
             OR a tuple (red, green, blue) of integers if the mode is RGB;
             OR a tuple (red, green, blue, alpha) of integers if the mode is RGBA. The alpha element is optional. If not defined, while the image mode is RGBA, the constructor considers the alpha element to be 255.

#### &ensp; Class SpriteSheet provides following methods:

##### &ensp;&nbsp; SpriteSheet.find_most_common_color(image):

	Find most used color in an Image object
	arg: image: MUST be an Image object
	Return most used color in the image with the same format image's mode

##### &ensp;&nbsp; SpriteSheet_object.create_sprite_labels_image():

	Create a mask image of initial image, and add a bounding box around each sprite,
	each sprite also have an unique random uniform color.
	Return an Image object.

##### &ensp;&nbsp; SpriteSheet_object.find_sprites():

	Detect sprites inside the image
	Return a 2D label map and a dict that stores:
	key: sprite's label
	value: its Sprite's object
	arg: image: MUST be an Image object

## Installation:
The project require Python 3.7+ to run

#### &ensp; FOR USER:
##### &emsp; In Terminal, use command:

		 pip3 install spriteutil

#### &ensp; FOR DEVELOPMENT:
##### &emsp; Step 1: Clone or Downloads the project, using this command:

         git clone http://gitlab-students.int.intek.edu.vn/sprite-sheet/vdinh.git
##### &emsp; Step 2: Install required libs and tools, using this command in Terminal:

		 pip3 install -r requirements.txt
##### &emsp; Step 3: Edit the source code as you wish.

## Contact:
&emsp;&emsp;&emsp; During the usage of the project, if you have any question, please contact me personally at INTEK HCM City or via my Github page: https://github.com/khagkhangg

## Contributors:
&emsp;&emsp;&emsp; Khang VU from INTEK Institute, HCM City
