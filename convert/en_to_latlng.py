import sys

def usage():
  print """
Convert easting northings files into latitude longitude

Usage:
	python en_to_latlng.py [filename]

If filename is not supplied then list is read from stdin.

The post code list should be supplied with one post code per line:
   <easting> <northing> <tag>

Example:
   519963 403141 DN377JX
   519496 404626 DN37 7JY
"""

if __name__=="__main__":

    from mapnik import Projection, Coord

    britishProj = Projection('+init=epsg:27700') # British National Grid
    
    pts = []
    fp = sys.stdin
    if len(sys.argv) > 1:
        fp = open(sys.argv[1],'r')
    else:
        usage()
        sys.exit(2)

    for line in fp:
        fld = line.split()
        c = Coord(float(fld[0]), float(fld[1]))
        c = britishProj.inverse(c)
	### Coord is now in lat/lng

        print c.y,c.x," ".join(fld[2:])
