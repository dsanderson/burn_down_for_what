import burn, time, sys, os, subprocess
import numpy as np
import matplotlib.pyplot as plt

def test_grid():
    grid = burn.make_cylinder(20, 0.2, 0.8)
    erode_radii = {1:1}
    B = burn.Burn(erode_radii, 20, grid)
    B.print_grid()

def test_step():
    grid = burn.make_cylinder(20, 0.2, 0.8)
    erode_radii = {1:0}
    B = burn.Burn(erode_radii, 20, grid)
    B.print_grid()
    B.outer_border = set([(10,10)])
    B.step()
    B.print_grid()

def test_sim(size = 20, rad=2):
    grid = burn.make_cylinder(size, 0.2, 0.8)
    erode_radii = {1:rad}
    B = burn.Burn(erode_radii, size, grid)
    removals, history = B.simulate((int(size/2.0),int(size/2.0)), save_history=True)
    #print removals
    #for h in history:
    #    B.print_grid(h)
    #    time.sleep(0.25)
    #print removals
    return removals, history

def plot_grid(grid, dim, fpath, removals):
    plt.subplot(1,2,1)
    x = np.linspace(-1.0,1.0,dim)
    y = np.linspace(-1.0,1.0,dim)
    xv, yv = np.meshgrid(x,y)
    plt.pcolor(xv, yv, grid, cmap='RdBu', vmin=grid.min(), vmax=grid.max())
    plt.subplot(1,2,2)
    xs = np.linspace(0,1,len(removals))
    axes = [min(xs),max(xs),min(removals),max(removals)]
    plt.savefig(fpath, bbox_inches='tight')

def plot_history(outimg, hist, removals):
    xs = np.linspace(0,1,len(removals))
    axes = [min(xs),max(xs),min(removals),max(removals)]
    paths = []
    for i, h in hist:
        fpath = os.getcwd()
        fpath = os.path.join(fpath,'imgs')
        fpath = os.path.join(fpath,'{}.png'.format(i))
        print fpath
        paths.append(fpath)
        plt.subplot(1,2,1)
        x = np.linspace(-1.0,1.0,dim)
        y = np.linspace(-1.0,1.0,dim)
        xv, yv = np.meshgrid(x,y)
        plt.pcolor(xv, yv, grid, cmap='RdBu', vmin=grid.min(), vmax=grid.max())
        plt.subplot(1,2,2)
        plt.plot(xs[:i],removals[:i],'b')
        plt.axis(axes)
        plt.savefig(fpath, bbox_inches='tight')
    make_gif(paths,outimg,2.0)

def make_gif(images, outimg, length):
    delay = length*100/float(len(images))
    command = ['convert', '-delay', str(int(delay)), '-dispose', 'none']
    for i in images:
        #command.append('-page')
        command.append(i)
    command.append(outimg)
    subprocess.call(command)

if __name__ == '__main__':
    #test_grid()
    #test_step()
    dim = 80
    rad = 5
    removals, history = test_sim(dim, rad)
    paths = []
    for i,h in enumerate(history):
        fpath = os.getcwd()
        fpath = os.path.join(fpath,'imgs')
        fpath = os.path.join(fpath,'{}.png'.format(i))
        print fpath
        paths.append(fpath)
        plot_grid(h,dim,fpath)
    outimg = os.getcwd()
    outimg = os.path.join(outimg,'imgs')
    outimg = os.path.join(outimg,'final.gif')
    make_gif(paths, outimg, 2)
