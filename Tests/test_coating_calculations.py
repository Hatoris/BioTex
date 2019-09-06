import pytest

from BioTex import ureg, Q_
from BioTex.pyfunction import coating_calculation as cc

@pytest.mark.parametrize("quant, surface, excpected", [
    ("5 ug/cm**2", "1 cm**2" "5 ug"),
]) 
def test_compute_quantity(quant, surface, excpected):
    assert cc.compute_quantity(quant, surface) == ureg(excpected)


if __name__ == "__main__":
    pytest.run()