import cadquery as cq

result = (cq.Workplane()
          .box(20,20,6)
          .faces(">Z")
          .workplane()
          .rect(14.1,14.1)
          .cutThruAll()
          .rect(14.1,8.5)
          .vertices()
          .rect(1.6*2,3.5)
          .cutThruAll()
          .workplane(-3)
          .rect(14.1,7)
          .extrude(3)
          .faces("|Z")
          .hole(5.2)
          )

show_object(result)

cq.exporters.export(result, "switch_holder.stl")