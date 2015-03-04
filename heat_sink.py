from mecode import G
#from mecode.profilometer_parse import load_and_curate
import numpy as np

silver_length = 5
silver_width = 0.25
total_x_width = 15

extruder_offset = (61.95,0.55)
orgin = (60, 60)
silver_orgin = (orgin[0]-extruder_offset[0], orgin[1]-extruder_offset[1])
FDM_feed = 40*60
silver_feed = 4*60
retraction_feed = 20*60
translation_speed = 90*60
total_count =0;
width_change = 1
top_left = (30,5)
bottom_length = 10
top_length = 8
bottom_width = 0.35*6
top_width = 0.7
fin_height = 0.15*33
extrusion_width = 0.35
silver_width = 0.25
layer_height = 0.15


# Robomama Outfile
#outfile = r"C:\Users\Lewis Group\Documents\GitHub\Muscular-Thin-Films\MTF_out-new.pgm"

# Travis' Computer Outfile
outfile = r"C:\Users\lewislab\Documents\GitHub\3D-Experimentation\gcode.gcode"
#outfile = r"C:\Users\Administrator\Documents\GitHub\LewisResearchGroup\FILE_NAME.gcode"
#outfile = r"C:\Users\lewislab\Desktop\3D_experiments\COREXYverticalPlasticE1.12F20.gcode"
#outfile = r"C:\Users\lewislab\Desktop\3D_experiments\Prusa\verticalDual.gcode"
#outfile = r"C:\Users\lewislab\Desktop\3D_experiments\Prusa\Calibration.gcode"



cal_data = None#load_and_curate(calfile, reset_start=(2, -2))

g = G(
    outfile=outfile,
    #header= r"Z:\User Files\Chong\mecode\Vertical Trace\header.gcode",
    #footer= r"Z:\User Files\Chong\mecode\Vertical Trace\footer.gcode",
    #cal_data=cal_data,
    print_lines=True,
    aerotech_include = False, 
    extrude = False,
    layer_height = 0.22, 
    extrusion_width = 0.4,
    filament_diameter = 1.75,
    extrusion_multiplier = 1.33#1.33,
    )





        
def set_feed(feed_rate):
    g.write('M203 X{} Y{}'.format((feed_rate), (feed_rate)))
    
def nozzle_change(nozzle):
    g.move(z=5) # rectraction for change of nozzle
    g.write('T' + str(nozzle))
    if nozzle == '0':
        g.move(*extruder_offset)
    if nozzle == '1':  
        g.move(-extruder_offset[0], -extruder_offset[1]) 
        g.write("END FDM G CODE")
        g.write("M400")
        g.write("M42 P32 S0; Pressure off")
        g.write("G91")
        g.write("SEPARATE HERE\n")
  
                                                                                                                                                                                                                      
def concentric_rectangle():
    extra = 0.5*silver_width + 0.5*g.extrusion_width
    Xo = silver_length + extra
    Yo = g.extrusion_width + 2*silver_width
    count = 0
    x_length = 0
    while x_length < total_x_width:
        g.move(x=Xo+g.extrusion_width*count)
        g.move(y=Yo+g.extrusion_width*count)
        count = count + 1
        g.move(x=-(Xo + g.extrusion_width*count))
        g.move(y=-(Yo + g.extrusion_width*count))
        count = count + 1
        x_length = count*g.extrusion_width + Xo

        
bottom_width = bottom_width + extrusion_width
top_width = top_width + extrusion_width
bottom_length = bottom_length + extrusion_width
top_length = top_length + extrusion_width
theta1= (np.arctan2(fin_height-layer_height, ((bottom_length-top_length)/2)))
theta2= (np.arctan2(fin_height-layer_height, ((bottom_width-top_width)/2)))
theta2_degrees = (theta2/np.pi)*180
print "theta2: {}".format(theta2_degrees)
length_change_per_layer = layer_height/np.tan(theta1)*2
width_change_per_layer = layer_height/np.tan(theta2)*2
print "width_change_per_layer: {}".format(width_change_per_layer)
layers = int(fin_height/layer_height)-1
print "layers: {}".format(layers)                
                        
                                        
def fin(layers, int_widths, extrusion_width, layer_height=0.15):
    
    for i in range(layers):
        current_width = bottom_width - extrusion_width - width_change_per_layer*(i)
        current_length = bottom_length -extrusion_width - length_change_per_layer
        num_widths = current_width/extrusion_width
        int_widths = int(num_widths)
        if int_widths%2!=0:
            int_widths = int_widths-1
        #starting_point = [(0,0)]
        starting_point = (top_left[0]+0.5*extrusion_width+((width_change_per_layer/2)*i), top_left[1]-(0.5*extrusion_width)-((length_change_per_layer/2)*i))
        current_z = layer_height + layer_height*i
        g.abs_move(starting_point[0], starting_point[1])
        g.abs_move(Z=current_z)
        print "int widths: {}".format(int_widths)
        for j in range(int_widths/2):
                      
            g.extrude = True
            g.extrusion_width = 0.35
            g.layer_height = 0.15
            g.move(x=current_width-2*j*extrusion_width, y=0)
            g.move(y=-(current_length-2*j*extrusion_width))
            g.move(x=-(current_width-2*j*extrusion_width))
            g.move(y=current_length-0.5*extrusion_width-2*j*extrusion_width)
            g.move(x=extrusion_width, y=-0.5*extrusion_width)
        g.extrude = False
        #retract
        
def silver_upwards_meander(Ag_bottom_length, Ag_top_length, meander_space, layer_height, offset, width_change_per_layer = 0.04375, side = 'left'):
    if side == 'left':
        starting_point = ((top_left[0]- 0.5*silver_width - offset), (top_left[1]- ((bottom_length-Ag_bottom_length)/2)))
        direction = 1
    else:
        starting_point = ((top_left[0]- 0.5*silver_width - offset), (top_left[1]- ((bottom_length-Ag_bottom_length)/2)))#fix this
        direction = -1
    g.abs_move(starting_point[0], starting_point[1])
    
    for i in range(layers):
        current_z = layer_height + layer_height*i
        g.abs_move(Z=current_z)
        #pressure_on
        g.move(y
        
              
    #print "num width: {}".format(num_widths)
    #
    #print int_widths
fin(top_left = top_left, bottom_length = 10, top_length = 8, bottom_width = 0.35*6, top_width = 0.7, fin_height = 0.15*33)

#g.view()                                        
g.teardown()