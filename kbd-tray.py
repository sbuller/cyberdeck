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

with open("talleth42.json") as file: kbd_layout = json.load(file)


def scaleKeyPositions(pos):
    return [(x*19.05, y*19.05) for (x,y) in  pos]

kbd_key_positions = scaleKeyPositions(kletools.parse_kle_positions(kbd_layout))
kbd_stab_positions = scaleKeyPositions(kletools.parse_kle_stabilizers(kbd_layout))
kbd_key_position_bounds = max_x, max_y = map(max, zip(*kbd_key_positions))
kbd_key_positions = [(x - max_x/2, -y + max_y/2) for (x,y) in kbd_key_positions]
kbd_stab_positions = [(x - max_x/2, -y + max_y/2) for (x,y) in kbd_stab_positions]

result = (
    cq.Workplane("XY")
    .box(kbd_tray_width,kbd_tray_length,kbd_tray_max_depth)
    .edges("|Z")
    .fillet(kbd_tray_fillet)
    .faces(">Z")
    .workplane()
    .rect(kbd_tray_width+kbd_tray_brim_width*2, kbd_tray_length+kbd_tray_brim_width*2)
    .extrude(1)
    .edges("|Z")
    .fillet(kbd_tray_brim_fillet)
    .faces(">Z")
    .workplane()
    .pushPoints(kbd_key_positions)
    .rect(14,14)
    .cutBlind(-10)
    #.add(key_plate)
    #.cutBlind(-10)
    )

#show_object(result)

cq.exporters.export(result, "kbd-tray.stl")
