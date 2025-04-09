# Borrowed from https://scipython.com/blog/quadtrees-2-implementation-in-python/

import numpy as np
import matplotlib
import matplotlib.patches as patches
PREP_MIN, PREP_MAX = 0, 100

cmap = matplotlib.cm.get_cmap('cool')

class Point:
    """A point located at (x,y) in 2D space.

    Each Point object may be associated with a payload object.

    """

    def __init__(self, x, y, c, payload=None):
        self.x, self.y, self.c = x, y, c
        self.payload = payload

    def __repr__(self):
        return '{}: {}'.format(str((self.x, self.y, self.c)), repr(self.payload))
    def __str__(self):
        return 'P({:.6f}, {:.6f}), C({:.6f})'.format(self.x, self.y, self.c)

    def distance_to(self, other):
        try:
            other_x, other_y = other.x, other.y
        except AttributeError:
            other_x, other_y = other
        return np.hypot(self.x - other_x, self.y - other_y)

class Rect:
    """A rectangle (x_min, y_min, x_max, y_max)"""

    def __init__(self, x_min, y_min, x_max, y_max):
        self.west_edge, self.east_edge = x_min, x_max
        self.north_edge, self.south_edge = y_min, y_max

    def __repr__(self):
        return str((self.west_edge, self.east_edge, self.north_edge,
                self.south_edge))

    def __str__(self):
        return '({:.6f}, {:.6f}, {:.6f}, {:.6f})'.format(self.west_edge,
                    self.north_edge, self.east_edge, self.south_edge)

    def contains(self, point):
        """Is point (a Point object or (x,y) tuple) inside this Rect?"""

        try:
            point_x, point_y = point.x, point.y
        except AttributeError:
            point_x, point_y = point

        return (point_x >= self.west_edge and
                point_x <  self.east_edge and
                point_y >= self.north_edge and
                point_y < self.south_edge)

        # ep = 1e-5
        # return (point_x >= self.west_edge + ep and
        #         point_x <  self.east_edge - ep and
        #         point_y >= self.north_edge + ep and
        #         point_y < self.south_edge - ep)

    def intersects(self, other):
        """Does Rect object other interesect this Rect?"""
        ep = 1e-5

        return not (other.west_edge > self.east_edge or
                    other.east_edge < self.west_edge or
                    other.north_edge > self.south_edge or
                    other.south_edge < self.north_edge)

    def draw(self, ax, c='k', lw=0.5, zorder=1, **kwargs):
        x1, y1 = self.west_edge, self.north_edge
        x2, y2 = self.east_edge, self.south_edge
        ax.plot([x1,x2,x2,x1,x1],[y1,y1,y2,y2,y1], c=c, lw=lw, zorder=zorder, **kwargs)


