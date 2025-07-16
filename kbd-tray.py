import cadquery as cq

kbd_tray_fillet = 7
kbd_key_recess = 10
kbd_tray_width = 232
kbd_tray_length = 179
kbd_tray_max_depth = 27
kbd_tray_brim_width = 2.5
kbd_tray_brim_fillet = 11

def key():
    pass

result = (
    cq.Workplane("XY")
    .box(kbd_tray_width,kbd_tray_length,10)
    .tag("base")
    .edges("|Z")
    .fillet(kbd_tray_fillet)
    .faces(">Z")
    .workplane()
    .rect(kbd_tray_width+kbd_tray_brim_width*2, kbd_tray_length+kbd_tray_brim_width*2)
    .extrude(1)
    .edges("|Z")
    .fillet(kbd_tray_brim_fillet)
    )

show_object(result)

cq.exporters.export(result, "kbd-tray.stl")