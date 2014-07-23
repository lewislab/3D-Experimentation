from mecode import G
#from mecode.profilometer_parse import load_and_curate
import numpy as np

silver_length = 5
silver_width = 0.25
total_x_width = 10
orgin = (60, 50)
extruder_offset = (0,0)#(75, 2)
FDM_feed = 15
silver_feed = 4





# Robomama Outfile
#outfile = r"C:\Users\Lewis Group\Documents\GitHub\Muscular-Thin-Films\MTF_out-new.pgm"

# Travis' Computer Outfile
#outfile = r"C:\Users\tbusbee\Documents\GitHub\Muscular-Thin-Films\MTF_out-testing.txt"
outfile = r"/Users/busbees/Documents/Code/Muscular-Thin-Films\MTF_out-testing.txt"




cal_data = None#load_and_curate(calfile, reset_start=(2, -2))

g = G(
    outfile=outfile,
    header=None,
    footer=None,
    #cal_data=cal_data,
    print_lines=False,
    extrude = False,
    layer_height = 0.22, 
    extrusion_width = 0.4,
    filament_diameter = 1.75,
    extrusion_multiplier = 1,   
    
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

def nozzle_change(nozzle):
    g.move(z=1)
    if nozzle == 'A':
        g.move(*extruder_offset) 
    if nozzle == 'B':
        g.move(-extruder_offset[0], -extruder_offset[1])   
            
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

#calc_extrude_rate(x = 30, y = 30, extrude=True, relative = False, extrusion_width = 0.4, 
#                    layer_height = 0.22, multiplier = 1, filament_diameter = 1.75)
def silver_3D(layers):
    g.abs_move(orgin[0], orgin[1] - 0.5*silver_width - 0.5*g.extrusion_width)
    g.set_home(x=0, y=(- 0.5*silver_width - 0.5*g.extrusion_width))
    for i in range(layers):
        g.abs_move(x=0, y=- 0.5*silver_width - 0.5*g.extrusion_width)
        g.feed(FDM_feed)
        g.extrude = True
        concentric_rectangle()
        g.extrude = False
        g.move(z=1)
        g.abs_move(x=0, y=0)
        nozzle_change('B')
        g.set_home(x=0, y=0)
        g.feed(silver_feed)
        g.meander(x=silver_length, y= silver_width, spacing = silver_width, start = 'LL', orientation = 'x')
        g.abs_move(0, 0)
        g.move(z=g.layer_height)
        nozzle_change('A')
        g.set_home(x=0, y=0)
        

silver_3D(layers = 5)
g.view()
g.teardown()