import os
import gerberex
from gerberex.dxf import DxfFile
import gerber
from gerber.render.cairo_backend import GerberCairoContext

def merge():
    ctx = gerberex.GerberComposition()
    a = gerberex.read('test.GTL')
    a.to_metric()
    ctx.merge(a)

    b = gerberex.read('test.GTL')
    b.to_metric()
    b.offset(0, 25)
    ctx.merge(b)

    c = gerberex.read('test2.GTL')
    c.to_metric()
    c.offset(0, 60)
    ctx.merge(c)

    c = gerberex.read('test.GML')
    c.to_metric()
    ctx.merge(c)

    ctx.dump('test-merged.GTL')

def merge2():
    ctx = gerberex.DrillComposition()
    a = gerberex.read('test.TXT')
    a.to_metric()
    ctx.merge(a)

    b = gerberex.read('test.TXT')
    b.to_metric()
    b.offset(0, 25)
    ctx.merge(b)

    c = gerberex.read('test2.TXT')
    c.to_metric()
    c.offset(0, 60)
    ctx.merge(c)

    ctx.dump('test-merged.TXT')


os.chdir(os.path.dirname(__file__))

file = gerberex.read('data/outline.dxf')
file.to_metric()
file.width = 0.1
file.write('outputs/outline-line.gml')
file.draw_mode = DxfFile.DM_MOUSE_BITES
file.width = 0.5
file.pitch = 1
file.write('outputs/outline.gml')
file.format = (3,3)
file.write('outputs/outline.txt', filetype=DxfFile.FT_EXCELLON)
file.draw_mode = DxfFile.DM_LINE
file.width = 0.1
file.write('outputs/outline-line.txt', filetype=DxfFile.FT_EXCELLON)

dxf = gerberex.read('data/fill.dxf')
dxf.to_metric()
dxf.rotate(30)
dxf.offset(100, 50)
dxf.width = 0.05
dxf.to_inch()
dxf.draw_mode = DxfFile.DM_LINE
dxf.write('outputs/fill-outline.gml')
dxf.draw_mode = DxfFile.DM_FILL
dxf.write('outputs/fill.gml')

ctx = gerberex.GerberComposition()
base = gerberex.rectangle(width=12, height=12, left=-1, bottom=-1, units='metric')
base.draw_mode = base.DM_FILL
ctx.merge(base)
top = gerberex.read('data/ref_gerber_metric.gtl')
ctx.merge(top)
ctx.dump('outputs/negative.gtl')

ctx = gerberex.GerberComposition()
t1 = gerberex.read('data/ref_gerber_metric.gtl')
t1.rotate(20)
ctx.merge(t1)
t2 = gerberex.read('data/ref_gerber_metric.gtl')
t2.offset(15,0)
ctx.merge(t2)
ctx.dump('outputs/new-merge.gtl')

top = gerberex.read('data/single_quadrant.gtl')
top.write('outputs/single_quadrant.gtl')

top = gerberex.read('data/ref_gerber_metric.gtl')
top.rotate(30)
top.offset(10, 5)
top.write('outputs/newgerber.gtl')
top.to_inch()
top.format = (2, 5)
top.write('outputs/newgerber_inch.gtl')

drill = gerberex.read('data/rout2.txt')
drill.rotate(30, (5, 2))
drill.offset(5,2)
drill.write('outputs/rout.txt')
drill.to_inch()
drill.format = (2, 4)
drill.write('outputs/rout_inch.txt')

ctx = gerberex.DrillComposition()
drill = gerberex.read('data/rout.txt')
ctx.merge(drill)
drill2 = gerberex.read('data/rout.txt')
drill2.rotate(20)
drill2.offset(10, 0)
ctx.merge(drill2)
ctx.dump('outputs/rout.txt')

#merge2()

top = gerberex.read('../tests/data/ref_gerber_metric.gtl')
top = gerber.load_layer('../tests/outputs/RS2724x_rotate.gtl')
ctx = GerberCairoContext(scale=50)
ctx.render_layer(top)
ctx.dump('outputs/test.png')

ctx = gerberex.DrillComposition()
base = gerberex.read('data/base.txt')
dxf = gerberex.read('data/mousebites.dxf')
dxf.draw_mode = DxfFile.DM_MOUSE_BITES
dxf.to_metric()
dxf.width = 0.5
ctx.merge(base)
ctx.merge(dxf)
ctx.dump('outputs/merged.txt')

dxf = gerberex.read('data/mousebite.dxf')
dxf.zero_suppression = 'leading'
dxf.write('outputs/a.gtl')
dxf.draw_mode = DxfFile.DM_MOUSE_BITES
dxf.width = 0.5
dxf.write('outputs/b.gml')
dxf.format = (3,3)
dxf.write('outputs/b.txt', filetype=DxfFile.FT_EXCELLON)
top = gerber.load_layer('outputs/a.gtl')
drill = gerber.load_layer('outputs/b.txt')
ctx = GerberCairoContext(scale=50)
ctx.render_layer(top)
ctx.render_layer(drill)
ctx.dump('outputs/b.png')

file = gerberex.read('data/test.GTL')
file.rotate(45)
file.write('outputs/test_changed.GTL')
file = gerberex.read('data/test.TXT')
file.rotate(45)
file.write('outputs/test_changed.TXT')

copper = gerber.load_layer('test-merged.GTL')
ctx = GerberCairoContext(scale=10)
ctx.render_layer(copper)
outline = gerber.load_layer('test.GML')
outline.cam_source.to_metric()
ctx.render_layer(outline)
drill = gerber.load_layer('test-merged.TXT')
ctx.render_layer(drill)
ctx.dump('test.png')
