import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter
import numpy as np
import matplotlib.cm as cm


def plot_eigs(eigs,xlim=None,ylim=None):
    fig, ax = plt.subplots(1)
    sc = ax.scatter(eigs.real, eigs.imag)
    ax.axvline(0, color='k', linewidth=0.5)
    ax.axhline(0, color='k', linewidth=0.5)
    ax.grid(True)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)

    annot = ax.annotate("", xy=(0, 0), xytext=(20, 20), textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="w"),
                        arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)

    def update_annot(ind):

        pos = sc.get_offsets()[ind["ind"][0]]
        annot.xy = pos
        text = '{:.2f} Hz\n{:.2f}%'.format(pos[1] / (2 * np.pi), -100 * pos[0] / np.sqrt(sum(pos ** 2)))
        annot.set_text(text)
        annot.get_bbox_patch().set_facecolor('C0')
        annot.get_bbox_patch().set_alpha(0.4)

    def hover(event):
        vis = annot.get_visible()
        if event.inaxes == ax:
            cont, ind = sc.contains(event)
            if cont:
                update_annot(ind)
                annot.set_visible(True)
                fig.canvas.draw_idle()
            else:
                if vis:
                    annot.set_visible(False)
                    fig.canvas.draw_idle()

    fig.canvas.mpl_connect("motion_notify_event", hover)


def phasor(vec, start=0j, ax=None, **kwargs):

    if not ax:
        fig, ax = plt.subplots(1, subplot_kw=dict(aspect=1))
    return ax.annotate('',
                       xy=(vec.real + start.real, vec.imag + start.imag),
                       xytext=(start.real, start.imag),
                       arrowprops=dict(arrowstyle='->', **kwargs),
                       annotation_clip=False)


def plot_mode_shape(mode_shape, ax=None, normalize=False, labels=None, xy0=np.empty(0), linewidth=2, auto_lim=False, colors=cm.get_cmap('Set1')):
    if not ax:
        ax = plt.subplot(111, projection='polar')
    if auto_lim:
        ax.set_rlim(0, max(abs(mode_shape)))

    if xy0.shape == (0,):
        xy0 = np.zeros_like(mode_shape)
    ax.axes.get_xaxis().set_major_formatter(NullFormatter())
    ax.axes.get_yaxis().set_major_formatter(NullFormatter())
    ax.grid(color=[0.85, 0.85, 0.85])

    if normalize:
        mode_shape_max = mode_shape[np.argmax(np.abs(mode_shape))]
        if abs(mode_shape_max) > 0:
            mode_shape = mode_shape * np.exp(-1j * np.angle(mode_shape_max)) / np.abs(mode_shape_max)

    max_length = np.max(np.abs(mode_shape))
    threshold = 0.5 * max_length

    # Remove yellow from the color map
    colors = [colors(i / len(mode_shape)) for i in range(len(mode_shape)) if colors(i / len(mode_shape)) != (1.0, 1.0, 0.0, 1.0)]

    pl = []
    for i, (vec, xy0_) in enumerate(zip(mode_shape, xy0)):
        if np.abs(vec) >= threshold:
            pl.append(ax.annotate("",
                                  xy=(np.angle(vec), np.abs(vec)),
                                  xytext=(np.angle(xy0_), np.abs(xy0_)),
                                  arrowprops=dict(arrowstyle="->",
                                                  color=colors[i % len(colors)])))
            

    if labels is not None:
        handles = [plt.Line2D([0], [0], color=colors[i % len(colors)], lw=2) for i in range(len(mode_shape)) if np.abs(mode_shape[i]) >= threshold]
        ax.legend(handles, [labels[i] for i in range(len(mode_shape)) if np.abs(mode_shape[i]) >= threshold], loc='center left', bbox_to_anchor=(1, 0.5), fontsize='small')

    return pl
