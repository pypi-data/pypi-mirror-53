from PIL import Image
from numpy import amax, where, array, zeros, uint8
from random import randint


class Sprite():
    def __init__(self, label, x1, y1, x2, y2):
        """ All arguments (except self) MUST be strictly positive integers
        """

        # Check validation
        if not self.is_valid_arguments(label, x1, y1, x2, y2):
            raise ValueError("Invalid coordinates")

        # These properties are read-only
        self._label = label
        self._top_left = (x1, y1)
        self._bottom_right = (x2, y2)

        # These are not read-only
        self.width = x2 - x1 + 1
        self.height = y2 - y1 + 1

    @property
    def label(self):
        return self._label

    @property
    def top_left(self):
        return self._top_left

    @property
    def bottom_right(self):
        return self._bottom_right

    def is_valid_arguments(self, label, x1, y1, x2, y2):
        """ Check validation of passed arguments

        All arguments MUST be non-negative Interger and
        x2 and y2 MUST be equal or greater respectively than x1 and y1

        Return True by default and False when requirement is not met
        """

        for element in [label, x1, y1, x2, y2]:
            try:
                if element < 0 or x2 < x1 or y2 < y1:
                    return False
            except TypeError:
            	return False
        return True


class Pixel():
    def __init__(self, row, column, is_background_pixel):
        # Axe x
        self.column = column
        # Axe y
        self.row = row
        # Boolean value, True if it is a background pixel
        self.is_background_pixel = is_background_pixel
        # Positive natural number
        self.label = 0

    def __repr__(self):
        return str(self.label)


