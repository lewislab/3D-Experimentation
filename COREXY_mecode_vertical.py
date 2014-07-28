from mecode import G
#from mecode.profilometer_parse import load_and_curate
import numpy as np

silver_length = 5
silver_width = 0.25
total_x_width = 15

extruder_offset = (63.05,0)
orgin = (90, 80)
silver_orgin = (orgin[0]-extruder_offset[0], orgin[1]-extruder_offset[1])
FDM_feed = 20#*60
silver_feed = 4#*60
total_count =0;
dwell_time = 1
travel_speed = 100


# Robomama Outfile
#outfile = r"C:\Users\Lewis Group\Documents\GitHub\Muscular-Thin-Films\MTF_out-new.pgm"

# Travis' Computer Outfile
#outfile = r"C:\Users\tbusbee\Documents\GitHub\Muscular-Thin-Films\MTF_out-testing.txt"
#outfile = r"C:\Users\Administrator\Documents\GitHub\LewisResearchGroup\FILE_NAME.gcode"
#outfile = r"C:\Users\lewislab\Desktop\3D_experiments\COREXYverticalPlastic.gcode"
outfile = r"\\vfiler1.seas.harvard.edu\group0\jlewis\User Files\Chong\mecode\Vertical Trace\verticalDual.gcode"
#outfile = r"C:\Users\lewislab\Desktop\3D_experiments\Calibration.gcode"

simple_g_code = True

cal_data = None#load_and_curate(calfile, reset_start=(2, -2))

g = G(
    #outfile=outfile,
    #header= r"\\vfiler1.seas.harvard.edu\group0\jlewis\User Files\Chong\mecode\Vertical Trace\header.gcode",
    #footer= r"\\vfiler1.seas.harvard.edu\group0\jlewis\User Files\Chong\mecode\Vertical Trace\footer.gcode",
    #cal_data=cal_data,
    print_lines=True,
    aerotech_include = False, 
    extrude = False,
    layer_height = 0.22, 
    extrusion_width = 0.4,
    filament_diameter = 1.75,
    extrusion_multiplier = 1.00,
    )

g.cal_data = None #np.array([[2, -2, 0], [70, -2, -10], [70, -48, -20], [2, -48, -10]])


def calc_extrude_rate(x, y, extrude=True, relative = True, extrusion_width = 0.4, 
                    layer_height = 0.22, multiplier = 1, filament_diameter = 1.75):
    if relative is not True:
        g.absolute()
    
    #area = 3.14159*(layer_height**2)/4 + (layer_height * extrusion_width - layer_height)
    area = layer_height*(extrusion_width-layer_height) + 3.14159*(layer_height/2)**2
    speed = g.speed
    if g.is_relative is not True:
        current_x_pos = g.current_position['x']
        current_y_pos = g.current_position['y']
        print g.current_position['x']
        x_distance = abs(x-current_x_pos)
        y_distance = abs(y-current_y_pos)
        g.abs_move(x=x, y=y)
    else:
        x_distance = x
        y_distance = y
        g.move(x=x, y=y)
           
    line_length = np.sqrt(x_distance**2 + y_distance**2)
    volume = line_length*area
    filament_length = (4*volume)/(3.14149*filament_diameter**2)
    time = line_length/speed
    flow_rate = (area*line_length)/time
    
    print filament_length
    print line_length
    print area

def calibration_cube(layers, retraction, x=10, y=10):
    g.feed(40)
    g.abs_move(orgin[0], orgin[1])
    g.abs_move(z=g.layer_height)
    for i in range(layers):
        if i%2 == 0:
            g.abs_move(orgin[0], orgin[1])
        if i%2 == 1:  
            g.abs_move(orgin[0]+x, orgin[1])  
        g.extrude = True
        g.retract(-retraction)
        if i%2 == 0:
            g.meander(x=x, y=y, spacing = g.extrusion_width, start = 'LL', orientation = 'x')
        if i%2 == 1:
            g.meander(x=x, y=y, spacing = g.extrusion_width, start = 'LR', orientation = 'x')
        g.retract(retraction)
        g.extrude = False
        g.move(z=g.layer_height)
        if i%2 == 0:
            g.abs_move(orgin[0], orgin[1]+y)
        if i%2 == 1:
            g.abs_move(orgin[0] + x, orgin[1]+y)
        g.extrude = True
        g.retract(-retraction)
        if i%2 == 0:
            g.meander(x=x, y=y, spacing = g.extrusion_width, start = 'UL', orientation = 'y')
        if i%2 == 1:
            g.meander(x=x, y=y, spacing = g.extrusion_width, start = 'UR', orientation = 'y')
        g.retract(retraction)
        g.move(z=g.layer_height) 
        g.extrude = False 
           

