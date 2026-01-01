# 1 Iterative convergence : Residuals
Idea : with all other physical parameters not obligated to be good, we first check that the algebraic equations are correctly solve. BEFORE looking at the physics
## What to vary : 
- residuals tolerance
## Fixed parameters:
- mesh = coarse but of good quality ( must not be shit quality)
- domain : just the zone of interest
- BC : standard
## Action
- axial velocity at CL (looked at z/D = 45)
- mass flow imbalance
- tke max in the domain
- axial velocity in the shear layer ( looked at z/D = 20, r/D = 0.5)

## Result : the tolerance to keep is 10**-6 on residuals.
### Keep these tolerance for the following analyses


# 2 Domain Independence
Idea : Domain / entrainment errors are more long range and physically problematic & this domain dfines the control volume
## What to vary : 
- domain height and length. Start with only zone of interest, then compute 1.5 , 2, ... times in L and H
## Fixed parameters:
- residuals fixed in phase 1
- mesh = coarse but of good quality ( must not be shit quality)
- BC : standard
## Action
- radial velocity at the lateral boundary
- dP/dx at the centerline
- U at centerline at x/D = 75
- velocity field change < 0.5 % near outlet ( what quantity to look at specifically )

## Result : the size to keep is 2.25 times the domain length
### Keep this domain for the following analyses

# 3 Mesh convergence
## What to vary : 
- mesh : use first 3 meshes : coarse, mid and fine; ratio between them is constant r~ 1.5 - 2
## Fixed parameters:
- residuals fixed in phase 1
- domain fixed in phase 2
- BC : standard
## Action
- if wall function : y+ = 30, if not, y+ = 1
- GCI < 2 % => fine or medium mesh are good.
- computed on potential core length : distance at which U_CL =  0.99 U_inlet
- and also computed on centerline velocity at x/D = 30 or 40  ( stay consistent with above qtties)

### Keep the fine mesh for xfinebis in the sqare1cell folder for further analyses. And if xfine is very costly, fine is ok for BC study.

# 4 BC sensitivity
## What to vary : 
- Inlet turbulence (1 - 5%) and viscosity ratio
- Lateral and outlet BC maybe
## Fixed parameters:
- residuals fixed in phase 1
- domain fixed in phase 2
- medium or fine mesh fixed in phase 3
## Action
- Compare the Potential Core Length. This is highly sensitive to inlet BCs.
- match dns paper conditions if possible ( it is the case here) : k = 3/2 (U_avg * I)^2 ; epsilon or omega depend on turbulent length scale l ~0.07D for a pipe exit;  lateral BC aim at I~1% for ambiant turbulence


# Final results 
## Round jet anomaly : the standard k-e overpredict the spread by about 25%