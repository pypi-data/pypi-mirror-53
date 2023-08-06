
# -*- coding: utf-8 -*-

u'''Ellipsoidal geodetic (lat-/longitude) and cartesian (x/y/z) classes
L{LatLon} and L{Cartesian} and functions L{areaOf} and L{perimeterOf}
based on I{Charles Karney's} Python implementation of U{GeographicLib
<https://PyPI.org/project/geographiclib>}.

Here's an example usage of C{ellipsoidalKarney}:

    >>> from pygeodesy.ellipsoidalKarney import LatLon
    >>> Newport_RI = LatLon(41.49008, -71.312796)
    >>> Cleveland_OH = LatLon(41.499498, -81.695391)
    >>> Newport_RI.distanceTo(Cleveland_OH)
    866,455.4329098687  # meter

You can change the ellipsoid model used by the Karney formulae
as follows:

    >>> from pygeodesy import Datums
    >>> from pygeodesy.ellipsoidalKarney import LatLon
    >>> p = LatLon(0, 0, datum=Datums.OSGB36)

or by converting to anothor datum:

    >>> p = p.convertDatum(Datums.OSGB36)

@newfield example: Example, Examples
'''

from pygeodesy.datum import Datums
from pygeodesy.ellipsoidalBase import CartesianBase, LatLonEllipsoidalBase
from pygeodesy.lazily import _ALL_LAZY
from pygeodesy.named import Bearing2Tuple, Destination2Tuple, Distance3Tuple
from pygeodesy.points import ispolar  # PYCHOK exported
from pygeodesy.utily import points2, property_RO, unroll180, \
                            wrap90, wrap180, wrap360

# all public contants, classes and functions
__all__ = _ALL_LAZY.ellipsoidalKarney + (
          'Cartesian', 'LatLon',  # classes
          'areaOf', 'isclockwise', 'ispolar', 'perimeterOf')  # functions
__version__ = '19.07.14'


