from datetime import datetime
from .BoundingBox import BoundingBox
class Scene:
    def __init__(self, validity_start, validity_end, bbox, states=[]):
        assert isinstance(validity_start, datetime )
        assert isinstance(validity_end, datetime)
        assert isinstance(bbox, BoundingBox)
        assert isinstance(states, list)
        self.validity_start = validity_start
        self.validity_end = validity_end
        self.bbox = bbox
        self.states = states