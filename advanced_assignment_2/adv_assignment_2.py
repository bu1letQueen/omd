class Color:
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    def __str__(self):
        END = '\033[0m'
        START = '\033[1;38;2'
        MOD = 'm'

        return(f'{START};{self.red};{self.green};{self.blue}{MOD}●{END}')

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, Color):
            return NotImplemented
        else:
            if (self.red == other.red and
                self.green == other.green and
                self.blue == other.blue):
                return True
            return False

    def __add__(self, other):
        if not isinstance(other, Color):
            return NotImplemented
        else:
            red = min(self.red + other.red, 255)
            green = min(self.green + other.green, 255)
            blue = min(self.blue + other.blue, 255)
            return Color(red, green, blue)

    def __hash__(self):
        color_tuple = (self.red, self.green, self.blue)
        return hash(color_tuple)

    def __mul__(self, other):
        contrast = max(0, min(other, 1))
        contrast_level = - 256 * (contrast - 1)
        fraction = (259 * (contrast_level + 255)) / (255 * (259 - contrast_level))
        lightened_red = int(max(0, min(fraction * (self.red - 128) + 128, 255)))
        lightened_green = int(max(0, min(fraction * (self.green - 128) + 128, 255)))
        lightened_blue = int(max(0, min(fraction * (self.blue - 128) + 128, 255)))
        return Color(lightened_red, lightened_green, lightened_blue)

    def __rmul__(self, other):
        return self.__mul__(other)

