import operator
import numpy as np
import pathlib
from pathlib import Path
from io import BufferedReader
from collections import defaultdict
from PIL import Image, PngImagePlugin
from PIL.PngImagePlugin import PngImageFile


class Sprite:
    def __init__(self, label, x1, y1, x2, y2):
        check_list = [label, x1, y1, x2, y2]
        for elm in check_list:
            if isinstance(elm, str) or elm < 0 or (x1, y1) > (x2, y2):
                raise ValueError("Invalid coordinates")
            else:
                self.__label = label
                self.__top_left = (x1, y1)
                self.__bottom_right = (x2, y2)

                self.x1 = x1
                self.y1 = y1
                self.x2 = x2
                self.y2 = y2

    @property
    def label(self):
        return self.__label

    @property
    def top_left(self):
        return (self.x1, self.y1)

    @property
    def bottom_right(self):
        return (self.x2, self.y2)

    @property
    def width(self):
        return self.x2 - self.x1 + 1

    @property
    def height(self):
        return self.y2 - self.y1 + 1


class Pixel:
    def __init__(self, label):
        self.label = label

    def __repr__(self):
        return str(self.label)


class SpriteSheet:
    def __init__(self, fd, background_color=None):
        try:
            if isinstance(fd, str):
                self.fd = Image.open(fd)
            elif isinstance(fd, Path):
                self.fd = Image.open(fd)
            elif isinstance(fd, BufferedReader):
                self.fd = Image.open(fd)
            elif isinstance(fd, PngImageFile):
                self.fd = fd
            if background_color == None:
                self.background_color = self.find_most_common_color(self.fd)
            else:
                self.background_color = background_color
        except FileNotFoundError:
            raise FileNotFoundError("FileNotFoundError")

    @staticmethod
    def find_most_common_color(image):
        """
        A function returns the pixel color that is the most used in this image.

        @param: image (Image object)
        @return:
            - an integer if the mode is grayscale;
            - a tuple (red, green, blue) of integers if the mode is RGB;
            - a tuple (red, green, blue, alpha) of integers if the mode is RGBA.
        """
        color_count = defaultdict(int)
        for pixel in image.getdata():
            color_count[pixel] += 1
        return max(color_count.items(), key=operator.itemgetter(1))[0]

    def find_sprites(self, background_color=None):
        """
        A function use to find sprites in an Image
        @param:
            - image
            - background_color (optional argument)
        @return:
            - sprites: a collection of key-value pairs (a dictionary)
                    where each key-value pair maps the key (the label of a sprite)
                    to its associated value (a Sprite object)
            - label_map: A 2D array of integers of equal dimension (width and
                height) as the original image where the sprites are packed in.
                The label_map array maps each pixel of the image passed to the
                function to the label of the sprite this pixel corresponds to,
                or 0 if this pixel doesn't belong to a sprite.
        """
        # Create empty label_map as same as size with image
        label_map = self.draw_map()
        label = 0
        check_label = False
        # List of pixel in image
        pixel_list = np.array(self.fd)
        four_direction = [[-1, -1], [-1, 0], [-1, 1], [0, -1]]
        # Define background_color if default is None
        if background_color == None:
            background_color = self.detect_background_color(pixel_list)
        for row in range(self.fd.size[1]):
            for col in range(self.fd.size[0]):
                if self.is_background_color(pixel_list[row][col], background_color):
                    label_map[row][col].label = 0
                else:
                    new_row, new_col = row, col
                    label_list = []
                    # Use 4-connected neighborhood method
                    for y, x in four_direction:
                        new_row = row + y
                        new_col = col + x
                        # If not in area of image, don't handle anything
                        if not self.is_in_area(new_row, new_col):
                            continue
                        if label_map[new_row][new_col].label != 0:
                            label_map[row][col].label = label_map[new_row][new_col].label
                            check_label = True
                            break
                        else:
                            check_label = False
                    label_map, label = self.create_new_label(
                        check_label, label_map, row, col, label)
        # Create label_equivalent after tick label
        label_equivalent = self.create_label_equivalent(
            label_map, four_direction)
        # New label_map after merge all label equivlent
        label_map = self.merge_label_map(label_map, label_equivalent)
        # Create a collection of sprite object
        sprites = self.detect_sprite(label_map)
        return sprites, label_map

    def draw_map(self):
        """
        A function return label_map with width and height same as image

        @param:
            - image (to get size)
        @return:
            - label_map contain each pixel object
        """
        label_map = []
        for i in range(self.fd.size[1]):
            tmp_list = []
            for j in range(self.fd.size[0]):
                tmp_list.append(Pixel("."))
            label_map.append(tmp_list)
        return label_map

    def detect_background_color(self, pixel_list):
        """
        A function return background_color of image:

        @param:
            - pixel_list (list of pixel in image)
            - image (to get mode)
        @return:
            - background_color of image
        """
        if self.fd.mode == "RGBA":
            background_color_list = []
            for i in range(len(pixel_list)):
                for j in range(len(pixel_list[i])):
                    if pixel_list[i][j][3] == 0:
                        background_color_list.append(pixel_list[i][j])
            return background_color_list
        return find_most_common_color(self.fd)

    def is_background_color(self, pixel, background_color):
        """
        A function return if pixel is background color or not

        @param:
            - pixel
            - background_color
        @return
            - pixel is background color or not
        """
        if isinstance(background_color, set):
            return pixel in background_color
        return np.all(pixel == background_color)

    def is_in_area(self, row, col):
        """
        A function return if position is in area or not

        @param:
            - row, col (position of pixel)
            - image (to get width and height of image)
        @return:
            - position is in area or not
        """
        return row >= 0 and row < self.fd.size[1] and col >= 0 and col < self.fd.size[0]

    def create_new_label(self, check_label, label_map, row, col, label):
        """
        A function to create new label if non-exist label neighborhood
        """
        if check_label == False:
            label += 1
            label_map[row][col].label = label
        return label_map, label

    def create_label_equivalent(self, label_map, four_direction):
        """
        A function return label_equivalent of label key

        @param:
            - label_map (with all label before merge)
            - four_direction (4-connected neighbor of pixel)
        """
        label_equivalent = {}
        for row in range(len(label_map)):
            for col in range(len(label_map[row])):
                if label_map[row][col].label != 0:
                    count_zero = 0
                    new_row, new_col = row, col
                    # Use 4-connected neighborhood method
                    for y, x in four_direction:
                        new_row = row + y
                        new_col = col + x
                        # If not in area of image, don't handle anything
                        if not self.is_in_area(new_row, new_col):
                            continue
                        if label_map[new_row][new_col].label != 0:
                            label_equivalent.setdefault(label_map[row][col].label, set()).add(
                                label_map[new_row][new_col].label)
                        elif label_map[new_row][new_col].label == 0:
                            count_zero += 1
                    # If non-exist neighborhood label
                    if count_zero == 4:
                        # Add itself to label_equivalent
                        label_equivalent.setdefault(label_map[row][col].label, set()).add(
                            label_map[row][col].label)
                        # Add another neighborhood label
                        if self.is_in_area(row, col + 1) and label_map[row][col + 1].label != 0:
                            label_equivalent.setdefault(label_map[row][col].label, set()).add(
                                label_map[row][col + 1].label)
        return self.merge_label_equivalent(label_equivalent)

    def merge_label_equivalent(self, input_dict):
        """
        A function return output dict after merge all label equivalent

        @param:
            - input_dict (a collection label key with
                        another key set value before merge)
        @return:
            - output dict after merge all label equivalent
        """
        output_dict = {}
        i = 0
        list_key = list(input_dict.keys())
        while i < len(list_key):
            value = list(input_dict[list_key[i]])
            first_len = -2
            second_len = -1
            while first_len != second_len:
                first_len = len(value)
                for elm in value:
                    value = list(set(value + list(input_dict[elm])))
                second_len = len(value)
                output_dict.update({list_key[i]: set(value)})
            i += 1
        return output_dict

    def merge_label_map(self, label_map, label_equivalent):
        """
        A function return label_map after merge all label equivalent

        @param:
            - label_map (before merge label)
            - label_equivalent (a collection key label has merged)
        @return:
            - label_map after merge label
        """
        for row in range(len(label_map)):
            for col in range(len(label_map[row])):
                if label_map[row][col].label in label_equivalent.keys():
                    label_map[row][col].label = min(
                        list(label_equivalent[label_map[row][col].label]))
        return label_map

    def detect_sprite(self, label_map):
        """
        A function return location of sprite object in image

        @param:
            - label_map (with all label was merged)
        @return:
            - a collection of sprite object
        """
        label_location_dict = {}
        for row in range(len(label_map)):
            for col in range(len(label_map[row])):
                if label_map[row][col].label != 0:
                    label_location_dict.setdefault(
                        label_map[row][col].label, []).append((row, col))
        return self.create_sprite_object(label_location_dict)

    def create_sprite_object(self, label_location_dict):
        """
        A function return a collection of sprite object

        @param:
            - label_location_dict (with key is label and
                                    value is location of each label)
        @return:
            - sprites is a collection of sprite object
        """
        sprites = {}
        for key in label_location_dict:
            x1 = min(label_location_dict[key], key=lambda x: x[1])[1]
            y1 = min(label_location_dict[key], key=lambda x: x[0])[0]
            x2 = max(label_location_dict[key], key=lambda x: x[1])[1]
            y2 = max(label_location_dict[key], key=lambda x: x[0])[0]
            sprites[key] = Sprite(key, x1, y1, x2, y2)
        return sprites

    def create_sprite_labels_image(self, background_color=(255, 255, 255)):
        """
        A function returns an image of equal dimension (width and height)
        as the original image that was passed to the function find_sprites.

        @param:
            - sprites (A collection of key-value pairs (a dictionary)
                    where each key-value pair maps the key (the label
                    of a sprite) to its associated value (a Sprite object))
            - label_map (array maps each pixel of the image passed to the function
                        to the label of the sprite this pixel corresponds to,
                        or 0 if this pixel doesn't belong to a sprite)
            - background_color (the color to use as the background
                                of the image to create)
        @return:
            - Image object of equal dimension (width and height) as the original
            image that was passed to the function find_sprites.
        """
        sprites, label_map = self.find_sprites()
        label_map, color_dict = self.draw_sprite_border(
            sprites, label_map, background_color)
        label_map = self.draw_sprite_color(
            label_map, color_dict, background_color)
        return Image.fromarray(np.array(label_map, dtype=np.uint8))

    def draw_sprite_border(self, sprites, label_map, background_color):
        """
        A function return label_map after draw border for each sprite.

        @param:
            - sprites (A collection of key-value pairs (a dictionary)
                    where each key-value pair maps the key (the label
                    of a sprite) to its associated value (a Sprite object))
            - label_map (array maps each pixel of the image passed to the function
                        to the label of the sprite this pixel corresponds to,
                        or 0 if this pixel doesn't belong to a sprite)
            - background_color (the color to use as the background
                                of the image to create)
        @return:
            - label_map after draw border for each sprite
            - color_dict has a collection of color for each label
        """
        color_dict = {}
        for key in sprites:
            color_dict[key] = self.create_random_color(background_color)
            for row in range(sprites[key].y1, sprites[key].y2 + 1):
                for col in range(sprites[key].x1, sprites[key].x2 + 1):
                    if row == sprites[key].y1 or row == sprites[key].y2:
                        label_map[row][col].label = key
                    elif col == sprites[key].x1 or col == sprites[key].x2:
                        label_map[row][col].label = key
        return label_map, color_dict

    def create_random_color(self, background_color):
        """
        A function return random color of RGB mode or RGBA mode

        @param:
            - background_color (the color to use as the background
                                of the image to create (to test length))
        @return:
            - random color of RGB mode or RGBA mode
        """
        if len(background_color) == 4:
            return (np.random.randint(0, 255), np.random.randint(0, 255),
                    np.random.randint(0, 255), np.random.randint(0, 255))
        else:
            return (np.random.randint(0, 255), np.random.randint(0, 255),
                    np.random.randint(0, 255))

    def draw_sprite_color(self, label_map, color_dict, background_color):
        """
        A function return label_map after draw color for each sprite

        @param:
            - label_map (a map after draw border for each sprite)
            - color_dict (a collection of color for each label)
            - background_color (the color to use as the background
                                of the image to create)

        @return:
            - label_map after draw color for each sprite
        """
        for row in range(len(label_map)):
            for col in range(len(label_map[row])):
                if label_map[row][col].label == 0:
                    label_map[row][col] = background_color
                else:
                    label_map[row][col] = color_dict[label_map[row][col].label]
        return label_map


