class LandShape:
    def __init__(self, d_path:str , precision_in_km:float=None):
        self.d_path = d_path
        self.precision_in_km = precision_in_km
    
    def __str__(self):
        return str(
            {
                "d_path" : self.d_path,
                "precision_in_km" : self.precision_in_km
            }
        )