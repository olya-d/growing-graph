import colorsys

def rgb_to_str(rgb):
    rgb255 = [min(int(d*256), 255) for d in rgb]
    return '#%02x%02x%02x' % (rgb255[0], rgb255[1], rgb255[2])

def distinct_colors(n):
    return [rgb_to_str(colorsys.hsv_to_rgb(*(x*1.0/n, 0.5, 0.5))) for x in range(n)]