def print_skirt(x, y):
    if (not simple_g_code):
        start_x = orgin[0] - 5
        start_y = orgin[1] - 5
        g.abs_move(start_x, start_y)
        g.abs_move(z=g.layer_height)
        g.extrude = True
        g.move(y=y )
        g.move(x=x)
        g.move(y=-y)
        g.move(x=-x)                                   
        g.extrude = False
    
def set_feed(feed_rate):
    if (not simple_g_code):
        g.write('M203 X{} Y{}'.format((feed_rate), (feed_rate)))
    
def nozzle_change(nozzle):
    if (not simple_g_code):
        g.move(z=5) # rectraction for change of nozzle
        g.write('T' + str(nozzle))
        if nozzle == '0':
            g.move(*extruder_offset) 
            set_feed(FDM_feed)
        if nozzle == '1':  
            g.move(-extruder_offset[0], -extruder_offset[1]) 
            g.write("; END FDM G CODE")
            g.write("M400")
            g.write("M42 P32 S0; Pressure off")
            g.write("G91")
            set_feed(silver_feed)
            #g.write("G90")
            
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

def retract_fdm():
    if (not simple_g_code):
        g.feed(60)
        g.retract(2)        
    
def pressure_on():
    g.write(" ; Turn pressure on")
    g.write("M400") #finish all current moves
    g.extrude = False
    g.write("M42 P32 S255 ;Pressure On")
    g.dwell(0.5) # dwell for a bit after pressure turned on

def pressure_off():
    g.write("; Turn pressure off")
    g.write("M400")
    g.write("M42 P32 S0")
    g.dwell(0.5)

def extrude_true():
    g.dwell(dwell_time)
    g.extrude = True
    
def extrude_false():
    g.dwell(dwell_time)
    g.extrude = False

def change_nozzle(number):
    g.move(Z = 5)
    nozzle_change('number')
    g.move(Z=-5)

def travel_mode(x,y):
    g.move(Z=5)
    g.abs_move(x,y)
    g.move(Z=-5)
        
#calc_extrude_rate(x = 30, y = 30, extrude=True, relative = False, extrusion_width = 0.4, 
#                    layer_height = 0.22, multiplier = 1, filament_diameter = 1.75)
def silver_3D(layers):
    
    
    for i in range(layers):
        # TRAVEL TO PRINT AREA
        set_feed(FDM_feed) # Set feed rate for FDM print
        extrude_false()   # Make sure extrude is false
        travel_mode(orgin[0], orgin[1] - 0.5*silver_width - 0.5*g.extrusion_width) # Move to print area
        
        # FDM Extrusion
        set_feed(FDM_feed) # Set feed rate for FDM print
        #g.move(Z=-5) # drop extruder 
        extrude_true() # Extrude calculation
        concentric_rectangle() #2D rectangle
        retract_fdm() # retract
        extrude_false() # Make sure it's not extruding
        
        # Ink extrusion
        g.travel_mode(orgin[0], orgin[1]) #move to initial print area
        nozzle_change('1') # change to ink extruder
        g.move(Z =-5) # recompensate height from nozzle_change
        pressure_on()
        g.meander(x=silver_length, y= silver_width, spacing = silver_width, start = 'LL', orientation = 'x')
        pressure_off()
        travel_mode(silver_orgin[0], silver_orgin[1])
        set_feed(FDM_feed)
        g.move(Z=g.layer_height)
        
        # Back to FDM Extrusion, preparing for next layer    
        nozzle_change('0')
        g.dwell(dwell_time)
        


#g.abs_move(orgin[0] - 0.5* (2*silver_width +(total_x_width - silver_length)), orgin[1] - 0.5*silver_width - 0.5*g.extrusion_width)
g.abs_move(Z=g.layer_height)
g.abs_move(Z=g.layer_height + 5)#Z must be capitol lettering in order to work
#dual_calibration()
#g.move(z=5)
silver_3D(5)  


#g.view()
                                            
g.teardown()