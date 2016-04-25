import burn, time

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

def test_sim(size = 20):
    grid = burn.make_cylinder(size, 0.2, 0.8)
    erode_radii = {1:2}
    B = burn.Burn(erode_radii, size, grid)
    removals, history = B.simulate((int(size/2.0),int(size/2.0)), save_history=True)
    #print removals
    for h in history:
        B.print_grid(h)
        time.sleep(0.25)
    print removals

if __name__ == '__main__':
    #test_grid()
    #test_step()
    test_sim(40)
