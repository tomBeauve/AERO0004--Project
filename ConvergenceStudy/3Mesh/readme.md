# Meshing strategy

## Initial mesh :

### Pipe
- length : 40 cells, uniform length
- heigth : 10 cells, Bias Factor 5 such that first cell height has y+ $\approx$ 2

### Domain Base
- length : 150 cells, growth ratio = 1.015
- heigth : 
    - from r = 0 to D/2 same as in pipe
    - from r = D/2 to 32D 100 cells and BF = 50 such that first cell height is approx the same as the one just under r = D/2

### Domain Extension
- length : growth ratio = 1.1, number of cells such that 1st cell length approx last cell length of the base domain
- heigth : growth ratio = 1.1, number of cells such that 1st cell heigth approx last cell heigth of the base domain


## Refinement strategy:
factor between two refinements r= 1.5

### Pipe
- length : increase number of cells by r, uniform length
- heigth : increase number of cells by r, Bias Factor *adjusted* such that first cell height keeps y+ $\approx$ 2

### Domain Base
- length : increase number of cells by r, growth ratio *adjusted* to keep **aspect ratio of the cell at (z,r) = (0, D/2) to be approx 1**
- heigth : 
    - from r = 0 to D/2 same as in pipe
    - from r = D/2 to 32D increase number of cells by r, BF *adjusted* such that first cell height is approx the same as the one just under r = D/2

### Domain Extension
- length : growth ratio = 1.1, number of cells such that 1st cell length approx last cell length of the base domain
- heigth : growth ratio = 1.1, number of cells such that 1st cell heigth approx last cell heigth of the base domain

## old strategy
For refinements, kept Bias factor = 50 in height and r = 1.015 in length