def find_most_common_color(image):
    """
    A function returns the pixel color that is the most used in this image.

    @param:
        - image (Image object)
    @return:
        - an integer if the mode is grayscale;
        - a tuple (red, green, blue) of integers if the mode is RGB;
        - a tuple (red, green, blue, alpha) of integers if the mode is RGBA.
    """
    color_count = defaultdict(int)
    for pixel in image.getdata():
        color_count[pixel] += 1
    return max(color_count.items(), key=operator.itemgetter(1))[0]


def find_sprites(image, background_color=None):
    """
    A function use to find sprites in an Image
    @param:
        - image
        - background_color (optional argument)
    @return:
        - sprites: a collection of key-value pairs (a dictionary)
                where each key-value pair maps the key (the label of a sprite)
                to its associated value (a Sprite object)
        - label_map: A 2D array of integers of equal dimension (width and
            height) as the original image where the sprites are packed in.
            The label_map array maps each pixel of the image passed to the
            function to the label of the sprite this pixel corresponds to,
            or 0 if this pixel doesn't belong to a sprite.
    """
    # Create empty label_map as same as size with image
    label_map = draw_map(image)
    label = 0
    check_label = False
    # List of pixel in image
    pixel_list = np.array(image)
    four_direction = [[-1, -1], [-1, 0], [-1, 1], [0, -1]]
    # Define background_color if default is None
    if background_color == None:
        background_color = detect_background_color(pixel_list, image)
    for row in range(image.size[1]):
        for col in range(image.size[0]):
            if is_background_color(pixel_list[row][col], background_color):
                label_map[row][col].label = 0
            else:
                new_row, new_col = row, col
                label_list = []
                # Use 4-connected neighborhood method
                for y, x in four_direction:
                    new_row = row + y
                    new_col = col + x
                    # If not in area of image, don't handle anything
                    if not is_in_area(new_row, new_col, image):
                        continue
                    if label_map[new_row][new_col].label != 0:
                        label_map[row][col].label = label_map[new_row][new_col].label
                        check_label = True
                        break
                    else:
                        check_label = False
                label_map, label = create_new_label(
                    check_label, label_map, row, col, label)
    # Create label_equivalent after tick label
    label_equivalent = create_label_equivalent(label_map, four_direction)
    # New label_map after merge all label equivlent
    label_map = merge_label_map(label_map, label_equivalent)
    # Create a collection of sprite object
    sprites = detect_sprite(label_map)
    return sprites, label_map


