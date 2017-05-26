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

# mkplot('Accuracy-Cost Tradeoff for Parabolic equation, FMG', cost_fmg, 'AccuracyVsCostFMG3D.pdf', dim=3)
# mkplot('Accuracy-Cost Tradeoff for Parabolic equation, LU', cost_lu, 'AccuracyVsCostLU2D.pdf', dim=2)
# mkplot('Accuracy-Cost Tradeoff for Parabolic equation, LU', cost_lu, 'AccuracyVsCostLU3D.pdf', dim=3)

def stoch_cost_mcmc(dx, implicit, dim, sdim, cost):
    e = error(dt,dx,implicit)
    n = e ** (-2)
    return n * cost(dx, implicit)
def stoch_cost_pce(dt, dx, implicit, dim, sdim, cost):
    e = error(dt,dx,implicit)
    n = numpy.log(1/e) ** sdim
    return n * cost(dt, dx, implicit)
def error_stoch_mcmc(M,dx,sdim):
    return dx**2 + M ** (-0.5)
def error_stoch_pce(M,dx,sdim):
    return dx**2 + 10*numpy.exp(- M ** (1/sdim))
def mkplot_stoch(title, error, filename, dim, sdim):
    M = numpy.logspace(0,5,100)
    lines = []
    for dx in [.05, .1, .2, .4, .8]:
        lines += pyplot.loglog(M*cost_fmg(dx,dx,implicit=True,dim=dim), error_stoch_mcmc(M,dx,sdim), '-')
        lines += pyplot.loglog(M*cost_fmg(dx,dx,implicit=True,dim=dim), error_stoch_pce(M,dx,sdim), '.')
    pyplot.title(title + ', %d parameters' % (sdim,))
    pyplot.ylabel('Spatial+Stochastic Error')
    pyplot.xlabel('Cost')
    pyplot.ylim(0.7*min(error_stoch_mcmc(M[-1],.05,sdim),error_stoch_pce(M[-1],.05,sdim)), 8)
    pyplot.legend(lines[-2:], ('MCMC', 'Spectral PCE'), loc='lower left')
    pyplot.savefig(filename)
    pyplot.clf()

mkplot_stoch('Accuracy-Cost Tradeoff for MCMC vs PCE', error_stoch_mcmc, 'AccuracyVsCostS3.pdf', dim=3, sdim=3)
mkplot_stoch('Accuracy-Cost Tradeoff for MCMC vs PCE', error_stoch_mcmc, 'AccuracyVsCostS4.pdf', dim=3, sdim=4)
mkplot_stoch('Accuracy-Cost Tradeoff for MCMC vs PCE', error_stoch_mcmc, 'AccuracyVsCostS5.pdf', dim=3, sdim=5)
mkplot_stoch('Accuracy-Cost Tradeoff for MCMC vs PCE', error_stoch_mcmc, 'AccuracyVsCostS6.pdf', dim=3, sdim=6)
mkplot_stoch('Accuracy-Cost Tradeoff for MCMC vs PCE', error_stoch_mcmc, 'AccuracyVsCostS8.pdf', dim=3, sdim=8)
