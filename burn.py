import os, sys, math, copy, random
import colorama
import numpy as np
import matplotlib.pyplot as plt

colorama.init()

class Burn():
    """simulator for fuel grain burn process"""
    def __init__(self, erode_radii, dim=100, grid=None):
        self.seen = set()
        self.inner_border = set()
        self.outer_border = set()
        self.erode_radii = erode_radii
        self.dim = dim
        if grid == None:
            self.grid = np.zeros((dim, dim))-1
        else:
            self.grid = grid

    def find_edge(self):
        """locate the current edge of points in grid without the value 0.  Ignore points with value -1"""
        self.inner_border = copy.deepcopy(self.outer_border)
        self.outer_border = set()
        while len(self.inner_border)>0:
            index = self.inner_border.pop()
            self.seen.add(index)
            neighbors = self.find_neighbors(index, 1)
            for n in neighbors:
                if n not in self.seen:
                    if self.grid[n] == 0:
                        self.inner_border.add(n)
                    elif self.grid[n] != -1:
                        self.outer_border.add(n)

    def find_neighbors(self, index, radius):
        """find all other indicies still within the grid within radius of the index"""
        idx = index[0]
        idy = index[1]
        neighbors = []
        for temp_x in xrange(0, radius+1):
            #calculate the +/- y range given the target radius and xvalue
            y_range = int(math.sqrt(radius**2-temp_x**2))
            for temp_y in xrange(0, y_range+1):
                if idx+temp_x<self.dim and idy+temp_y<self.dim:
                    neighbors.append((idx+temp_x, idy+temp_y))
                if idx+temp_x<self.dim and idy-temp_y >= 0:
                    neighbors.append((idx+temp_x, idy-temp_y))
                if idx-temp_x>=0 and idy+temp_y<self.dim:
                    neighbors.append((idx-temp_x, idy+temp_y))
                if idx-temp_x>=0 and idy-temp_y >= 0:
                    neighbors.append((idx-temp_x, idy-temp_y))
        return neighbors

    def step(self):
        """Find the edge, then erode along that edge"""
        self.find_edge()
        removed = self.erode()
        return removed

    def erode(self):
        """iterate over the outer border; for any points of indentical type to the current one,
        and within the region specified by erode_radius, change their value to zero.  Return a count of nodes removed"""
        #TODO prevent paths from passing through other areas
        new_grid = copy.deepcopy(self.grid)
        removed = 0
        for index in self.outer_border:
            #get the radius for the point currently under inspection
            if self.grid[index] != -1:
                radius = self.erode_radii[self.grid[index]]
                new_grid[index] = 0
                removed += 1
                for n in self.find_neighbors(index, radius):
                        if self.grid[n] == self.grid[index]:
                            new_grid[n] = 0
                            removed += 1
        self.grid = copy.deepcopy(new_grid)
        return removed

    def simulate(self, start_index, save_history=False):
        """iterate through the simulation until there are no burnable points left.
        If save_history is true, the grid at each point will be saved in an array"""
        self.outer_border = set([start_index])
        if save_history:
            history = [copy.deepcopy(self.grid)]
        else:
            history = None
        removal = []
        removed = self.step()
        removal.append(removed)
        if save_history:
            history.append(copy.deepcopy(self.grid))
        while len(self.outer_border) > 0:
            removed = self.step()
            removal.append(removed)
            if save_history:
                history.append(copy.deepcopy(self.grid))
        return removal, history

    def print_grid(self, grid=None):
        if grid == None:
            grid = self.grid
        for row in list(grid):
            out_row = []
            for e in row:
                if e == -1:
                    out_row.append(colorama.Back.BLACK+' ')
                elif e == 1:
                    out_row.append(colorama.Back.GREEN+' ')
                elif e == 0:
                    out_row.append(colorama.Back.BLACK+' ')
            out_row = ' '.join(out_row)
            print out_row

def make_cylinder(dim, inner_radius, outer_radius):
    grid = np.zeros((dim, dim)) - 1
    center = dim/2.0
    inner_r2 = (dim/2.0*inner_radius)**2
    outer_r2 = (dim/2.0*outer_radius)**2
    for x in xrange(0, dim):
        for y in xrange(0, dim):
            if (x-center)**2+(y-center)**2>outer_r2:
                grid[(x,y)] = -1
            elif (x-center)**2+(y-center)**2>inner_r2:
                grid[(x,y)] = 1
            else:
                grid[(x,y)] = 0
    return grid

def grid2polar(x,y,dim):
    center = dim/2.0
    x_arm = x-center
    y_arm = y-center
    rad = math.sqrt(x_arm**2+y_arm**2)
    ang = math.atan2(y_arm,x_arm)
    return ang, rad