def draw_map(image):
    """
    A function return label_map with width and height same as image

    @param:
        - image (to get size)
    @return:
        - label_map contain each pixel object
    """
    label_map = []
    for i in range(image.size[1]):
        tmp_list = []
        for j in range(image.size[0]):
            tmp_list.append(Pixel("."))
        label_map.append(tmp_list)
    return label_map


def detect_background_color(pixel_list, image):
    """
    A function return background_color of image:

    @param:
        - pixel_list (list of pixel in image)
        - image (to get mode)
    @return:
        - background_color of image
    """
    if image.mode == "RGBA":
        background_color_list = []
        for i in range(len(pixel_list)):
            for j in range(len(pixel_list[i])):
                if pixel_list[i][j][3] == 0:
                    background_color_list.append(pixel_list[i][j])
        return background_color_list
    return find_most_common_color(image)


def is_background_color(pixel, background_color):
    """
    A function return if pixel is background color or not

    @param:
        - pixel
        - background_color
    @return
        - pixel is background color or not
    """
    if isinstance(background_color, set):
        return pixel in background_color
    return np.all(pixel == background_color)


def is_in_area(row, col, image):
    """
    A function return if position is in area or not

    @param:
        - row, col (position of pixel)
        - image (to get width and height of image)
    @return:
        - position is in area or not
    """
    return row >= 0 and row < image.size[1] and col >= 0 and col < image.size[0]


