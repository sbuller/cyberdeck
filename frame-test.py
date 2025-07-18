import cadquery as cq

# all measurements in mm.

width = 235
length = 183
depth = 10
thickness = 15
textWidth = thickness *4

screen_standoff_diameter = 2.05
screen_standoff_hole = 6
screen_standoff_width = 218.1
screen_standoff_height = 133

screen_body_width = 2 + 239 - 13.225 + 6.295 - 7.665 + 6.295
screen_body_height = 2 + 133 + 6.05*2 - screen_standoff_diameter
screen_body_depth = 5.5
#screen_body_offset = 5.56
screen_body_offset = 2.2

screen_belly_width = 50
screen_belly_height = 80
# centered in y
screen_belly_x_offset = 82
screen_belly_depth = 4

depth = screen_body_depth + 4.2

fin_length = 20 - 4.1
fin_width = 50
fin_thickness = 3

brim_width = 3
brim_thickness = 1.5

version = 6

# TODO: bottom frame should tuck under screen
# edge. Bottom panel should be thinned for
# placement of connectors and controls.
# connectors and controls should be selected
# and placed
# 4xUSB?
# Barrel jack DC in.
# XT-60 out
# Power button
# multiple LAN ports
# WAN port
# Serial port?
# Antenna connector?
# passthrough or connector for keyboard


frame = (
    cq.Workplane("XY")
    .box(width, length, depth)
    .tag("firstbox")
    .edges("|Z")
    .fillet(11)
    .workplane(depth/2)
    .box(width+brim_width*2, length+brim_width*2, brim_thickness)
    .edges("|Z")
    .fillet(14)
    .faces(">Z")
    .workplane()
    .tag("frame")
    )

screen_recess = (
    frame
    .center(screen_body_offset,9)
    .tag("recess")
    .rect(screen_body_width, screen_body_height)
    .cutBlind(-screen_body_depth-brim_thickness)
    .faces(">Z").workplane()
    .rect(width+22,screen_body_height+3)
    .cutBlind(-1.5)
    .workplaneFromTagged("recess")
    .rect(screen_standoff_width, screen_standoff_height, forConstruction=True)
    .vertices()
    .hole(screen_standoff_hole, brim_thickness + screen_body_depth + 4.2)
    .center(-screen_body_offset,-9)
    )

belly_recess = (
    screen_recess
    .workplaneFromTagged("firstbox")
    .moveTo(screen_belly_x_offset,9)
    .rect(screen_belly_width,screen_belly_height)
    .cutBlind(-screen_belly_depth)
    )

with_fins = (
    belly_recess
    .faces("<Z", "firstbox")
    .workplane()
    .rarray(150, length-fin_thickness, 2, 2)
    .rect(fin_width,fin_thickness)
    .extrude(fin_length)
    .rarray(width-fin_thickness, 80, 2, 2)
    .rect(fin_thickness, fin_width)
    .extrude(fin_length)
    )

ports = (
    with_fins
    .faces(">Z")
    .workplane()
    .moveTo(0, 4+(2*screen_body_offset - length - screen_body_height)/4)
    .rect(width - 30,20)
    .cutThruAll()
    )

final = (
    ports
    .faces(">Z")
    .workplane()
    .moveTo(screen_body_offset,9)
    .rect(screen_body_width - thickness*2, screen_body_height - thickness*2)
    .cutThruAll()
    )

show_object(final)

cq.exporters.export(final, "frame-test.step")
