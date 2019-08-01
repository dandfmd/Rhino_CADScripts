# Origin https://discourse.mcneel.com/t/the-best-way-to-identify-layers-without-objects-to-delete/7690/4

import rhinoscriptsyntax as rs
layers=rs.LayerNames()
for layer in layers:
    if rs.IsLayerEmpty(layer): rs.DeleteLayer(layer)