def create_new_label(check_label, label_map, row, col, label):
    """
    A function to create new label if non-exist label neighborhood
    """
    if check_label == False:
        label += 1
        label_map[row][col].label = label
    return label_map, label


def create_label_equivalent(label_map, four_direction):
    """
    A function return label_equivalent of label key

    @param:
        - label_map (with all label before merge)
        - four_direction (4-connected neighbor of pixel)
    """
    label_equivalent = {}
    for row in range(len(label_map)):
        for col in range(len(label_map[row])):
            if label_map[row][col].label != 0:
                count_zero = 0
                new_row, new_col = row, col
                # Use 4-connected neighborhood method
                for y, x in four_direction:
                    new_row = row + y
                    new_col = col + x
                    # If not in area of image, don't handle anything
                    if not is_in_area(new_row, new_col, image):
                        continue
                    if label_map[new_row][new_col].label != 0:
                        label_equivalent.setdefault(label_map[row][col].label, set()).add(
                            label_map[new_row][new_col].label)
                    elif label_map[new_row][new_col].label == 0:
                        count_zero += 1
                # If non-exist neighborhood label
                if count_zero == 4:
                    # Add itself to label_equivalent
                    label_equivalent.setdefault(label_map[row][col].label, set()).add(
                        label_map[row][col].label)
                    # Add another neighborhood label
                    if is_in_area(row, col + 1, image) and label_map[row][col + 1].label != 0:
                        label_equivalent.setdefault(label_map[row][col].label, set()).add(
                            label_map[row][col + 1].label)
    return merge_label_equivalent(label_equivalent)