def make_wagonwheel(dim, inner_radius, outer_radius, hole_ang, symmetry=4, inner_offset = 0.3, outer_offset = 0.3):
    grid = np.zeros((dim, dim))
    center = dim/2.0
    inner_r = (dim/2.0*inner_radius)
    outer_r = (dim/2.0*outer_radius)
    outer_lim = outer_r-(outer_r-inner_r)*outer_offset
    inner_lim = inner_r+(outer_r-inner_r)*inner_offset
    for x in xrange(0, dim):
        for y in xrange(0, dim):
            ang, rad = grid2polar(x,y, dim)
            if rad>outer_r:
                grid[(x,y)] = -1
            elif rad<inner_r:
                grid[(x,y)] = 0
            elif ang%(2*math.pi/symmetry)<hole_ang and rad<outer_lim and rad>inner_lim:
                grid[(x,y)] = 0
            else:
                grid[(x,y)] = 1
    return grid

def make_wagonwheel_2mat(dim, inner_radius, outer_radius, hole_ang, symmetry=4, inner_offset = 0.3, outer_offset = 0.3):
    grid = np.zeros((dim, dim))
    center = dim/2.0
    inner_r = (dim/2.0*inner_radius)
    outer_r = (dim/2.0*outer_radius)
    outer_lim = outer_r-(outer_r-inner_r)*outer_offset
    inner_lim = inner_r+(outer_r-inner_r)*inner_offset
    for x in xrange(0, dim):
        for y in xrange(0, dim):
            ang, rad = grid2polar(x,y, dim)
            if rad>outer_r:
                grid[(x,y)] = -1
            elif rad<inner_r:
                grid[(x,y)] = 0
            elif ang%(2*math.pi/symmetry)<hole_ang and rad<outer_lim and rad>inner_lim:
                grid[(x,y)] = 2
            else:
                grid[(x,y)] = 1
    return grid

def make_shells(dim, inner_radius, outer_radius, shells=[{"rad":[0.2,0.8],"mat":1}]):
    grid = np.zeros((dim, dim))
    center = dim/2.0
    for x in xrange(0, dim):
        for y in xrange(0, dim):
            ang, rad = grid2polar(x,y, dim)
            for s in shells:
                if rad>s["rads"][0]*dim/2.0 and rad<s["rads"][1]*dim/2.0:
                    grid[x,y]=s["mat"]
            if rad>outer_radius*dim/2.0:
                grid[x,y]=-1
            if rad<inner_radius*dim/2.0:
                grid[x,y]=0
    return grid


def make_holey_moley(dim, inner_radius, outer_radius, hole_rad, hole_count, hole_mat=0, seed=100):
    grid = np.zeros((dim, dim))
    center = dim/2.0
    inner_r = (dim/2.0*inner_radius)
    outer_r = (dim/2.0*outer_radius)
    rad_offset = (outer_r-inner_r)/3.0
    for x in xrange(0, dim):
        for y in xrange(0, dim):
            ang, rad = grid2polar(x,y, dim)
            if rad>outer_r:
                grid[(x,y)] = -1
            elif rad<inner_r:
                grid[(x,y)] = 0
            else:
                grid[(x,y)] = 1
    random.seed(seed)
    for i in xrange(0, hole_count):
        x = random.randint(0,dim-1)
        y = random.randint(0,dim-1)
        while grid[x,y]==-1 or grid[x,y]==0:
            x = random.randint(0,dim-1)
            y = random.randint(0,dim-1)
        grid[x,y] = hole_mat
        ns = find_neighbors((x,y), int(hole_rad*dim), dim)
        for n in ns:
            if grid[n] != -1 and grid[n] != 0:
                grid[n] = hole_mat
    return grid

def find_neighbors(index, radius, dim):
    """find all other indicies still within the grid within radius of the index"""
    idx = index[0]
    idy = index[1]
    neighbors = []
    for temp_x in xrange(0, radius+1):
        #calculate the +/- y range given the target radius and xvalue
        y_range = int(math.sqrt(radius**2-temp_x**2))
        for temp_y in xrange(0, y_range+1):
            if idx+temp_x<dim and idy+temp_y<dim:
                neighbors.append((idx+temp_x, idy+temp_y))
            if idx+temp_x<dim and idy-temp_y >= 0:
                neighbors.append((idx+temp_x, idy-temp_y))
            if idx-temp_x>=0 and idy+temp_y<dim:
                neighbors.append((idx-temp_x, idy+temp_y))
            if idx-temp_x>=0 and idy-temp_y >= 0:
                neighbors.append((idx-temp_x, idy-temp_y))
    return neighbors
