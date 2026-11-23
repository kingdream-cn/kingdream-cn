from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from math import sin

fontdir = Path('/usr/share/fonts/truetype/dejavu')
fonts = {n: ImageFont.truetype(str(fontdir / f'DejaVuSansMono{"-Bold" if n>9 else ""}.ttf'), n) for n in [7,8,19]}
cloud='#ecf4ec'; amber='#ffb66a'; mint='#72ded0'; muted='#9fb8c6'

def scene(frame):
    im=Image.new('RGB',(384,132),'#102233'); d=ImageDraw.Draw(im)
    def box(x,y,w,h,c): d.rectangle((x,y,x+w-1,y+h-1),fill=c)
    def line(points,c,w=1): d.line(points,fill=c,width=w)
    def text(x,y,s,n,c): d.text((x,y),s,font=fonts[n],fill=c,anchor='lt')
    def dot(x,y,r,c): d.ellipse((x-r,y-r,x+r,y+r),fill=c)
    def bot(x,y,wave=False, wire=False):
        edge=mint if wire else '#101f31'; shell='#153c51' if wire else '#e9eee3'; blue='#5ba8bc' if wire else '#a4c2ca'
        box(x-10,y+17,20,15,edge); box(x-8,y+19,16,11,blue)
        box(x-5,y+22,10,5,'#163247'); box(x-2,y+23,4,2,amber)
        box(x-15,y-5,30,24,edge); box(x-12,y-7,24,26,edge)
        box(x-12,y-4,24,19,shell); box(x-10,y-6,20,22,shell)
        box(x-10,y+1,20,10,'#193447'); box(x-8,y+10,16,2,'#234658')
        height=1 if frame in [3,4,27] else 4
        box(x-6,y+4,3,height,mint); box(x+4,y+4,3,height,mint)
        box(x-2,y-12,2,6,blue); box(x-3,y-14,5,3,amber)
        line([(x-8,y+21),(x-15,y+24),(x-15,y+29)],edge,5)
        line([(x-8,y+21),(x-15,y+24),(x-15,y+29)],blue,2)
        hand=(x+19+(frame%6<3)*3,y+3+(frame%6<3)*4) if wave else (x+15,y+29)
        line([(x+8,y+22),(x+15,y+21),hand],edge,5)
        line([(x+8,y+22),(x+15,y+21),hand],blue,2); dot(*hand,2,shell)
        step=0 if wave else round(2*sin(frame*1.5))
        box(x-8,y+31,6,6+step,edge); box(x+2,y+31,6,6-step,edge)
        box(x-9,y+34+step,7,3,blue); box(x+2,y+34-step,7,3,blue)
    box(0,0,384,132,'#0b2335'); box(260,0,124,132,'#302a30')
    for x in range(0,260,12): line([(x,0),(x,131)],'#16394a')
    for y in range(0,132,12): line([(0,y),(259,y)],'#16394a')
    d.polygon([(261,96),(385,96),(385,132),(236,132)],fill='#42383c')
    for x in range(268,400,22): line([(x,96),(x-15,132)],'#574547')
    for y in [103,113,126]: line([(256,y),(383,y)],'#574547')
    for y in range(0,132,7): box(259,y,1,3,'#66838a')
    text(169,16,'SIMULATION',7,mint); text(277,16,'PHYSICAL WORLD',7,amber)
    text(16,23,'KING DREAM',8,muted)
    text(15,43,'Aim & Advance',19,cloud); text(16,72,'Learning Embodied AI',8,mint)
    text(16,103,'OBSERVE / MODEL / ACT',7,muted)
    # Mechanism and shadow stay fixed while the agent tracks across the floor.
    box(330,97,41,10,'#242834'); box(335,92,32,6,'#b08b71')
    joints=[(350,92),(348,66),(367,46),(351,36),(331,44)]
    line(joints,'#171c27',10); line(joints,'#8a8483',6); line(joints,'#dbc2a6',3)
    for x,y in joints[:-1]: dot(x,y,4,'#9a7768'); dot(x,y,2,amber)
    line([(331,44),(329,51),(333,55)],'#d0b3a1',2); line([(331,44),(324,47),(325,53)],'#d0b3a1',2)
    box(319,91,10,10,'#79544b'); box(320,91,8,3,amber)
    for x in range(177,331,7): box(x,111,4,1,amber if x<196+frame*4 else '#7a655c')
    line([(325,107),(331,111),(325,115)],amber)
    x=190+round(106*min(frame,28)/28); y=65+round(sin(frame*1.5))
    bot(x,y,frame>=29,x<260)
    if 19<=frame<=24:
        box(258,28,3,77,mint); box(255,28,1,77,'#35777e')
    return im.resize((768,264),Image.Resampling.NEAREST)



def main():
    output_dir = Path(__file__).resolve().parent.parent / 'assets'
    output_dir.mkdir(exist_ok=True)
    frames = [scene(frame) for frame in range(36)]
    frames[0].save(
        output_dir / 'aim-and-advance.gif',
        save_all=True,
        append_images=frames[1:],
        duration=[120] * 35 + [620],
        loop=0,
        optimize=True,
        disposal=1,
    )


if __name__ == '__main__':
    main()
