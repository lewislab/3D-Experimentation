from __future__ import division #ensures that all calculations are done using float division, as opposed to integer division. ex. important for dispersant calculations

dispersant_weight_fraction = 0.9 #weight fraction of dispersent stock solution
thickener_weight_fraction = 0.175 #0.175 coapur 975W
pigment_specific_area = 1 # 0.8? units of m^2/g
desired_solvent_Vfrac = 0.55  #volume fraction solvent of uncured ink 0.484 for 1010, 0.440 for 1120
desired_polymer_volume_fraction_dry = 0.42  #with respect to silver pigment only
polymer_solution_weight_fraction = .457  #if polymer solution is labeled as 'not_premade' then you do not have to change this value

solvent_density = 1 #g/mL 0.91 for EP, 0.90 for EGBE, 0.938 for diacetone alcohol
pigment_density = 10.49 # 10.1? g/cc
polymer_density = 1.2 # estimate density for TPU (g/cc)
dispersant_stock_density = 1.08 #g/cc 


target_pigment_mass = 8#grams
target_dispersant_mass_per_area = 5 #mg/m^2
thickener_weight_percent = 0.005 #weight percent of thickener compared to solvents and polymer (silver weight excluded)

def make_paste(polymer_solution_weight_fraction, polymer_solution = 'not_premade'):
    volume_pigment = target_pigment_mass*(1/pigment_density) # answer in CC
    volume_polymer = volume_pigment*(desired_polymer_volume_fraction_dry/(1-desired_polymer_volume_fraction_dry))
    #print volume_polymer 
    weight_polymer = volume_polymer*polymer_density
    #print weight_polymer
    total_pigment_area = (target_pigment_mass*pigment_specific_area) #answer in m^2
    weight_of_pure_surfactant = (target_dispersant_mass_per_area*total_pigment_area)/1000  #answer in grams
    weight_of_dispersant_stock = weight_of_pure_surfactant/dispersant_weight_fraction
    volume_of_dispersant_stock = (weight_of_dispersant_stock*(1/dispersant_stock_density))
    volume_of_dispersant_stock_uL = (weight_of_dispersant_stock*(1/dispersant_stock_density))*1000 #in microliters yo
    
    volume_dispersant_pure = volume_of_dispersant_stock*(dispersant_weight_fraction) #volume of the dispersant alone with no additional carrier solvents
    volume_of_dispersant_solvent = volume_of_dispersant_stock-volume_dispersant_pure #how much solvent volume is included in the total dispersant volume
    #print volume_of_dispersant_solvent
    volume_of_solvent_to_add = ((desired_solvent_Vfrac/(1-desired_solvent_Vfrac))*(volume_pigment+volume_dispersant_pure+volume_polymer))-volume_of_dispersant_solvent
    solvent_weight = volume_of_solvent_to_add*(solvent_density)
    
    #print solvent_weight
    print "weight of pigment to add: {} grams".format(target_pigment_mass)  
    
    if polymer_solution=='not_premade':
        polymer_solution_weight_fraction = (weight_polymer/(solvent_weight+weight_polymer))
        weight_polymer_solution = (weight_polymer/polymer_solution_weight_fraction)
        print "The polymer solution should be have a weight fraction of {} for adding no additional solvent".format(polymer_solution_weight_fraction)
        print "You need to add {} grams of the polymer solution".format(weight_polymer_solution)
        
    else:
        weight_polymer_solution = (weight_polymer/polymer_solution_weight_fraction)
        volume_extra_solvent = volume_of_solvent_to_add-(((weight_polymer/(polymer_solution_weight_fraction))-weight_polymer)/solvent_density)
        weight_extra_solvent = volume_extra_solvent*solvent_density
        print "Add {} grams of polymer solution with weight fraction of {}".format(weight_polymer_solution, polymer_solution_weight_fraction)
        print "then you will need to add an additional {} grams or {} mL of solvent ".format(weight_extra_solvent, volume_extra_solvent)
        
    vol_frac_pigment = (volume_pigment)/(volume_of_solvent_to_add+volume_polymer+volume_of_dispersant_stock+volume_pigment)
    vol_frac_solvent = (volume_of_solvent_to_add)/(volume_of_solvent_to_add+volume_polymer+volume_of_dispersant_stock+volume_pigment)
    vol_frac_polymer = (volume_polymer)/(volume_of_solvent_to_add+volume_polymer+volume_of_dispersant_stock+volume_pigment)
        
    mass_thickener_to_add =( ((weight_polymer_solution+weight_of_dispersant_stock+weight_extra_solvent)*thickener_weight_percent))/thickener_weight_fraction
    print "mass (g) and volume (uL) of dispersant solution to add repectively: {}, {}".format(weight_of_dispersant_stock, volume_of_dispersant_stock_uL)
    print "mass thickener to add (g): {}".format(mass_thickener_to_add)
    print "volume fractions (uncured)- pigment ({}), solvent ({}), polymer ({})".format(vol_frac_pigment, vol_frac_solvent, vol_frac_polymer)
    
make_paste(polymer_solution_weight_fraction, polymer_solution = 0.4)


