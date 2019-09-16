from typing import List, Tuple
from BioPlate import BioPlate

from .latex_elements import LatexElements as LE
from . import ureg
from pythontex_command import Enumerate


def create_table(plates : List[Tuple[str, List[Tuple[str, str]], str]], plate_infos = [6,4]) -> None:
    """
    Return a latex tables with captation and label.

    Arguments
    --------
    plates : List
        List that should contain an iterables with captation, values for BioPlate, and label.
    plate_infos : List
        List that should contain row and column to parse in bioplate 
    """
    row, col = plate_infos
    for title, values, label in plates:
        plate = BioPlate(row,col)
        plate.set(values, merge=True)
        print(r"\begin{table}[H]")
        print(r"\caption{" + title + "}")
        print(r"\resizebox{\textwidth}{!}{")
        print(plate.table(tablefmt="latex_raw", stralign="center"))
        print("}")
        print(r"\label{" + label + "}")
        print(r"\end{table}")

def create_stock_solution(infos : List):
    """Create a subsubsection with drug name in it. Create a numerate list will all the step to do. if weighted not present return the desired masse to weight

    infos : List
        for each elements in infos return a subsub section. List should contain following informations as Dict:
            { 
                "name" : "Verapamil",
                "weighted" :  "",
                "Mw" : "491.1 g/mol",
                "Cf" : "10 mM",
                "Vf" : "1 mL",
                "diluant" : "DMSO"
            
            }
    """
    for drug in infos:
        print(LE.subsubsection(f"Préparation de la solution de {drug.get('name', 'NotFound')}"))
        with Enumerate() as enum:
            enum.append(f"La concentration final désirée est de {drug.get('Cf', 'XX')}")
            if drug.get('weighted', False):
                Mp = ureg(drug.get('weighted'))
                Cf = ureg(drug.get("Cf")).to("mol/mL")
                Mw = ureg(drug.get("Mw")) 
                Vf = ((Mp.to("g") / Mw) / Cf)
                enum.append(f"La masse pesée est de {Mp:.2~P}")
            else:
                Cf = ureg(drug.get("Cf")).to("mol/mL")
                Mw = ureg(drug.get("Mw"))
                Vf = ureg(drug.get("Vf"))
                Md = (Cf * Mw * Vf).to("mg")
                enum.append(f"La masse qui devrait être pesée est de {Md:.2~P}")
            enum.append(f"On ajoute {Vf:.2~P} de {drug.get('diluant')}")
            enum.append("Entourer le tube d'aluminium")

def create_stock_solutions_2(infos : List):
    """
    voir ref create_stock_solution
    """
    for drug in infos:
        print(LE.subsubsection(f"Préparation de la solution de {drug.get('name', 'NotFound')}"))
        Cf = concentration_for_a_given_masse(drug.get("Vf"), drug.get("Mw"), drug.get("weighted"), concentration_massique=drug.get("concentration_massique", None))
        with Enumerate() as enum:
            enum.append(f"La masse pesée est de {ureg(drug.get('weighted', '0 mg')):~P}")
            enum.append(f"Dans une fiole jaugé déposée la masse pesée et completer jusqu'à 10 mL avec du {drug.get('diluant')}")
            enum.append("Fermer la fiole jaugé est la mettre dasns le bain marie à 37$^\\circ$C")
            enum.append("Une fois la solution limpide et qu'il n'y a plus de particules en suspension filtrer la solution à 0.2 nm")
            enum.append(f"La concentration final de la solution est {round(Cf,2):~P}".replace("ug", "$\\mu g$"))
            enum.append("Entourer le tube d'aluminium")

def create_work_solution(infos : List):
    """Return a section for diluting the stock solution
    
    Parameters
    ----------
    infos : List
        for each elements in infos return a subsub section. List should contain following informations as Dict:
            { 
                "name" : "Verapamil",
                "weighted" :  "",
                "Mw" : "491.1 g/mol",
                "Cf" : "10 mM",
                "Vf" : "1 mL",
                "diluant" : "DMSO",
                "Ct" : "10 uM",
                "nb_puits" : 24,
                "vol_puits" : "100 uL"
            
            }
    """
    for drug in infos:
        print(LE.subsubsection(f"Préparation de la solution de travail du {drug.get('name', 'NotFound')}"))
        Ci = (concentration_for_a_given_masse(drug.get("Vf"), drug.get("Mw"), drug.get("weighted"), concentration_massique = drug.get("concentration_massique", None))).to(drug.get("concentration_massique", "uM"))
        Vt = round((ureg(drug.get("vol_puits")) * drug.get("nb_puits")).to("uL") * 1.10, 1)
        Vi = round(ureg(drug.get("Ct")) * Vt / Ci, 1)
        with Enumerate() as enum:
            enum.append(f"Prendre {Vt:~P} de {drug.get('work_diluant')} et le mettre dans un falcon de 50 mL".replace("ul", "$\\mu L$"))
            enum.append(f"Enlever {Vi:~P} de {drug.get('work_diluant')} et ajouter {Vi:~P} de la solution stock de {drug.get('name', 'NotFound')} ({round(Ci.to(drug.get('concentration_massique', 'uM'))):~P})".replace("ul", "$\\mu L$"))
            enum.append(f"Vortexer et protéger de la lumiére")
            enum.append(f"Conserver la solution de {drug.get('name')} ({drug.get('Ct')}) a température piéce, mettre à incuber 30 min avant le test".replace("uM", "$\\mu M$"))

def concentration_for_a_given_masse(Vf : str, Mw : str, masse : str, concentration_massique : str = None):
    '''
   Return the final concentration in mM 
    '''
    Vf = ureg(Vf).to("liter")
    Mw = ureg(Mw)
    masse = ureg(masse).to("g")
    conc_massique = masse / Vf
    if concentration_massique:
        return conc_massique.to(concentration_massique)
    return (conc_massique / Mw).to("mM")