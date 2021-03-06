import logging

class BoundingBox:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_x = x + width
        self.max_y = y + height

    def union(self, other):
        self_max_x = self.x+self.width
        self_max_y = self.y+self.height
        other_max_x = other.x+other.width
        other_max_y = other.y+other.height
        min_x = min(self.x, other.x)
        min_y = min(self.y, other.y)
        max_x = max(self_max_x, other_max_x)
        max_y = max(self_max_y, other_max_y)
        return BoundingBox(min_x, min_y, max_x-min_x, max_y-min_y)

    def area(self):
        return self.width*self.height

    def intersection(self, other):
        self_max_x = self.x+self.width
        self_max_y = self.y+self.height
        other_max_x = other.x+other.width
        other_max_y = other.y+other.height
        min_x = max(self.x, other.x)
        min_y = max(self.y, other.y)
        max_x = min(self_max_x, other_max_x)
        max_y = min(self_max_y, other_max_y)
        return BoundingBox(min_x, min_y, max_x-min_x, max_y-min_y)

    
    def get_area_percentage_in_common(self, other, log=None):        
        return 100 * self.intersection(other).area() / self.union(other).area()

    def to_dict(self):
        return {
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height
        }


    def __str__(self):
        return str((self.x, self.y, self.width, self.height))

    def equals(self, other):
        return isinstance(other, BoundingBox) and (other.x, other.y, other.width, other.height)==(self.x, self.y, self.width, self.height)
    
    def center(self):
        return (self.x+self.width / 2, self.y+self.height/2)

    def resize(self, factor):
        return BoundingBox(
            x= self.x - (factor - 1) * self.width / 2,
            y= self.y - (factor - 1) * self.height / 2,
            width= self.width * factor,
            height= self.height * factor
        )

    def enlarge_to_aspect_ratio(self, aspect_ratio) :
        aspect = self.width / self.height
        if aspect < aspect_ratio :
            return BoundingBox(
                y = self.y,
                height = self.height,
                width= aspect_ratio * self.height,
                x= self.x - (aspect_ratio * self.height - self.width) / 2
            )
        elif aspect > aspect_ratio :
            return BoundingBox(
                width=self.width,
                x=self.x,
                height= self.width / aspect_ratio,
                y= self.y - ( self.width/aspect_ratio - self.height) / 2
            )
        else :
            return self
