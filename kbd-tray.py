import cadquery as cq
import json
import kletools

kbd_tray_fillet = 7
kbd_key_recess = 10
kbd_tray_width = 232
kbd_tray_length = 179
kbd_tray_max_depth = 27
kbd_tray_brim_width = 2.5
kbd_tray_brim_fillet = 11
kbd_tray_draft_angle = 2 # degrees

wire_gap = 2.3

with open("talleth42.json") as file: kbd_layout = json.load(file)


def scaleKeyPositions(pos):
    return [(x*19.05, y*19.05) for (x,y) in  pos]

kbd_key_positions = scaleKeyPositions(kletools.parse_kle_positions(kbd_layout))
kbd_stab_positions = scaleKeyPositions(kletools.parse_kle_stabilizers(kbd_layout))
max_x, max_y = map(max, zip(*kbd_key_positions))
kbd_key_positions = [(x - max_x/2, -y + max_y/2) for (x,y) in kbd_key_positions]
kbd_stab_positions = [(x - max_x/2, -y + max_y/2) for (x,y) in kbd_stab_positions]

key_cutout = (cq.Sketch()
              .rect(14.1,8.5)
              .vertices()
              .rect(1.6*2,3.5)
              .reset()
              .rect(14.1,14.1)
              .clean()
              )

result = (
    cq.Workplane("XY")
    # Frame
    .box(kbd_tray_width,kbd_tray_length,15)
    .edges("|Z")
    .fillet(kbd_tray_fillet)
    # Brim
    .faces(">Z")
    .workplane()
    .rect(kbd_tray_width+kbd_tray_brim_width*2, kbd_tray_length+kbd_tray_brim_width*2)
    .extrude(1)
    .edges("|Z")
    .fillet(kbd_tray_brim_fillet)
    # Keyboard Tray
    .faces(">Z")
    .workplane()
    .center(0,-30)
    .rect(max_x+19.1, max_y+19.1).cutBlind(-10)
    # Key locations
    .faces("+Z").faces("<Z")
    .workplane()
    .pushPoints(kbd_key_positions)
    .placeSketch(key_cutout)
    .cutThruAll()
    # Peg bar
    .faces("+Z").faces("<Z")
    .workplane(-3)
    .pushPoints(kbd_key_positions)
    .rect(14.1,7)
    .extrude(-3)
    # Peg holes
    .faces("+Z").faces("<Z")
    .hole(5.2)
    # h filler
    .faces(">Z").workplane(-5)
    .moveTo(0,max_y/2 - 5*19.05/8)
    .rect(max_x+19.1,4.75)
    # num filler 1&2
    .moveTo(-max_x/2 + .75*19.05, max_y/2)
    .rect(9.5,19.1)
    .moveTo(-max_x/2 + 6.25*19.05, max_y/2)
    .rect(9.5,19.1)
    # space filler 1&2
    .moveTo(-max_x/2+3.125*19.05, -max_y/2)
    .rect(4.75,19)
    .moveTo(-max_x/2+5.625*19.05, -max_y/2)
    .rect(4.75,19)
    # extrude all the fillers
    .extrude(-5.1)
    
    # pocket
    .faces(">Z").workplane()
    .moveTo(0,90)
    .sketch()
    .rect(220,46)
    .vertices()
    .fillet(4)
    .finalize()
    .cutThruAll()
    
    # pico-bay
    .faces("<Z").workplane()
    .moveTo(0,-62)
    .rect(220,20)
    .cutBlind(-12)
    )

#show_object(result)

cq.exporters.export(result, "kbd-tray.stl")
