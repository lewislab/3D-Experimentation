from mecode import G
import numpy as np


FDM_feed = 16
silver_feed = 15
retraction_feed = 50
travel_speed = 90*60
total_count =0;
width_change = 1
top_left = (96,70)
bottom_length = 10
top_length = 8
bottom_width = 0.35*6
top_width = 0.7
fin_height = 0.15*33
fin_spacing = 4
cross_beam_offset = 1.5
extrusion_width = 0.35
silver_width = 0.25
layer_height = 0.15


# Robomama Outfile
#outfile = r"C:\Users\Lewis Group\Documents\GitHub\Muscular-Thin-Films\MTF_out-new.pgm"

# LeroyComputer Outfile
#outfile = r"C:\Users\Voxel8\Documents\GitHub\3D-Experimentation\gcode.gcode"
#Greentown Trav Comp
outfile = r"C:\Users\Workstation 1\Documents\GitHub\3D-Experimentation\gcode.gcode"
#outfile = r"C:\Users\lewislab\Desktop\3D_experiments\COREXYverticalPlasticE1.12F20.gcode"
#outfile = r"C:\Users\lewislab\Desktop\3D_experiments\Prusa\verticalDual.gcode"
#outfile = r"C:\Users\lewislab\Desktop\3D_experiments\Prusa\Calibration.gcode"



cal_data = None#load_and_curate(calfile, reset_start=(2, -2))

g = G(
    outfile=outfile,
    #header= r"Z:\User Files\Chong\mecode\Vertical Trace\header.gcode",
    #footer= r"Z:\User Files\Chong\mecode\Vertical Trace\footer.gcode",
    #cal_data=cal_data,
    print_lines=False,
    aerotech_include = False, 
    extrude = False,
    layer_height = 0.15, 
    extrusion_width = 0.4,
    filament_diameter = 1.75,
    extrusion_multiplier = 1#1.33,
    )
        
             
def preamble():
    g.write("G91\nG1 Z15 F1000\nG90\nM106 S0\nM42 P2 S255\nM109 S210\nM280 P0 S80\nM42 P24 S255\nM221 S130\nG28 Y\nG28  ; home all axes\nG29\nG1 X0 Y0 Z20 F3000\nG92 E0\nG1 E-5 F300\nG4 S2\nG1 E20 F300\n;G4 S5\nG92 E0\nG1 Z0 X100 E5 F3000 ; bell move to copy ultimaker\nG92 E0 ; reset extruder value to 0\nM400\n")

def postamble():
    g.write("G1 X50 Y115 F2000\nT0\nM104 S0\n")
    
def pressure_on():
    g.write('M400\nM42 P6 S255\n')
    
def pressure_off():
    g.write('M400\nM42 P6 S0\n')
    
def activate_T0():
    g.write("T0\nG91\nG1 Z12 F1000 ; lift up 3\nG90\nG1 X25 F10000\nG1 Y114 F12000 ; go to y max\nG91\nG1 E1.5\nG90\nG1 Z17 F1000; go to proper z wipe height\nG1 X0 F8000; enter wipe brush area\nG1 Y78 ; exit wipe brush area\nG1 Z20 F1000 ; \nG90\nG1 X22 F12000\n;move to z\nG1 Z16 F1000\nG90\n;T0 activated\n")

def activate_T1():
    #g.write("T0\nG91\nG1 Y2.5 F10000\nG1 Z14.5 F1000\nG4 P200 \nM400 \nM280 P0 S159\nG90\nT0\nG1 Y113 F10000\nG1 X140 F10000\nG1 Z15.5 F1000\nG1 X150 F3000\nG1 Y105 F3000\nG1 X140 F10000\nG1 Y113 F10000\nG1 X90 F10000\nM400\nT1\n;move to z\nG1 Z22 F1000\n;T1 activated\nT1\n")    
    g.write('G91\n G1 Z12 F1000\nT1\nM280 P0 S159\n')
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

bottom_width = bottom_width + extrusion_width
top_width = top_width + extrusion_width
bottom_length = bottom_length + extrusion_width
top_length = top_length + extrusion_width
theta1= (np.arctan2(fin_height-layer_height, ((bottom_length-top_length)/2)))
theta2= (np.arctan2(fin_height-layer_height, ((bottom_width-top_width)/2)))
theta2_degrees = (theta2/np.pi)*180
#print "theta2: {}".format(theta2_degrees)
length_change_per_layer = (layer_height/np.tan(theta1))*2
width_change_per_layer = (layer_height/np.tan(theta2))*2
print "width_change_per_layer: {}".format(width_change_per_layer)
layers = 1#int(fin_height/layer_height)-1
#print "layers: {}".format(layers)                                           
                                                                                                                        
