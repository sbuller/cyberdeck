import cadquery as cq

peg_points = [
    (-3.571875,-25.003125),
    (14.2875,25.003125),
    (-14.2875,25.003125)
    ]

result = (cq.Workplane("XY")
    # Base
    .rect(35,56)
    .extrude(1)
    .edges("|Z")
    .fillet(3.5)
    # Mounting pegs
    .pushPoints(peg_points)
    .circle(3.3/2)
    .extrude(7.7)
    .faces("+Z").faces("<Z")
    .fillet(0.6)
    # pico shafts for inserts
    .faces("<Z").workplane()
    .rect(11.4, 47, forConstruction=True)
    .vertices()
    .circle((3+1.6*2)/2+0.2)
    .extrude(-6.1)
    # holes for the inserts
    .faces("<Z").workplane()
    .rect(11.4, 47, forConstruction=True)
    .vertices()
    .hole(3+0.2)
    )

show_object(result)

cq.exporters.export(result, "pico-platform.step")