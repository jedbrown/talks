import seaborn
import pandas
from numpy import log10
import matplotlib.pyplot as plt
plt.style.use('seaborn-talk')
plt.tight_layout()

SEC_PER_DAY  = 3600 * 24
DAY_PER_YEAR = 365
SEC_PER_YEAR = SEC_PER_DAY * DAY_PER_YEAR

def cosmo_dt(dx):
    return dx * 6.315789

def node_efficiency(dx, sypd, num_nodes, dt=None):
    if dt is None:
        dt = cosmo_dt(dx)
    return sypd * SEC_PER_YEAR / dx**2 / dt / num_nodes

df = pandas.read_csv('fuhrer2018-scaling.csv')
df['simulated_rate'] = df.SYPD * DAY_PER_YEAR
df['node_efficiency'] = node_efficiency(df.resolution, df.SYPD, df.num_nodes, df.time_step)
df['ms_per_step'] = df.time_step / df.simulated_rate

def ann(fig, sypd, dx, vline=False):
    xy=(cosmo_dt(dx) / (sypd * DAY_PER_YEAR),
        node_efficiency(dx, sypd, 4888))
    fig.annotate(s=f'{sypd} SYPD @ {dx} km',
                 xy=xy,
                 annotation_clip=False)
    ymin, ymax = fig.get_ylim()
    if vline:
        fig.axvline(xy[0], ymax=(log10(xy[1]) - log10(ymin))/(log10(ymax)-log10(ymin)))
    return xy



if True:
    fig = seaborn.scatterplot(data=df, x='num_nodes', y='SYPD', markers=['o', 's', '^', 'D'], style='resolution', hue='machine')
    fig.set_xscale('log')
    fig.set_yscale('log')
    fig.set_xlabel('number of nodes')
    plt.savefig('fuhrer2018-scaling-nodes.pdf', bbox_inches='tight')

if True:
    plt.clf()
    fig = seaborn.scatterplot(data=df, x='ms_per_step', y='node_efficiency', markers=['o', 's', '^', 'D'], style='resolution', hue='machine')
    fig.set_xscale('log')
    fig.set_yscale('log')
    fig.set_xlabel('time per step (s)')
    fig.set_ylabel('rate of work per node')
    fig.set_xlim(left=.01)
    ann(fig, 1, 10)
    ann(fig, 2, 10)
    ann(fig, 5, 10)
    ann(fig, 10, 10)
    ann(fig, 10, 19)
    plt.savefig('fuhrer2018-scaling-time-ann1.pdf', bbox_inches='tight')
    fig.set_xlim(left=.002)
    fig.set_ylim(top=10000)
    ann(fig, 0.1, 1)
    ann(fig, 1, 1, vline=True)
    ann(fig, 5, 1, vline=True)
    plt.savefig('fuhrer2018-scaling-time-ann2.pdf', bbox_inches='tight')