class LatLon(LatLonEllipsoidalBase):
    '''An ellipsoidal L{LatLon} similar to L{ellipsoidalVincenty.LatLon}
       but using I{Charles F. F. Karney's} Python U{GeographicLib
       <https://PyPI.org/project/geographiclib>} to compute the geodesic
       distance, initial and final bearing (azimuths) between two given
       points or the destination point given a start point and an initial
       bearing.

       @note: This L{LatLon}'s methods require the U{GeographicLib
       <https://PyPI.org/project/geographiclib>} package to be installed.
    '''

    def bearingTo(self, other, wrap=False):
        '''DEPRECATED, use method C{initialBearingTo}.
        '''
        return self.initialBearingTo(other, wrap=wrap)

    def bearingTo2(self, other, wrap=False):
        '''Compute the initial and final bearing (forward and reverse
           azimuth) from this to an other point, using Karney's
           Inverse method.  See methods L{initialBearingTo} and
           L{finalBearingTo} for more details.

           @param other: The other point (L{LatLon}).
           @keyword wrap: Wrap and unroll longitudes (C{bool}).

           @return: A L{Bearing2Tuple}C{(initial, final)}.

           @raise ImportError: Package U{geographiclib
                               <https://PyPI.org/project/geographiclib>}
                               not installed or not found.

           @raise TypeError: The B{C{other}} point is not L{LatLon}.

           @raise ValueError: If this and the B{C{other}} point's L{Datum}
                              ellipsoids are not compatible.
        '''
        r = Bearing2Tuple(*self._inverse(other, True, wrap)[1:])
        return self._xnamed(r)

    def destination(self, distance, bearing, height=None):
        '''Compute the destination point after having travelled
           for the given distance from this point along a geodesic
           given by an initial bearing, using Karney's Direct
           method.  See method L{destination2} for more details.

           @param distance: Distance (C{meter}).
           @param bearing: Initial bearing in (compass C{degrees360}).
           @keyword height: Optional height, overriding the default
                            height (C{meter}, same units as C{distance}).

           @return: The destination point (L{LatLon}).

           @raise ImportError: Package U{geographiclib
                               <https://PyPI.org/project/geographiclib>}
                               not installed or not found.

           @example:

           >>> p = LatLon(-37.95103, 144.42487)
           >>> d = p.destination(54972.271, 306.86816)
           >>> d
           LatLon(37°39′10.14″S, 143°55′35.39″E)  # 37.652818°S, 143.926498°E
        '''
        return self._direct(distance, bearing, True, height=height)[0]

    def destination2(self, distance, bearing, height=None):
        '''Compute the destination point and the final bearing (reverse
           azimuth) after having travelled for the given distance from
           this point along a geodesic given by an initial bearing,
           using Karney's Direct method.

           The distance must be in the same units as this point's datum
           axes, conventionally meter.  The distance is measured on the
           surface of the ellipsoid, ignoring this point's height.

           The initial and final bearing (forward and reverse azimuth)
           are in compass degrees.

           The destination point's height and datum are set to this
           point's height and datum.

           @param distance: Distance (C{meter}).
           @param bearing: Initial bearing (compass C{degrees360}).
           @keyword height: Optional height, overriding the default
                            height (C{meter}, same units as C{distance}).

           @return: A L{Destination2Tuple}C{(destination, final)}.

           @raise ImportError: Package U{geographiclib
                               <https://PyPI.org/project/geographiclib>}
                               not installed or not found.

           @example:

           >>> p = LatLon(-37.95103, 144.42487)
           >>> d, f = p.destination2(54972.271, 306.86816)
           >>> d
           LatLon(37°39′10.14″S, 143°55′35.39″E)  # 37.652818°S, 143.926498°E
           >>> f
           307.1736313846665
        '''
        r = Destination2Tuple(*self._direct(distance, bearing, True,
                                            height=height)[:2])
        return self._xnamed(r)

    def distanceTo(self, other, wrap=False):
        '''Compute the distance between this and an other point
           along a geodesic, using Karney's Inverse method.
           See method L{distanceTo3} for more details.

           @param other: The other point (L{LatLon}).
           @keyword wrap: Wrap and unroll longitudes (C{bool}).

           @return: Distance (C{meter}).

           @raise ImportError: Package U{geographiclib
                               <https://PyPI.org/project/geographiclib>}
                               not installed or not found.

           @raise TypeError: The B{C{other}} point is not L{LatLon}.

           @raise ValueError: If this and the B{C{other}} point's L{Datum}
                              ellipsoids are not compatible.

           @example:

           >>> p = LatLon(50.06632, -5.71475)
           >>> q = LatLon(58.64402, -3.07009)
           >>> d = p.distanceTo(q)  # 969,954.1663142084 m
        '''
        return self._inverse(other, False, wrap)

    def distanceTo3(self, other, wrap=False):
        '''Compute the distance, the initial and final bearing along a
           geodesic between this and an other point, using Karney's
           Inverse method.

           The distance is in the same units as this point's datum axes,
           conventially meter.  The distance is measured on the surface
           of the ellipsoid, ignoring this point's height.

           The initial and final bearing (forward and reverse azimuth)
           are in compass degrees from North.

           @param other: Destination point (L{LatLon}).
           @keyword wrap: Wrap and unroll longitudes (C{bool}).

           @return: A L{Distance3Tuple}C{(distance, initial, final)}.

           @raise ImportError: Package U{geographiclib
                               <https://PyPI.org/project/geographiclib>}
                               not installed or not found.

           @raise TypeError: The B{C{other}} point is not L{LatLon}.

           @raise ValueError: If this and the B{C{other}} point's L{Datum}
                              ellipsoids are not compatible.
        '''
        r = Distance3Tuple(*self._inverse(other, True, wrap))
        return self._xnamed(r)

    def finalBearingOn(self, distance, bearing):
        '''Compute the final bearing (reverse azimuth) after having
           travelled for the given distance along a geodesic given
           by an initial bearing from this point, using Karney's
           Direct method.  See method L{destination2} for more details.

           @param distance: Distance (C{meter}).
           @param bearing: Initial bearing (compass C{degrees360}).

           @return: Final bearing (compass C{degrees360}).

           @raise ImportError: Package U{geographiclib
                               <https://PyPI.org/project/geographiclib>}
                               not installed or not found.

           @example:

           >>> p = LatLon(-37.95103, 144.42487)
           >>> b = 306.86816
           >>> f = p.finalBearingOn(54972.271, b)  # 307.1736313846665°
        '''
        return self._direct(distance, bearing, False)

    def finalBearingTo(self, other, wrap=False):
        '''Compute the final bearing (reverse azimuth) after having
           travelled along a geodesic from this point to an other
           point, using Karney's Inverse method.  See method
           L{distanceTo3} for more details.

           @param other: The other point (L{LatLon}).
           @keyword wrap: Wrap and unroll longitudes (C{bool}).

           @return: Final bearing (compass C{degrees360}).

           @raise ImportError: Package U{geographiclib
                               <https://PyPI.org/project/geographiclib>}
                               not installed or not found.

           @raise TypeError: The B{C{other}} point is not L{LatLon}.

           @raise ValueError: If this and the B{C{other}} point's L{Datum}
                              ellipsoids are not compatible.

           @example:

           >>> p = new LatLon(50.06632, -5.71475)
           >>> q = new LatLon(58.64402, -3.07009)
           >>> f = p.finalBearingTo(q)  # 11.297220414306684°

           >>> p = LatLon(52.205, 0.119)
           >>> q = LatLon(48.857, 2.351)
           >>> f = p.finalBearingTo(q)  # 157.83449958372714°
        '''
        return self._inverse(other, True, wrap)[2]

    @property_RO
    def geodesic(self):
        '''Get this C{LatLon}'s U{Geodesic
           <https://GeographicLib.SourceForge.io/html/python/code.html>},
           provided package U{geographiclib
           <https://PyPI.org/project/geographiclib>} is installed.
        '''
        return self.datum.ellipsoid.geodesic

    def initialBearingTo(self, other, wrap=False):
        '''Compute the initial bearing (forward azimuth) to travel
           along a geodesic from this point to an other point,
           using Karney's Inverse method.  See method
           L{distanceTo3} for more details.

           @param other: The other point (L{LatLon}).
           @keyword wrap: Wrap and unroll longitudes (C{bool}).

           @return: Initial bearing (compass C{degrees360}).

           @raise ImportError: Package U{geographiclib
                               <https://PyPI.org/project/geographiclib>}
                               not installed or not found.

           @raise TypeError: The B{C{other}} point is not L{LatLon}.

           @raise ValueError: If this and the B{C{other}} point's L{Datum}
                              ellipsoids are not compatible.

           @example:

           >>> p = LatLon(50.06632, -5.71475)
           >>> q = LatLon(58.64402, -3.07009)
           >>> b = p.initialBearingTo(q)  # 9.141877488906045°

           >>> p = LatLon(52.205, 0.119)
           >>> q = LatLon(48.857, 2.351)
           >>> b = p.initialBearingTo(q)  # 156.1106404059787°

           @JSname: I{bearingTo}.
        '''
        return self._inverse(other, True, wrap)[1]

    def toCartesian(self):
        '''Convert this (geodetic) point to (geocentric) x/y/z
           Cartesian coordinates.

           @return: Ellipsoidal (geocentric) Cartesian point (L{Cartesian}).
        '''
        x, y, z = self.to3xyz()  # ellipsoidalBase.LatLonEllipsoidalBase
        return Cartesian(x, y, z)  # this ellipsoidalVincenty.Cartesian

    def _direct(self, distance, bearing, llr, height=None):
        '''(INTERNAL) Direct Karney method.
        '''
        g = self.datum.ellipsoid.geodesic
        m = g.AZIMUTH
        if llr:
            m |= g.LATITUDE | g.LONGITUDE
        r = g.Direct(self.lat, self.lon, bearing, distance, m)
        t = wrap360(r['azi2'])
        if llr:
            a, b = wrap90(r['lat2']), wrap180(r['lon2'])
            h = self.height if height is None else height
            t = self.classof(a, b, height=h, datum=self.datum), t
        return t

    def _inverse(self, other, azis, wrap):
        '''(INTERNAL) Inverse Karney method.

           @raise TypeError: The B{C{other}} point is not L{LatLon}.

           @raise ValueError: If this and the B{C{other}} point's L{Datum}
                              ellipsoids are not compatible.
        '''
        g = self.ellipsoids(other).geodesic
        m = g.DISTANCE
        if azis:
            m |= g.AZIMUTH
        _, lon = unroll180(self.lon, other.lon, wrap=wrap)
        r = g.Inverse(self.lat, self.lon, other.lat, lon, m)
        t = r['s12']
        if azis:  # forward and reverse azimuth
            t = t, wrap360(r['azi1']), wrap360(r['azi2'])
        return t