def fin(extrusion_width, layer_height=0.15,num_layers=1, start_x=top_left[0],start_y=top_left[1], start_z = 0.15):
    
    if num_layers==0:
        num_layers = int(fin_height/layer_height)-1
    
    g.extrude = False
    set_speed(travel_speed)
    g.abs_move(start_x+0.5*extrusion_width, start_y-(0.5*extrusion_width))
    g.abs_move(Z=start_z)
    unretract()
    for i in range(num_layers):
        current_width = bottom_width - extrusion_width - width_change_per_layer*(i)
        current_length = bottom_length -extrusion_width - length_change_per_layer*i
        num_widths = current_width/extrusion_width
        int_widths = int(num_widths)
        if int_widths%2!=0:
            int_widths = int_widths-1
        #starting_point = [(0,0)]
        starting_point = (start_x+0.5*extrusion_width+((width_change_per_layer/2)*i), start_y-(0.5*extrusion_width)-((length_change_per_layer/2)*i))
        current_z = start_z + 0.05 + layer_height*i
        g.abs_move(starting_point[0], starting_point[1])
        g.abs_move(Z=current_z)
        #print "int widths: {}".format(int_widths)
        
        for j in range(int_widths/2):
                      
            g.extrude = True
            g.extrusion_width = 0.35
            g.layer_height = 0.15
            set_speed(FDM_feed)
            g.move(x=current_width-2*j*extrusion_width, y=0, Z=0)
            g.move(y=-(current_length-2*j*extrusion_width), Z=0)
            g.move(x=-(current_width-2*j*extrusion_width),  Z=0)
            g.move(y=current_length-0.5*extrusion_width-2*j*extrusion_width,  Z=0)
            g.move(x=extrusion_width, y=-0.5*extrusion_width,  Z=0)
    g.extrude = False
    retract()

def fins(extrusion_width, num_fins, fin_spacing, layer_height=0.15,num_layers=1, start_x=top_left[0],start_y=top_left[1], start_z = 0.15):
    
    if num_layers==0:
        num_layers = int(fin_height/layer_height)-1
    
    g.extrude = False
    set_speed(travel_speed)
    g.abs_move(start_x+0.5*extrusion_width, start_y-(0.5*extrusion_width))
    g.abs_move(Z=start_z)
    unretract()
    for i in range(num_layers):
        current_width = bottom_width - extrusion_width - width_change_per_layer*(i)
        current_length = bottom_length -extrusion_width - length_change_per_layer*i
        num_widths = current_width/extrusion_width
        int_widths = int(num_widths)
        if int_widths%2!=0:
            int_widths = int_widths-1
        #starting_point = [(0,0)]
        for r in range(num_fins):
            starting_point = (start_x+0.5*extrusion_width+fin_spacing*r+((width_change_per_layer/2)*i), start_y-(0.5*extrusion_width)-((length_change_per_layer/2)*i))
            current_z = start_z + 0.05 + layer_height*i
            g.abs_move(Z=current_z)
            g.abs_move(starting_point[0], starting_point[1])
            unretract()
            
            #print "int widths: {}".format(int_widths)
            
            for j in range(int_widths/2):                        
                g.extrude = True
                g.extrusion_width = 0.35
                g.layer_height = 0.15
                set_speed(FDM_feed)
                g.move(x=current_width-2*j*extrusion_width, y=0, Z=0)
                g.move(y=-(current_length-2*j*extrusion_width), Z=0)
                g.move(x=-(current_width-2*j*extrusion_width),  Z=0)
                g.move(y=current_length-0.5*extrusion_width-2*j*extrusion_width,  Z=0)
                g.move(x=extrusion_width, y=-0.5*extrusion_width,  Z=0)
            g.extrude = False
            retract()
        
def silver_upwards_meander(cross_beam_layers, bottom_layer_start, Ag_bottom_length, Ag_top_length, meander_space, layer_height, num_layers, offset, Ag_feed, width_change_per_layer = 0.04375, side = 'left', Ag_start_x = top_left[0] , Ag_start_y = top_left[1], Ag_start_z = 0.15):
    if side == 'left':
        starting_point = ((Ag_start_x- 0.5*silver_width - offset), (Ag_start_y- ((bottom_length-Ag_bottom_length)/2)))
        direction = 1
    else:
        starting_point = ((Ag_start_x+ 0.5*silver_width + offset+bottom_width), (Ag_start_y- ((bottom_length-Ag_bottom_length)/2)))#fix this
        direction = -1
    if num_layers==0:
        num_layers = int((fin_height+(cross_beam_layers-1)*layer_height+bottom_layer_start)/layer_height)-1
    g.extrude = False
    g.abs_move(starting_point[0], starting_point[1])
    set_speed(silver_feed)
    
    for i in range(num_layers):
        current_z = layer_height + layer_height*i
        current_length = Ag_bottom_length
        layer_starting_point = ((starting_point[0] + direction*(width_change_per_layer/2)*i), (starting_point[1]))
        g.abs_move(x=layer_starting_point[0], y= layer_starting_point[1], Z=current_z)
        pressure_on()
        g.move(y=-current_length)
        g.move(x=-1*direction*meander_space)
        g.move(y=current_length)
        g.move(x=direction*meander_space)
    print g.current_position
    pressure_off()
    if side!= 'left':
        g.move(x=meander_space, Z=layer_height)
        pressure_on()
        g.meander(x=2, y=8.35, spacing = 0.3, start = 'UR',   orientation = 'x') 
        g.move(z=0.15)
        g.meander(x=2, y=8.35, spacing = 0.3, start = 'LL',   orientation = 'y') 
        pressure_off()
        set_speed(travel_speed)
        g.move(y=12)
        pressure_off()
        g.move(y=5, Z=5)