def merge_label_equivalent(input_dict):
    """
    A function return output dict after merge all label equivalent

    @param:
        - input_dict (a collection label key with
                    another key set value before merge)
    @return:
        - output dict after merge all label equivalent
    """
    output_dict = {}
    i = 0
    list_key = list(input_dict.keys())
    while i < len(list_key):
        value = list(input_dict[list_key[i]])
        first_len = -2
        second_len = -1
        while first_len != second_len:
            first_len = len(value)
            for elm in value:
                value = list(set(value + list(input_dict[elm])))
            second_len = len(value)
            output_dict.update({list_key[i]: set(value)})
        i += 1
    return output_dict


def merge_label_map(label_map, label_equivalent):
    """
    A function return label_map after merge all label equivalent

    @param:
        - label_map (before merge label)
        - label_equivalent (a collection key label has merged)
    @return:
        - label_map after merge label
    """
    for row in range(len(label_map)):
        for col in range(len(label_map[row])):
            if label_map[row][col].label in label_equivalent.keys():
                label_map[row][col].label = min(
                    list(label_equivalent[label_map[row][col].label]))
    return label_map


def detect_sprite(label_map):
    """
    A function return location of sprite object in image

    @param:
        - label_map (with all label was merged)
    @return:
        - a collection of sprite object
    """
    label_location_dict = {}
    for row in range(len(label_map)):
        for col in range(len(label_map[row])):
            if label_map[row][col].label != 0:
                label_location_dict.setdefault(
                    label_map[row][col].label, []).append((row, col))
    return create_sprite_object(label_location_dict)


