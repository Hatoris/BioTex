from BioTex import ureg, Q_

class Coating:

    def __init__(self, 
        number_of_wells = None,
        volume_per_well =  None,
        quantity_per_surface = None,
        surface_well = None,
        Ci = None,
        Cf = None,
        Vf = None,
        molecule_name = None
    
    ):
        pass

@ureg.wraps("ug", ("ug/cm**2", "cm**2"))
def compute_quantity(quantity_per_surface, surface):
    return round(quantity_per_surface * surface, 2)