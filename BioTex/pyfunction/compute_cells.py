from typing import Union, List

class cellDilutionParameters:

    def __init__(self, volume_initial : int = 1, cell_per_surface : int = 4e5, volume_per_well : int = 200, 
        well_surface : float = 0.33, 
        output : List = ["condition_name", "concentration_initial", "volume_initial", "concentration_final", "volume_final"]):
        """Based paramter
        
        Parameters
        ----------
        volume_initial : int, optional
            volume in of cells (mL) , by default 1
        cell_per_surface : int, optional
            numbr of cells per cm2 surface (cells/cm2), by default 4e5
        volume_per_well : int, optional
            volume of final cell supsension to add in each well (uL), by default 200
        well_surface : float, optional
            surface of one well (cm2), by default 0.33
        output : list, optional
            structure of the outuput list, by default ["condition_name", "concentration_initial", "volume_initial", "concentration_final", "volume_final"]
        """
        self.volume_initial = volume_initial
        self.cell_per_surface = cell_per_surface
        self.volume_per_well = volume_per_well
        self.well_surface = well_surface
        self.output = output

    @property
    def cell_per_well(self) -> float:
        """Number pof cells to put in each wells to reach the desired concentration in cell per surface
        
        Returns
        -------
        float
            number of cells in one well
        """
        return self.cell_per_surface * self.well_surface


    @property
    def concentration_final(self) -> float:
        """Cell suspension concentration final to add the [cell_per_well] for a given [volume_per_well]
        
        Returns
        -------
        float
            Cell suspension concetration in cells / mL 
        """
        return self.cell_per_well / (self.volume_per_well / 1000)




class cellDilution:

    def __init__(self, 
        condition_name : str,
        concentration_initial : int, 
        nb_puits : int, 
        parameters : cellDilutionParameters):
        """Compute informations
        
        Parameters
        ----------
        concentration_initial : int
            concentration found after trypsinisation (cells/mL)
        nb_puits : int
            number of wells to put cells in it
        parameters : cellDilutionParameters
            parameters object with informations about this experiment
        """
        self.condition_name = condition_name
        self.concentration_initial = concentration_initial
        self.nb_puits = nb_puits
        self.parameters = parameters

    @property
    def total_number_of_cell(self) ->float:
        """Total number of cells used in this expermient 
        
        Returns
        -------
        float
            Total number of cells 
        """
        return self.parameters.cell_per_well * self.nb_puits

    @property
    def is_enough(self) -> bool:
        """Based on conditions check if we have enought cells to put in each wells
        
        Returns
        -------
        bool
            True if we have enought
        """
        return self.concentration_initial * self.parameters.volume_initial > self.total_number_of_cell

    @property
    def volume_final(self) -> float:
        """Compute the volume final to reach the desired concentration based on the [concentration_intial], [parmameters.volume_initial] and [parameters.concentration_final]
        
        Returns
        -------
        float
            Volume final in mL
        """
        return round(self.concentration_initial * self.parameters.volume_initial / self.parameters.concentration_final, 2)

    @staticmethod
    def to_latex(value : Union[int, float]) -> str:
        """Transform an interger to a validate scientific notation for LaTeX
        
        Parameters
        ----------
        value : Union[int, float]
            float or int to convert in LaTeX scientific notation
        
        Returns
        -------
        str
            LaTeX scientific notation
        """
        fstr = f"{value:.2E}"
        val, power = fstr[:4], fstr[-1]
        return fr"${val}\,\times\,10^{int(power)}$" 

    def concentration_to_latex(self, element : str) -> str:
        """convert concentration to latex format
        
        Parameters
        ----------
        element : str
            concentration type : intial or final 
        
        Returns
        -------
        str
            latex concentration
        """
        if "initial" in element:
            return cellDilution.to_latex(self.concentration_initial)
        return cellDilution.to_latex(self.parameters.concentration_final)

    @property
    def results(self) -> List:
        """Returns the desired values in list based on [parameters.output]
        
        Returns
        -------
        List
            Computed values
        """
        results = []
        for element in self.parameters.output:
            if "concentration" in element:
                results.append(self.concentration_to_latex(element))
                continue
            if element in self.__dict__.keys() or element in dir(self):
                results.append(getattr(self, element))
            else:
                results.append(getattr(self.parameters, element))
        return results