def create_sprite_object(label_location_dict):
    """
    A function return a collection of sprite object

    @param:
        - label_location_dict (with key is label and
                                value is location of each label)
    @return:
        - sprites is a collection of sprite object
    """
    sprites = {}
    for key in label_location_dict:
        x1 = min(label_location_dict[key], key=lambda x: x[1])[1]
        y1 = min(label_location_dict[key], key=lambda x: x[0])[0]
        x2 = max(label_location_dict[key], key=lambda x: x[1])[1]
        y2 = max(label_location_dict[key], key=lambda x: x[0])[0]
        sprites[key] = Sprite(key, x1, y1, x2, y2)
    return sprites


def create_sprite_labels_image(sprites, label_map, background_color=(255, 255, 255)):
    """
    A function returns an image of equal dimension (width and height)
    as the original image that was passed to the function find_sprites.

    @param:
        - sprites (A collection of key-value pairs (a dictionary)
                where each key-value pair maps the key (the label
                of a sprite) to its associated value (a Sprite object))
        - label_map (array maps each pixel of the image passed to the function
                    to the label of the sprite this pixel corresponds to,
                    or 0 if this pixel doesn't belong to a sprite)
        - background_color (the color to use as the background
                            of the image to create)
    @return:
        - Image object of equal dimension (width and height) as the original
        image that was passed to the function find_sprites.
    """
    label_map, color_dict = draw_sprite_border(
        sprites, label_map, background_color)
    label_map = draw_sprite_color(label_map, color_dict, background_color)
    return Image.fromarray(np.array(label_map, dtype=np.uint8))


def draw_sprite_border(sprites, label_map, background_color):
    """
    A function return label_map after draw border for each sprite.

    @param:
        - sprites (A collection of key-value pairs (a dictionary)
                where each key-value pair maps the key (the label
                of a sprite) to its associated value (a Sprite object))
        - label_map (array maps each pixel of the image passed to the function
                    to the label of the sprite this pixel corresponds to,
                    or 0 if this pixel doesn't belong to a sprite)
        - background_color (the color to use as the background
                            of the image to create)
    @return:
        - label_map after draw border for each sprite
        - color_dict has a collection of color for each label
    """
    color_dict = {}
    for key in sprites:
        color_dict[key] = create_random_color(background_color)
        for row in range(sprites[key].y1, sprites[key].y2 + 1):
            for col in range(sprites[key].x1, sprites[key].x2 + 1):
                if row == sprites[key].y1 or row == sprites[key].y2:
                    label_map[row][col].label = key
                elif col == sprites[key].x1 or col == sprites[key].x2:
                    label_map[row][col].label = key
    return label_map, color_dict


def create_random_color(background_color):
    """
    A function return random color of RGB mode or RGBA mode

    @param:
        - background_color (the color to use as the background
                            of the image to create (to test length))
    @return:
        - random color of RGB mode or RGBA mode
    """
    if len(background_color) == 4:
        return (np.random.randint(0, 255), np.random.randint(0, 255),
                np.random.randint(0, 255), np.random.randint(0, 255))
    else:
        return (np.random.randint(0, 255), np.random.randint(0, 255),
                np.random.randint(0, 255))


def draw_sprite_color(label_map, color_dict, background_color):
    """
    A function return label_map after draw color for each sprite

    @param:
        - label_map (a map after draw border for each sprite)
        - color_dict (a collection of color for each label)
        - background_color (the color to use as the background
                            of the image to create)

    @return:
        - label_map after draw color for each sprite
    """
    for row in range(len(label_map)):
        for col in range(len(label_map[row])):
            if label_map[row][col].label == 0:
                label_map[row][col] = background_color
            else:
                label_map[row][col] = color_dict[label_map[row][col].label]
    return label_map


if __name__ == "__main__":
    image = SpriteSheet("../resources/metal_slug_single_sprite.png")
    new_image = image.create_sprite_labels_image()
    new_image.save("./Khang.png")