class Cartesian(CartesianBase):
    '''Extended to convert (geocentric) L{Cartesian} points to
       Karney-based (ellipsoidal) geodetic L{LatLon}.
    '''

    def toLatLon(self, datum=Datums.WGS84, LatLon=LatLon, **pairs):  # PYCHOK XXX
        '''Convert this (geocentric) Cartesian (x/y/z) point to
           an (ellipsoidal) geodetic point on the specified datum.

           @keyword datum: Optional datum to use (L{Datum}).
           @keyword LatLon: Optional ellipsoidal (sub-)class to return
                            the point (L{LatLon}) or C{None}.
           @keyword pairs: Optional C{name=value} pairs to be set at
                           the B{C{LatLon}} instance.

           @return: The ellipsoidal geodetic point (B{C{LatLon}}) or
                    a L{LatLon3Tuple}C{(lat, lon, height)} if
                    B{C{LatLon}} is C{None}.
        '''
        return CartesianBase._to3LLh(self, datum, LatLon, **pairs)


def _geodesic(datum, points, closed, line, wrap):
    # Compute the area or perimeter of a polygon,
    # using the GeographicLib package, iff installed
    g = datum.ellipsoid.geodesic

    if not wrap:  # capability LONG_UNROLL can't be off
        raise ValueError('%s invalid: %s' % ('wrap', wrap))

    _, points = points2(points, closed=closed)  # base=LatLonEllipsoidalBase(0, 0)

    g = g.Polygon(line)

    # note, lon deltas are unrolled, by default
    for p in points:
        g.AddPoint(p.lat, p.lon)
    if line and closed:
        p = points[0]
        g.AddPoint(p.lat, p.lon)

    # g.Compute returns (number_of_points, perimeter, signed area)
    return g.Compute(False, True)[1 if line else 2]