def silver_top():
    g.abs_move(x=98.637) 
    g.move(z=0.15)
    pressure_on()
    g.meander(x=2.1256, y=8.35, spacing = 0.3, start = 'UR',   orientation = 'x') 
    g.move(z=0.15)
    g.meander(x=2.1256, y=8.35, spacing = 0.3, start = 'LL',   orientation = 'y') 
    pressure_off()
    set_speed(travel_speed)
    g.move(y=12)

def heat_sink(num_fins, length_fins, fin_space, fin_height, bottom_layer_start = 0.18, cross_beam_layers = 2):
    cross_beam_length = cross_beam_offset*2+(num_fins-1)*fin_space + bottom_width
    for j in range(cross_beam_layers):
        g.abs_move((top_left[0]+0.5*extrusion_width-cross_beam_offset), top_left[1]-0.5*extrusion_width)
        g.abs_move(Z=bottom_layer_start+layer_height*j)
        g.extrude = True
        g.move(x=cross_beam_length)
        g.move(y=-(bottom_length-extrusion_width))
        g.move(x=-cross_beam_length)
        g.move(y=(bottom_length-extrusion_width))
        retract()
        g.extrude =False
        for f in range(num_fins):
            fin(extrusion_width, layer_height=layer_height, num_layers = 1, start_x = top_left[0]+fin_space*f, start_y = top_left[1], start_z=bottom_layer_start+layer_height*j)
    g.write(';start fins\n')
    fins(extrusion_width, num_fins, fin_spacing, layer_height=layer_height, num_layers = 0, start_x = top_left[0], start_y = top_left[1], start_z=bottom_layer_start+layer_height*(cross_beam_layers -1))
    
    #for k in range(num_fins):
    #    fin(extrusion_width, layer_height=layer_height, num_layers = 0, start_x = top_left[0]+fin_space*k, start_y = top_left[1], start_z=bottom_layer_start+layer_height*(cross_beam_layers -1))
    for l in range(num_fins):
        silver_upwards_meander(cross_beam_layers, bottom_layer_start,Ag_bottom_length = top_length, Ag_top_length=top_length, meander_space=0.28, layer_height=layer_height, num_layers = 0, offset=0.1, Ag_feed=15, width_change_per_layer = 0.04375
            , side = 'left',Ag_start_x = top_left[0]+fin_space*l , Ag_start_y = top_left[1], Ag_start_z = 0.25)
        set_speed(travel_speed)
        g.move(y=4)
        g.move(Z=10)
        silver_upwards_meander(cross_beam_layers, bottom_layer_start, Ag_bottom_length = top_length, Ag_top_length=top_length, meander_space=0.28, layer_height=layer_height, num_layers = 0, offset=0.1, Ag_feed=15, width_change_per_layer = 0.04375
        , side = 'right',Ag_start_x = top_left[0]+fin_space*l , Ag_start_y = top_left[1], Ag_start_z = 0.25)
    
            
        

            
def skirt():
    set_speed(50)
    g.abs_move(Z=15)
    g.abs_move(x=100, y=3)
    g.abs_move(Z=0.15)
    set_speed(10)
    g.extrude = True
    g.write('M221 S130')
    g.abs_move(x=1, y=3)
    g.write('M221 S100')
    retract()
    g.extrude = False
    set_speed(50)
    g.abs_move(Z=10)
        
def setup():
    preamble()
    g.write('M106\n')
    g.write('M218 T0 X0 Y0 Z0\n')
    g.write(' M218 T1 X57.65 Y-5.9 Z-4.7\n')        
        
setup()
skirt()
unretract()
g.write('M106\n')
heat_sink(num_fins = 3, length_fins = bottom_length, fin_space = 4, fin_height = 5, bottom_layer_start = 0.18)
#fin(layers, extrusion_width, layer_height=0.15, startx = top_left[0], start_y=top_left[1], start_z=0.15)
#g.extrude = False
#g.abs_move(60, 130)
#g.write('G4 S12\n')
#activate_T1()
#
#silver_upwards_meander(Ag_bottom_length = top_length, Ag_top_length=top_length, meander_space=0.28, layer_height=layer_height, offset=0.1, Ag_feed=15, width_change_per_layer = 0.065625
#, side = 'left')
#set_speed(travel_speed)
#g.move(y=4)
#g.move(Z=10)
#silver_upwards_meander(Ag_bottom_length = top_length, Ag_top_length=top_length, meander_space=0.28, layer_height=layer_height, offset=0.1, Ag_feed=15, width_change_per_layer = 0.065625
#, side = 'right')
#silver_top()
postamble()                                        
g.teardown()