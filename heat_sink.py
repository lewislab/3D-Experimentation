from mecode import G
import numpy as np


FDM_feed = 30
silver_feed = 12
retraction_feed = 50
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
outfile = r"C:\Users\tbusbee\Documents\GitHub\3D-Experimentation\gcode.gcode"
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
        
bottom_width = bottom_width + extrusion_width
top_width = top_width + extrusion_width
bottom_length = bottom_length + extrusion_width
top_length = top_length + extrusion_width
theta1= (np.arctan2(fin_height-layer_height, ((bottom_length-top_length)/2)))
theta2= (np.arctan2(fin_height-layer_height, ((bottom_width-top_width)/2)))
theta2_degrees = (theta2/np.pi)*180
print "theta2: {}".format(theta2_degrees)
length_change_per_layer = (layer_height/np.tan(theta1))*2
width_change_per_layer = (layer_height/np.tan(theta2))*2
print "width_change_per_layer: {}".format(width_change_per_layer)
layers = int(fin_height/layer_height)-1
print "layers: {}".format(layers)                
def preamble():
    g.write("G91\nG1 Z15 F1000\nG90\nM106 S0\nM42 P2 S255\nM109 S210\nM280 P0 S80\nM42 P24 S255\nM221 S130\nG28 Y\nG28  ; home all axes\nG29\nG1 X0 Y0 Z20 F3000\nG92 E0\nG1 E-5 F300\nG4 S2\nG1 E20 F300\n;G4 S5\nG92 E0\nG1 Z0 X100 E5 F3000 ; bell move to copy ultimaker\nG92 E0 ; reset extruder value to 0\nM400\n")

def postable():
    g.write("G1 X50 Y115 F2000\nT0\nM104 S0\n")
    
def pressure_on():
    g.write('M400\nM42 P2 S255\n')
    
def pressure_off():
    g.write('M400\nM42 P2 S0\n')
    
def activate_T0():
    g.write("T0\nG91\nG1 Z12 F1000 ; lift up 3\nG90\nG1 X25 F10000\nG1 Y114 F12000 ; go to y max\nG91\nG1 E1.5\nG90\nG1 Z17 F1000; go to proper z wipe height\nG1 X0 F8000; enter wipe brush area\nG1 Y78 ; exit wipe brush area\nG1 Z20 F1000 ; \nG90\nG1 X22 F12000\n;move to z\nG1 Z16 F1000\nG90\n;T0 activated\n")

def activate_T1():
    g.write("T0\nG91\nG1 Y2.5 F10000\nG1 Z14.5 F1000\nG4 P200 \nM400 \nM280 P0 S159\nG90\nT0\nG1 Y113 F10000\nG1 X140 F10000\nG1 Z15.5 F1000\nG1 X150 F3000\nG1 Y105 F3000\nG1 X140 F10000\nG1 Y113 F10000\nG1 X90 F10000\nM400\nT1\n;move to z\nG1 Z22 F1000\n;T1 activated")    

def deactivate_T1():
    g.write("M400 \nM280 P0 S80\n")

def set_speed(speed):
    feed_rate = speed*60
    g.write('G1 F{}\n'.format(feed_rate))
    
    
def retract():
    set_speed(retraction_feed)
    g.move(E=-6.5)
    set_speed(FDM_feed)
    
def unretract():
    set_speed(retraction_feed)
    g.move(E=6.6)  
    set_speed(FDM_feed)                      
                                        
def fin(layers, extrusion_width, layer_height=0.15):
    
    for i in range(layers):
        current_width = bottom_width - extrusion_width - width_change_per_layer*(i)
        current_length = bottom_length -extrusion_width - length_change_per_layer*i
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
        
def silver_upwards_meander(Ag_bottom_length, Ag_top_length, meander_space, layer_height, offset, Ag_feed, width_change_per_layer = 0.04375, side = 'left'):
    if side == 'left':
        starting_point = ((top_left[0]- 0.5*silver_width - offset), (top_left[1]- ((bottom_length-Ag_bottom_length)/2)))
        direction = 1
    else:
        starting_point = ((top_left[0]+ 0.5*silver_width + offset+bottom_width), (top_left[1]- ((bottom_length-Ag_bottom_length)/2)))#fix this
        direction = -1
    g.abs_move(starting_point[0], starting_point[1])
    g.extrude = True
    for i in range(layers):
        current_z = layer_height + layer_height*i
        current_length = Ag_bottom_length
        layer_starting_point = ((starting_point[0] + direction*(width_change_per_layer/2)*i), (starting_point[1]))
        g.abs_move(x=layer_starting_point[0], y= layer_starting_point[1], Z=current_z)
        pressure_on()
        g.move(y=-current_length)
        g.move(x=-1*direction*meander_space)
        g.move(y=current_length)
        g.move(x=direction*meander_space)
    pressure_off()
        
        
        
fin(layers, extrusion_width, layer_height=0.15)
silver_upwards_meander(Ag_bottom_length = top_length, Ag_top_length=top_length, meander_space=0.25, layer_height=layer_height, offset=0.25, Ag_feed=15, width_change_per_layer = 0.04375, side = 'left')
silver_upwards_meander(Ag_bottom_length = top_length, Ag_top_length=top_length, meander_space=0.25, layer_height=layer_height, offset=0.25, Ag_feed=15, width_change_per_layer = 0.04375, side = 'right')

#g.view()                                        
g.teardown()