import drawSvg as draw
import drawSvg.color
import math

# drawing size
N = 13
M = 10

# the one true circle constant
tau = math.pi*2

drawing = draw.Drawing(M*50, N*50, origin=(-1,-1), displayInline=True)

def largest_prime_factor (n):
    max_prime = -1
      
    for i in range(2, int(math.sqrt(n)) + 1):
        while n % i == 0:
            max_prime = i
            n //= i
      
    if n > 1:
        max_prime = n
      
    return int(max_prime)


# color scheme
def col(f):
    return drawSvg.color.Hsv(f,0.7,0.8)

class Viewport:
    cx = 0
    cy = 0
    scale = 200
    angle = tau/4
    
    def __str__(self): #debug
        return f'Viewport(cx={self.cx}, cy={self.cy}, scale={self.scale}, angle={self.angle/tau} tau)'


def draw_number(drawing, viewport, number, number_offset, number_total, recursion_depth = 0):
    if number == 1:
        drawing.append(draw.Circle(viewport.cx, viewport.cy, viewport.scale, fill = col(number_offset / number_total), stroke_width=0.25, stroke='black'))
        return
    
    n = largest_prime_factor(number)
    
    alpha = tau / n
    
    # calculate the major circle radius
    R = viewport.scale
    
    if recursion_depth > 0:
        R *= 0.95 # add some padding between intermediate levels
    
    # calculate the minor circle radius
    r = R - R/(1+math.sin(alpha/2)) # small circle radius needed to form a ring of circles inscribed in R
    d = R-r
    
    # special case for repeated 2-factors to eliminate excessive padding
    if n == 2 and number > 2:
        r *= 1.25
        
    #if n == number: # optional: shade the inside of the smallest prime factor
    #    e = math.cos(alpha/2) * d
    #    drawing.append(draw.Circle(viewport.cx, viewport.cy, e, fill = '#eee'))
    
    for i in range(n):
        angle = (viewport.angle + i/n * tau) % tau
        v = Viewport()
        # rotate the viewport
        v.cx, v.cy = viewport.cx + d * math.cos(angle), viewport.cy + d * math.sin(angle)
        v.scale = r
        v.angle = angle
        if n == 2:
            # special case 90° rotation to make repeated factors 2 tile in both directions (can probably be generalized)
            v.angle += tau/4
        
        # recursion – cycle colors except for the last grouping (unless it's a prime)
        draw_number(drawing, v, number//n, number_offset + (recursion_depth == 0 or n != number) * i * number//n, number_total, recursion_depth+1)
        
viewport = Viewport()

for m in range(N*M):
    x = m % M
    y = N - 1 - m // M
    vp = Viewport()
    vp.cx =  (x+0.5) * 50 + extra_padding_left
    vp.cy =  (y+0.5) * 50
    vp.scale = 23
    
    n = m+1
    if n > 0:
        draw_number(drawing, vp, n, 0, n)
    if n > 3:
        drawing.append(draw.Text(f'{n}',7, vp.cx, vp.cy, text_anchor='middle',center=0.65, fill='#aaa'))

drawing.setPixelScale(4)  # Set number of pixels per geometry unit
#drawing.setRenderSize(400,200)  # Alternative to setPixelScale
drawing.saveSvg('numbers.svg')
drawing.savePng('numbers.png')

# Display in Jupyter notebook
#drawing.rasterize()  # Display as PNG
drawing  # Display as SVG
