# dancingGalaxies mBranch
Doing some bug fixes and working on render types. 

To simplify the process, im working on a simplified V1.2.3, obviously however, 
during merging I'll stitch it up with whichever latest version it works on.

-M

### Adjust starting zPos
Done:
- Added z_start variable which moves galactic position before starting simulation
- Adjusted dynamic frames calculation to account for non-zero z_start
- Calculate vmin and vmax when at z=0 otherwise we will get less accurate colourmap range
- Deal with negative z_shift, z_start, and z_max values

