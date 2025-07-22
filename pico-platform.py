import cadquery as cq

peg_points = [
    (3.571875,-25.003125),
    (14.2875,25.003125),
    (-14.2875,25.003125)
    ]

result = (cq.Workplane("XY")
    # Base
    .rect(36,60)
    .extrude(1)
    .edges("|Z")
    .fillet(3.5)
    # Mounting pegs
    .pushPoints(peg_points)
    .circle(3.5/2)
    .extrude(7.7)
    # pico shafts for inserts
    .faces("<Z").workplane()
    .rect(17.78, 48.26, forConstruction=True)
    .vertices()
    .circle(7.2/2)
    .extrude(-6.7)
    # holes for the inserts
    .faces("<Z").workplane()
    .rect(17.78, 48.26, forConstruction=True)
    .vertices()
    .hole(4)
    )

show_object(result)

cq.exporters.export(result, "pico-platform.step")