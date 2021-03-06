from resources.Land import Land
from resources.BoundingBox import BoundingBox
from maps_geometry.compression import compress_land
from crud.Land_CRUD import LandCRUD
from werkzeug.exceptions import BadRequest
import conf
from crud.db import get_cursor
class LandTag:
    @staticmethod
    def post_land(land):
        assert isinstance(land, Land)
        compressed = compress_land(land)
        if len(compressed.representations) <= 1:
            raise BadRequest(f"Path is too and is not even visible at {min(conf.PRECISION_LEVELS)}km precision : {land.representations[0].d_path}")
        with get_cursor() as curs:
            return LandCRUD.add_land(curs, compressed)
    
    @staticmethod
    def get_land(land_id):
        assert isinstance(land_id, int)
        with get_cursor() as cursor:
            return LandCRUD.get_land(cursor, land_id)

    @staticmethod
    def get_lands(bbox, precision):
        assert isinstance(bbox, BoundingBox)
        if precision not in conf.PRECISION_LEVELS:
            raise BadRequest(f"required precision is not registered on server, available precisions : {conf.PRECISION_LEVELS}")
        with get_cursor() as cursor:
            return LandCRUD.get_lands(cursor, bbox, precision)