def areaOf(points, datum=Datums.WGS84, wrap=True):
    '''Compute the area of a (n ellipsoidal) polygon.

       @param points: The polygon points (L{LatLon}[]).
       @keyword datum: Optional datum (L{Datum}).
       @keyword wrap: Wrap and unroll longitudes (C{bool}).

       @return: Area (C{meter}, same as units of the B{C{datum}}
                ellipsoid, squared).

       @raise ImportError: Package U{GeographicLib
              <https://PyPI.org/project/geographiclib>} missing.

       @raise TypeError: Some B{C{points}} are not L{LatLon}.

       @raise ValueError: Insufficient number of B{C{points}} or longitudes
                          not wrapped, unrolled, B{C{wrap}} is C{False}.

       @note: This function requires installation of the U{GeographicLib
              <https://PyPI.org/project/geographiclib>} package.

       @see: L{pygeodesy.areaOf}, L{sphericalNvector.areaOf} and
             L{sphericalTrigonometry.areaOf}.
    '''
    return abs(_geodesic(datum, points, True, False, wrap))


def isclockwise(points, datum=Datums.WGS84, wrap=True):
    '''Determine the direction of a path or polygon.

       @param points: The path or polygon points (C{LatLon}[]).
       @keyword datum: Optional datum (L{Datum}).
       @keyword wrap: Wrap and unroll longitudes (C{bool}).

       @return: C{True} if B{C{points}} are clockwise, C{False} otherwise.

       @raise TypeError: Some B{C{points}} are not C{LatLon}.

       @raise ValueError: Insufficient number of B{C{points}} or B{C{points}}
                          enclose a pole or zero area.

       @note: This function requires installation of the U{GeographicLib
              <https://PyPI.org/project/geographiclib>} package.

       @see: L{pygeodesy.isclockwise}.
    '''
    a = _geodesic(datum, points, True, False, wrap)
    if a > 0:
        return True
    elif a < 0:
        return False
    raise ValueError('polar or zero area: %r' % (points,))


def perimeterOf(points, closed=False, datum=Datums.WGS84, wrap=True):
    '''Compute the perimeter of a (n ellipsoidal) polygon.

       @param points: The polygon points (L{LatLon}[]).
       @keyword closed: Optionally, close the polygon (C{bool}).
       @keyword datum: Optional datum (L{Datum}).
       @keyword wrap: Wrap and unroll longitudes (C{bool}).

       @return: Perimeter (C{meter}, same as units of the B{C{datum}}
                ellipsoid).

       @raise ImportError: Package U{GeographicLib
              <https://PyPI.org/project/geographiclib>} missing.

       @raise TypeError: Some B{C{points}} are not L{LatLon}.

       @raise ValueError: Insufficient number of B{C{points}} or longitudes
                          not wrapped, unrolled, B{C{wrap}} is C{False}.

       @note: This function requires installation of the U{GeographicLib
              <https://PyPI.org/project/geographiclib>} package.

       @see: L{pygeodesy.perimeterOf} and L{sphericalTrigonometry.perimeterOf}.
    '''
    return _geodesic(datum, points, closed, True, wrap)

# **) MIT License
#
# Copyright (C) 2016-2020 -- mrJean1 at Gmail -- All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
