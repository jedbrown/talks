from matplotlib import pyplot
import numpy

UnstableInf = 4

def error(dt, dx, implicit=False):
    stable = dt ** 2 + dx ** 2
    return stable if implicit else numpy.where(dt < 0.5*dx**2, stable, UnstableInf)

def cost_fmg(dt, dx, implicit=False, dim=3):
    return (3. if implicit else 1.) / (dt * dx ** dim)
def cost_lu(dt, dx, implicit=False, dim=3):
    exponent = [None, 1, 1.5, 2]
    return (4/dx**(exponent[dim]-1) if implicit else 1.) / (dt * dx ** dim)

dt = numpy.logspace(-3, 0.2, 100)
mindt = .005

def mkplot(title, cost, filename, dim):
   lines = []
   for dx in [.05, .1, .2, .4, .8]:
       uscore = '' if dx == 0.4 else '_'
       lines += pyplot.loglog(cost(dt,dx,dim=dim), error(dt,dx), '-')
       lines += pyplot.loglog(cost(dt,dx,implicit=True,dim=dim), error(dt,dx,implicit=True), '.')
       pyplot.annotate('$\Delta x=%.2f$' % dx, xy=(cost(mindt,dx,implicit=True,dim=dim),1.2*error(mindt,dx,implicit=True)), backgroundcolor='white')
   pyplot.title(title + ', %dD' % dim)
   pyplot.ylabel('Spatial+Temporal Discretization Error $\Delta x^2 + \Delta t^2$')
   pyplot.xlabel('Cost')
   pyplot.ylim(0.7*error(mindt,.05,implicit=True), 1.9*UnstableInf)
   pyplot.annotate('Explicit unstable $\Delta t > (\Delta x)^2/2$', xy=(cost(.05,0.4,dim=dim),1.2*UnstableInf), backgroundcolor='white')
   pyplot.legend(lines[-2:], ('Explicit', 'Implicit'), loc='lower left')
   pyplot.savefig(filename)
   pyplot.clf()

mkplot('Accuracy-Cost Tradeoff for Parabolic equation, FMG', cost_fmg, 'AccuracyVsCostFMG3D.pdf', dim=3)
mkplot('Accuracy-Cost Tradeoff for Parabolic equation, LU', cost_lu, 'AccuracyVsCostLU2D.pdf', dim=2)
mkplot('Accuracy-Cost Tradeoff for Parabolic equation, LU', cost_lu, 'AccuracyVsCostLU3D.pdf', dim=3)
