#!/usr/bin/env python2

from __future__ import division

scalar = 8
index  = 4

def work_interior(m, stencil, overlap):
    return m**3
def work_overlap(m, stencil, overlap):
    if overlap == 0:
        return work_interior(m,stencil,overlap)
    else:
        return (m + 2*stencil*overlap)**3 + work_overlap(m, stencil, overlap-1)
def memory_overlap(m, stencil, overlap):
    return (m + 2*stencil*overlap)**3
def communication_outgoing(m, stencil, overlap):
    return work_interior(m, stencil, overlap) - (m - 2*stencil*overlap)**3
def communication_incoming(m, stencil, overlap):
    return work_overlap(m,stencil,overlap) - work_interior(m, stencil, overlap)

def plot_work(opts):
    import numpy as np
    import matplotlib.pyplot as plt
    def set_sizes_paper():
        def get_dims(args, dflt_width, ratio=(np.sqrt(5)-1)/2):
            inches_per_pt = 1/72.27
            width = inches_per_pt * (args.width_pt if args.width_pt else dflt_width)
            height = width * ratio * 0.9
            return width, height
        fig_size = get_dims(opts, 480)
        plt.rcParams.update({'axes.titlesize': 11,
                         'axes.labelsize': 9,
                         'text.fontsize': 9,
                         'lines.linewidth': 1,
                         'legend.fontsize': 9,
                         'legend.markerscale' : 1,
                         'xtick.labelsize': 8,
                         'ytick.labelsize': 8,
                         'text.usetex': True,
                         'figure.figsize': fig_size,
                         'figure.subplot.left': 0.05,
                         'figure.subplot.right': 0.95})
    set_sizes_paper()
    if opts.format != 'native': plt.rc(('backend', opts.format))
    x = np.arange(6,40,2)
    xv = work_interior(x,0,0)
    y1interior = work_interior(x,1,1)
    
    fig = plt.figure()
    ax1 = fig.add_subplot(131)
    #ax1e = ax1.twinx()
    ax2 = fig.add_subplot(132)
    ax3 = fig.add_subplot(133)
    #ax2e = ax2e.twinx()
    styles = ['-', '--', '-.']
    ax1.set_title('work')
    ax1.loglog(xv, y1interior*2, 'r-', label='$p=1$ x2')
    ax1.loglog(xv, work_overlap(x,1,1), 'rs', label='$p=1, s=2$')
    ax1.loglog(xv, y1interior*3, 'g-', label='$p=2$ x2')
    ax1.loglog(xv, work_overlap(x,2,2), 'go', label='$p=2, s=3$')
    ax1.loglog(xv, y1interior*5, 'b-', label='$p=2$ x4')
    ax1.loglog(xv, work_overlap(x,2,4), 'b^', label='$p=2, s=5$')

    ax2.set_title('memory')
    ax2.loglog(xv, memory_overlap(x,1,1), 'r-', label='$p=1, s=1$')
    ax2.loglog(xv, memory_overlap(x,2,1), 'g-', label='$p=2, s=1$')
    ax2.loglog(xv, memory_overlap(x,2,2), 'go', label='$p=2, s=3$')
    ax2.loglog(xv, memory_overlap(x,2,4), 'b^', label='$p=2, s=5$')

    ax3.set_title('communication')
    ax3.loglog(xv, communication_incoming(x,1,1), 'rs', label='$p=1, s=1$')
    ax3.loglog(xv, communication_incoming(x,2,1)*3, 'g-', label='$p=2$ x3')
    ax3.loglog(xv, communication_incoming(x,2,3), 'go', label='$p=2, s=3$')
    ax3.loglog(xv, communication_incoming(x,2,1)*5, 'b-', label='$p=2$ x5')
    ax3.loglog(xv, communication_incoming(x,2,5), 'b^', label='$p=2, s=5$')
    #ax1.set_ylabel('work (vertices)')
    #ax2.set_ylabel('communication (vertices)')
    plt.axes(ax2); plt.legend(loc='lower right')
    # idx = [0,2,4,1,3,5]
    # legend = plt.figlegend((ax1.lines[i] for i in idx),
    #                        (ax1.lines[i].get_label() for i in idx),
    #                        #(0.555,0.6), frameon=False)
    #                        (0.68,0.12), frameon=True)
    # plt.axes(ax2); plt.xticks(nrange-1); plt.ylim(35)
    # plt.axes(ax1); plt.xticks(nrange-1); plt.xlim(min(nrange-1),max(nrange-1)); plt.ylim(60,50e3)
    # plt.axes(ax2e); plt.xticks(nrange-1); plt.xlim(min(nrange-1),max(nrange-1)); plt.yticks([])
    # plt.axes(ax1e); plt.xticks(nrange-1); plt.xlim(min(nrange-1),max(nrange-1)); plt.yticks([])
    #plt.show()
    plt.savefig(opts.output, dpi=600)

def main():
    import argparse
    parser = argparse.ArgumentParser(description='SpMV performance model')
    parser.add_argument('--plot', action='store_true')
    parser.add_argument('--format', choices='native png jpg eps pdf'.split(), help='Output format for plotting')
    parser.add_argument('--width-pt', help='Width, in LaTeX points, of the figure', type=float)
    parser.add_argument('-o', '--output', help='Output filename')
    opts = parser.parse_args()
    plot_work(opts)

if __name__ == "__main__":
    try: main()
    except:
        import pdb, traceback, sys
        type, value, tb = sys.exc_info()
        traceback.print_exc()
        pdb.post_mortem(tb)
