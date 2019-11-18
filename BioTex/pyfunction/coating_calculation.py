from BioTex import ureg, Q_
from datetime import datetime

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


def total_incubation_time(start : str, end : str) -> str:
    """Compute the time difference between start and end.
    
    Parameters
    ----------
    start : str
        starting time of incubation # 2019-11-18 12h30
    end : str
        ending time of incubation # 2019-11-18 16h00
    
    Returns
    -------
    str
        Delta time in hour:minute # 3h30
    """
    split_date_time = lambda x : x.split(" ")
    split_date = lambda x : x.split("-")
    split_time = lambda x : x.split("h")

    try:
        sdate, stime = split_date_time(start)
        edate, etime = split_date_time(end)
        syear, smonth, sday = split_date(sdate)
        eyear, emonth, eday = split_date(edate)
        shour, smin = split_time(stime)
        ehour, emin = split_time(etime)
        st = datetime(*map(int, [syear, smonth, sday, shour, smin]))
        et = datetime(*map(int, [eyear, emonth, eday, ehour, emin]))
        delta = (et - st).total_seconds() / 3600
        hour, minutes = int(delta), delta - int(delta)
        return f"{hour}h{int(minutes * 60)}"
    except ValueError:
        return "**h**"


