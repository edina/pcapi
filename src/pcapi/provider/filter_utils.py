"""
PCAPI QA utils
"""


def point_in_poly(x, y, poly):
    """
    Determine if a point is inside a given polygon or not Polygon is a list of
    (x,y) pairs. This function returns True or False. The algorithm is called
    the "Ray Casting Method".

    x - x coordinate of point
    y - y coordinate of point
    poly - polygon as a list of tuples

    example:
    polygon = [[0,10],[10,10],[10,0],[0,0]]
    inside = point_in_poly(5, 5, polygon)
    """

    n = len(poly)
    inside = False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside

if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(description='Test point in polygon')
    parser.add_argument(
        '-x',
        type = float,
        required = True,
        help = 'x coordinate of point')
    parser.add_argument(
        '-y',
        type = float,
        required = True,
        help = 'x coordinate of point')
    parser.add_argument(
        '-p',
        '--poly',
        required = True,
        help = 'polygon as a list of tuples')

    args = vars(parser.parse_args())
    print point_in_poly(
        args['x'],
        args['y'],
        json.loads(args['poly']))