class SpriteSheet():
    def __init__(self, fd, background_color=None):
        self.image_object = self.create_image_object(fd)
        # Raise error if background_color doesn't match image mode
        if background_color is not None and not self.is_valid_arguments(background_color):
            raise ValueError("Not valid arguments")
        elif background_color is not None:
            self._background_color = background_color
        else:
            self._background_color = SpriteSheet.find_most_common_color(self.image_object)

    @property
    def background_color(self):
        return self._background_color

    def is_valid_arguments(self, background_color):
        """
        Return True by default
        Return False when background_color mode is not matched with image mode
        """
        modes = { 4: "RGBA",
        3: "RGB"
        }
        if self.image_object.mode != "L" and type(background_color) != tuple:
            return False
        elif self.image_object.mode != modes[len(background_color)]:
            return False
        return True

    def create_image_object(self, fd):
        try:
            return Image.open(fd)
        except (AttributeError, UnicodeDecodeError):
            try:
                return Image.open(fd.name)
            except Exception:
                return fd

    @staticmethod
    def find_most_common_color(image):
        """
        Find most used color in an Image object

        @arg: image: MUST be an Image object

        Return most used color in the image
        Format of the return value is same as image's mode
        """

        try:
            # List of color used and its occurence
            colors = image.getcolors(image.size[0]*image.size[1])
            # List of color occurrence
            occurrences = [color[0] for color in colors]
            # Index of the most most common color
            most_common_color_index = where(occurrences == amax(occurrences))[0][0]
            # Return most common color
            most_common_color = colors[most_common_color_index][1]
            return most_common_color
        except Exception:
            print("Your Image object is invalid! Please try another!")

    def find_sprites(self):
        """ Detect sprites inside the image
        Return a 2D label map and a dict that stores:
            key: sprite's label
            value: its Sprite's object

        @image: MUST be an Image object
        """

        def collect_sprites(label_map, numpy_array):
            """
            Return a dict:
                key: sprite'label
                value: corresponding Sprite object
            """
            sprites = {}

            for row_index, row in enumerate(numpy_array):
                for column_index, column in enumerate(row):
                    current_pixel = label_map[row_index][column_index]
                    label = current_pixel.label
                    if label != 0:
                        if label not in sprites:
                            sprites[label]={'columns':{current_pixel.column}, 'rows':{current_pixel.row}}
                        else:
                            sprites[label]['columns'].add(current_pixel.column)
                            sprites[label]['rows'].add(current_pixel.row)

            for sprite in sprites:
                sprites[sprite] = Sprite(sprite, min(sprites[sprite]['columns']),
                                         min(sprites[sprite]['rows']),
                                         max(sprites[sprite]['columns']),
                                         max(sprites[sprite]['rows']))

            return sprites

        def unify_sprites(pixels_to_sprites, unified_matrix, numpy_array):
            """ Unify all pixels that are in a same sprite

            Return a 2D-array map of sprites
            """
            for row_index, row in enumerate(numpy_array):
                for column_index, column in enumerate(row):
                    current_pixel = pixels_matrix[row_index][column_index]
                    current_label = current_pixel.label
                    # Ignore background pixels
                    if current_label == 0 or current_label not in pixels_to_sprites:
                        continue
                    current_pixel.label = pixels_to_sprites[current_label]
            return unified_matrix

        def analyze_connected_sprites(connected_sprites):
            """ Find all pixels that are connected (belong to a same sprite)

            Return a dict:
                key: pixel'label
                value: sprite's label that key belong to
            """
            pixels_to_sprites = {}
            for key in list(connected_sprites.keys()):
                # Ignore those sprites that is unconnected to another
                if key not in connected_sprites or len(connected_sprites[key]) == 1:
                    continue
                in_progress = True
                old_length = len(connected_sprites[key])
                while in_progress:
                    for value in connected_sprites[key]:
                        # Ignore invalid key
                        if value not in connected_sprites:
                            continue
                        connected_sprites[key] = connected_sprites[key] | connected_sprites[value]
                        if value in connected_sprites and value != key:
                            del connected_sprites[value]
                    # Stop 'while' if there is no newly connected sprite found
                    if old_length == len(connected_sprites[key]):
                        in_progress = False
                    else:
                        old_length = len(connected_sprites[key])

            for key in connected_sprites:
                for value in connected_sprites[key]:
                    pixels_to_sprites[value] = key
            return pixels_to_sprites

        def is_new_sprite(current_row, current_column, pixels_matrix):
            """ Return False if there is a non-background pixel adjacent to current pixel
            Ignores background pixels.
            """
            neighbor_coordinates = [(-1, -1), (-1, 0), (-1, 1), (0, -1)]
            current_pixel = pixels_matrix[current_row][current_column]
            is_new_sprite = True

            # Ignore background pixels
            if current_pixel.is_background_pixel:
                return False

            # Check 4 neighbor of current pixels
            for coordinate in neighbor_coordinates:
                neighbor_row = current_row + coordinate[0]
                neighbor_column = current_column + coordinate[1]
                # Make sure pixel's coordinate is inside the image
                if 0 <= neighbor_row < image_height and 0 <= neighbor_column < image_width:
                    neighbor_pixel = pixels_matrix[neighbor_row][neighbor_column]
                    # Ignore background pixels
                    if neighbor_pixel.label == 0:
                        continue
                    if current_pixel.label != 0 and current_pixel.label != neighbor_pixel.label:
                        connected_sprites.setdefault(current_pixel.label, set()).add(neighbor_pixel.label)
                    else:
                        pixels_matrix[current_row][current_column].label = neighbor_pixel.label
                        is_new_sprite = False

            return is_new_sprite

        def is_ignored_pixel(current_pixel, numpy_array):
            """ Check if that pixel is considered background pixel

            Return False by default
            """
            if (self._background_color == (0,0,0,0) and current_pixel[-1] == 0) or (current_pixel == array(self._background_color)).all() or (image.mode == "L" and current_pixel == background_color):
                return True
            return False

        def analyze_numpy_array():
            """ Convert image to numpy array then analyze each pixel

            Return Maps of pixels under format matrix and numpy array (multi-dimensional)
            """

            numpy_array = array(image)
            pixels_matrix = zeros(numpy_array.shape, dtype=int).tolist()

            vertorize_function = vectorize(create_pixel_object)
            vertorize_function(numpy_array)

            for row_index, row in enumerate(numpy_array):
                for column_index, column in enumerate(row):
                    current_pixel = numpy_array[row_index, column_index]
                    pixels_matrix[row_index][column_index] = Pixel(row_index, column_index, is_ignored_pixel(current_pixel, numpy_array))

            for row_index, row in enumerate(numpy_array):
                for column_index, column in enumerate(row):
                    if is_new_sprite(row_index, column_index,
                                     pixels_matrix):
                        new_label = sprites_label[-1] + 1
                        pixels_matrix[row_index][column_index].label = new_label
                        sprites_label.append(new_label)
                        connected_sprites.setdefault(new_label, set()).add(new_label)

            return pixels_matrix, numpy_array

        def is_valid_background_color():
            """ Check if arg @background_color is valid

            Return True by default
            """
            # Not int or tuple
            if type(self._background_color) not in (int, tuple):
                return False
            # Invalid grayscale format
            if type(self._background_color) == int:
                if not 255 >= self._background_color >= 0 or image.mode != "L":
                    return False
            # Invalid RGB/ RGBA format
            if type(self._background_color) == tuple:
                if len(self._background_color) not in (3,4) or image.mode == "L":
                    return False
                for element in self._background_color:
                    if type(element) != int or not 255 >= element >= 0:
                        return False
            return True

        image = self.image_object
        if self._background_color:
            pass
        elif image.mode == "RGBA":
            self._background_color = (0,0,0,0)
        else:
            self._background_color = SpriteSheet.find_most_common_color(image)

        # Check validation of arg background_color
        if not is_valid_background_color() or not image:
            print("Invalid arguments! Please try again!")
            return

        image_width, image_height = image.size
        # Store all connected sprites that can be unified latter
        connected_sprites = {}
        # List of pixels label exist inside the map
        sprites_label = [0]
        # Maps of pixels under format matrix and numpy array
        pixels_matrix, numpy_array = analyze_numpy_array()
        # Dict of pixels'label corresponding to sprite's label
        pixels_to_sprites = analyze_connected_sprites(connected_sprites)
        # Map of sprites under format 2D-matrix
        label_map = unify_sprites(pixels_to_sprites, pixels_matrix, numpy_array)
        # A dictionary with key:the label of a sprite and value:it's Sprite object
        sprites = collect_sprites(label_map, numpy_array)
        return (sprites, label_map)


    def create_sprite_labels_image(self, background_color=(255, 255, 255)):
        """ Create a mask image of initial image,
        adding a bounding box around each sprite,
        each sprite also have an unique random uniform color.

        Return an Image object.
        """

        def colorize(sprite_colors):
            """ Replace each pixel'object in the map by its color
            """
            for row_index, row in enumerate(label_map):
                for column_index, column in enumerate(row):
                    current_pixel_label = label_map[row_index][column_index].label
                    if current_pixel_label not in sprite_colors:
                        # Image mode != "L"
                        if type(background_color) != int:
                            label_map[row_index][column_index] = list(background_color)
                        else:
                            label_map[row_index][column_index] = background_color
                    else:
                        # Image mode != "L"
                        if len(sprite_colors[current_pixel_label]) != 1:
                            label_map[row_index][column_index] = sprite_colors[current_pixel_label]
                        else:
                            label_map[row_index][column_index] = sprite_colors[current_pixel_label][0]

        def add_border(row_range, column_range, label):
            """ Represent bounding box (border) using the label of its sprite
            """
            for row in row_range:
                for column in column_range:
                    label_map[row][column].label = label

        def add_bounding_box():
            """ Return a dictionary with:
                    key: sprite's label
                    value: array of sprite's bounding box's coordinates
            """
            for label in sprites:
                sprite = sprites[label]
                # Gets coordinates of sprite's corners points
                top_left_column, top_left_row = sprite.top_left
                bottom_right_column, bottom_right_row  = sprite.bottom_right

                # Find coordinates of all points belong to bounding box (borders)
                add_border((top_left_row, bottom_right_row), range(top_left_column, bottom_right_column + 1), label)
                add_border(range(top_left_row, bottom_right_row + 1), (top_left_column, bottom_right_column), label)

        def select_color_for_sprite():
            """ Return @background_color mode and
            its sprites's random uniform color.
            """
            modes = {1:"L", 3:"RGB", 4:"RGBA"}
            if type(background_color) is tuple:
                background_color_length = len(background_color)
            else:
                background_color_length = 1
            # Mode of the image that will be returned
            mode = modes[background_color_length]
            # Dict with key:sprite's label and value: it's color
            sprite_colors = {}

            for sprite in sprites:
                # Mix color for each sprite depend on @background_color mode
                if mode == "RGB":
                    color = [randint(0, 256), randint(0, 256), randint(0, 256)]
                elif mode == "RGBA":
                    color = [randint(0, 256), randint(0, 256),
                             randint(0, 256), 255]
                else:
                    color = [randint(0, 256)]

                sprite_colors[sprite] = color
            return mode, sprite_colors

        sprites, label_map = self.find_sprites()
        # Image mode and dict of color corresponding to its sprite
        mode, sprite_colors = select_color_for_sprite()
        # Represent bounding boxes using the label of its sprite
        bounding_boxes_coordinate = add_bounding_box()
        # Replace each pixel'object in the map by its color
        colorize(sprite_colors)
        # Turn the map of pixels's color to Image object
        sprite_label_image = Image.fromarray(array(label_map, dtype=uint8))

        return sprite_label_image
