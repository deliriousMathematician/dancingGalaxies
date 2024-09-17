# Function to seperate stars by age.
# This should be relatively easily modifiable into something more general as needed.
def star_ages (sim):
    
    stars = sim.stars
    current_time = sim.properties['time'].in_units('Gyr')
    star_ages = current_time - stars['tform'].in_units('Gyr')
    y_stars = stars[star_ages < 1]
    i_stars = stars[(star_ages > 1) & (star_ages < 5)]
    o_stars = stars[star_ages > 5]
    
    return y_stars, i_stars, o_stars
