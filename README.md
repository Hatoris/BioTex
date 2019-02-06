# BioTex

## Introduction 

This repo contain all my `.tex` and `.sty` files used to genrate protocols with $\LaTeX$.

## Folder structures 

### image 

All common pictures needed to illustrate my protocols.

### material 

Files with pre-filed informations about materials used during experiment.
- Cellues.tex
- Consommables.tex

### package

Files `.sty` with usefull command in it.

- BioAbreviation.sty : abbreviations commonly used with nice formated options

### protocole

Files with pre-filed about common technic used during experiments.

- ARN_extraction.tex
- Comptage_cellules.tex
- Dilutions_courbe_calibration.tex
- Dilutions_ICC.tex
- Inflammation_cellules.tex
- Mesure_TEER.tex
- Milieu_inflammation.tex
- Solution_stock_poudre.tex
- Staining_ibidi.tex
- Test_permeabilite.tex
- Transwell_collagen.tex
- Transwell_depos_cellule.tex

### Template

Basic files to generates a protocol PDF protocol


## Command for TeXMakers

1. Run pdflatex, pythontex, bibtex and makeindex in a single commande. 
```sh

pdflatex %.tex|pythontex %.tex|bibtex %.tex|pdflatex -shell-escape %.tex|makeindex %.nlo -s nomencl.ist -o %.nls|pdflatex %.tex

```