class QuadTree:
    """A class implementing a quadtree."""

    def __init__(self, boundary, max_points, PREP=None, depth=0, max_depth=10):
        """Initialize this node of the quadtree.

        boundary is a Rect object defining the region from which points are
        placed into this node; max_points is the maximum number of points the
        node can hold before it must divide (branch into four more nodes);
        depth keeps track of how deep into the quadtree this node lies.
        """

        self.boundary = boundary
        self.max_points = max_points
        self.points = []
        self.PREP = PREP
        self.depth = depth
        self.max_depth = max_depth
        # A flag to indicate whether this node has divided (branched) or not.
        self.divided = False

    def __str__(self):
        """Return a string representation of this node, suitably formatted."""
        sp = ' ' * self.depth * 2
        s = str(self.boundary) + '\n'
        s += sp + ', '.join(str(point) for point in self.points)
        if not self.divided:
            return s
        return s + '\n' + '\n'.join([
                sp + 'nw: ' + str(self.nw), sp + 'ne: ' + str(self.ne),
                sp + 'se: ' + str(self.se), sp + 'sw: ' + str(self.sw)])

    def calc_PREP(self):
        """Before dividnig the quadtree, self.color should be stored"""
        # Average the color value among contained points inside quadtree
        PREP_avg = 0.
        if self.points is not None and len(self.points)>0:
            for point in self.points:
                PREP_avg += point.c
            PREP_avg = PREP_avg/len(self.points)

            return PREP_avg
        else:
            return self.PREP

            

    def divide(self):
        """Divide (branch) this node by spawning four children nodes."""
        #print('Call Divide:Depth:{}, NumofPoints:{}'.format(self.depth, len(self.points)))

        west_edge, east_edge = self.boundary.west_edge, self.boundary.east_edge
        north_edge, south_edge = self.boundary.north_edge, self.boundary.south_edge
        half_vertical_edge = (west_edge+east_edge)/2.
        half_horizon_edge = (north_edge+south_edge)/2.
        # The boundaries of the four children nodes are "northwest",
        # "northeast", "southeast" and "southwest" quadrants within the
        # boundary of the current node.
        self.nw = QuadTree(Rect(west_edge, north_edge, half_vertical_edge, half_horizon_edge),
                                    self.max_points, self.PREP, self.depth + 1, self.max_depth)
        self.ne = QuadTree(Rect(half_vertical_edge, north_edge, east_edge, half_horizon_edge),
                                    self.max_points, self.PREP, self.depth + 1, self.max_depth)
        self.sw = QuadTree(Rect(west_edge, half_horizon_edge, half_vertical_edge, south_edge),
                                    self.max_points, self.PREP, self.depth + 1, self.max_depth)
        self.se = QuadTree(Rect(half_vertical_edge, half_horizon_edge, east_edge, south_edge),
                                    self.max_points, self.PREP, self.depth + 1, self.max_depth)
        

        self.divided = True

    def insert(self, point):
        """Try to insert Point point into this QuadTree."""

        if not self.boundary.contains(point):
            # The point does not lie inside boundary
            return False

        #print('Before Point Length Check:Depth:{}, NumofPoints:{}'.format(self.depth, len(self.points)))

        if len(self.points) < self.max_points:
            # There's room for our point without dividing the QuadTree.
            #print('When Insertion:Depth:{}, Point:{}'.format(self.depth, point))
            self.points.append(point)
            self.PREP = self.calc_PREP()
            return True

        if self.depth >= self.max_depth:
            #print('Over Max_Depth')
            self.points.append(point)
            self.PREP = self.calc_PREP()
            return True

        # No room: divide if necessary, then try the sub-quads.
        if not self.divided:
            # before divide itself, calc and store the rgba color value
            self.PREP = self.calc_PREP()
            
            self.divide()

            # add existing points which belong to the siblings
            # be careful not to call insert here -> bad recursion will be occurred!
            ne_points = []
            nw_points = []
            se_points = []
            sw_points = []
            
            for remain_point in self.points:
                #print('After Divide Allocate Points:Depth:{}, point:{}'.format(self.depth, remain_point))
                if self.ne.boundary.contains(remain_point):
                    ne_points.append(remain_point)
                elif self.nw.boundary.contains(remain_point):
                    nw_points.append(remain_point)
                elif self.se.boundary.contains(remain_point):
                    se_points.append(remain_point)
                elif self.sw.boundary.contains(remain_point):
                    sw_points.append(remain_point)

            # assert len(ne_points)+len(nw_points)+len(se_points)+len(sw_points)<4,\
            #     "This can not happed: nw:{}, ne:{}, sw:{}, se:{}".format(len(nw_points), len(ne_points), len(sw_points), len(se_points))

            self.ne.points = ne_points
            self.nw.points = nw_points
            self.se.points = se_points
            self.sw.points = sw_points
        
        return (self.nw.insert(point) or
                self.ne.insert(point) or
                self.sw.insert(point) or
                self.se.insert(point)
                )


    def query(self, boundary, found_points):
        """Find the points in the quadtree that lie within boundary."""

        if not self.boundary.intersects(boundary):
            # If the domain of this node does not intersect the search
            # region, we don't need to look in it for points.
            return False

        # Search this node's points to see if they lie within boundary ...
        if self.divided == False:
            for point in self.points:
                #print('boundary:{}, point:{}, edges:{}'.format(boundary, point, (self.boundary.west_edge, self.boundary.north_edge, self.boundary.east_edge, self.boundary.south_edge)))
                if boundary.contains(point):
                    found_points.append(point)
        # ... and if this node has children, search them too.
        if self.divided:
            self.nw.query(boundary, found_points)
            self.ne.query(boundary, found_points)
            self.se.query(boundary, found_points)
            self.sw.query(boundary, found_points)
        return found_points


    def query_circle(self, boundary, centre, radius, found_points):
        """Find the points in the quadtree that lie within radius of centre.

        boundary is a Rect object (a square) that bounds the search circle.
        There is no need to call this method directly: use query_radius.

        """

        if not self.boundary.intersects(boundary):
            # If the domain of this node does not intersect the search
            # region, we don't need to look in it for points.
            return False

        # Search this node's points to see if they lie within boundary
        # and also lie within a circle of given radius around the centre point.
        if self.divided == False:
            for point in self.points:
                if (boundary.contains(point) and
                        point.distance_to(centre) <= radius):
                    found_points.append(point)

        # Recurse the search into this node's children.
        if self.divided:
            self.nw.query_circle(boundary, centre, radius, found_points)
            self.ne.query_circle(boundary, centre, radius, found_points)
            self.se.query_circle(boundary, centre, radius, found_points)
            self.sw.query_circle(boundary, centre, radius, found_points)
        return found_points

    def query_radius(self, centre, radius, found_points):
        """Find the points in the quadtree that lie within radius of centre."""

        # First find the square that bounds the search circle as a Rect object.
        boundary = Rect(*centre, 2*radius, 2*radius)
        return self.query_circle(boundary, centre, radius, found_points)


    def __len__(self):
        """Return the number of points in the quadtree."""

        #npoints = len(self.points)
        npoints = 0

        if self.divided == False:
            npoints = len(self.points)

        if self.divided:
            npoints += len(self.nw)+len(self.ne)+len(self.se)+len(self.sw)
        return npoints

    def draw(self, ax, draw_text=False):
        """Draw a representation of the quadtree on Matplotlib Axes ax."""

        # Draw boundary
        self.boundary.draw(ax)
        if self.divided:
            self.nw.draw(ax)
            self.ne.draw(ax)
            self.se.draw(ax)
            self.sw.draw(ax)

        # Draw rect with average of point.c
        if self.divided == False:
            bbox = (self.boundary.west_edge,\
                    self.boundary.north_edge, \
                    self.boundary.east_edge, \
                    self.boundary.south_edge)

            # color
            color_ratio = (self.PREP - PREP_MIN)/(PREP_MAX-PREP_MIN)
            rgba = cmap(color_ratio)

            epsilon = 5e-4
            rect = patches.Rectangle((bbox[0]+epsilon, bbox[1]+epsilon),
                                bbox[2] - bbox[0] - 2*epsilon,
                                bbox[3] - bbox[1] - 2*epsilon, fill=True,
                                facecolor=rgba, zorder=2)
            ax.add_patch(rect)

            
            
            #draw Text
            ax.text(bbox[0] + 0.50*(bbox[2]-bbox[0]) - 1.5e-3, \
                    bbox[1] + 0.50*(bbox[3]-bbox[1]) - 0.85e-3, str(int(round(self.PREP))),\
                    fontsize=2, zorder=10, color='k')

            #draw Text for numbers
            # ax.text(bbox[0] + 0.50*(bbox[2]-bbox[0]) - 1.5e-3, \
            #         bbox[1] + 0.43*(bbox[3]-bbox[1]) - 0.85e-3, str(len(self.points)),\
            #         fontsize=2, zorder=11)

            # ax.text(bbox[0] + 0.5*(bbox[2]-bbox[0]), \
            #      bbox[1] + 0.5*(bbox[3]-bbox[1]), str(self.divided),\
            #          fontsize=3, zorder=10)
