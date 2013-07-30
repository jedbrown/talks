from FIAT import Lagrange,quadrature,shapes,jacobi
from pylab import *

def set_sizes_talk():
    golden = (sqrt(5)-1)/2
    fig_width = 6;
    #fig_size = (fig_width,fig_width*golden)
    fig_size = (fig_width,fig_width/golden)
    rcParams.update({'axes.titlesize': 16,
                     'axes.labelsize': 16,
                     'text.fontsize': 18,
                     'legend.fontsize': 16,
                     #'legend.markerscale' : 8,
                     'xtick.labelsize': 16,
                     'ytick.labelsize': 16,
                     'text.usetex': True,
                     'linewidth': 4,
                     'figure.figsize': fig_size})
    #subplots_adjust(left=0.06,right=0.975,bottom=0.08,top=0.94)
    subplots_adjust(left=0.15,right=0.95,bottom=0.06,top=0.95)

set_sizes_talk()
rcParams.update({'backend': 'png'})
m=5
n=100
u = Lagrange.Lagrange(1,m,shapes.line_point_family_lgl)
ufs=u.function_space()
q=quadrature.make_quadrature(1,n)
x=q.get_points()
t=ufs.tabulate_jet(1,x)
B=t[0][(0,)]
D=t[1][(1,)]
subplot(211)
p = [plot(x,B[i],linewidth=2) for i in range(m+1)]
ylabel('Basis functions')
#xlabel('$\hat{x}$')
subplot(212)
p = [plot(x,D[i],linewidth=2) for i in range(m+1)]
ylim(-10,10)
ylabel('Derivatives')
xlabel('$\hat{x}$')
savefig('lgl.png')


