import matplotlib.pyplot as plt
import matplotlib.patches as patches

def digit_plotter(ax, num, colors):
#     ax.xaxis.set_major_locator(plt.NullLocator())
#     ax.yaxis.set_major_locator(plt.NullLocator())
    ax.axis('off')
    circle = patches.Circle((0.5, 0.5), 0.4, linewidth=0, \
                            edgecolor='black', facecolor=colors[(num-1) // 10])
    ax.add_artist(circle)
    if len(str(num)) == 1:
        ax.text(0.35, 0.4, str(num), color='w', fontsize=20, weight=True)
    else:
        ax.text(0.25, 0.4, str(num), color='w', fontsize=20, weight=True)
    return ax

def plus_plotter(ax):
#     ax.xaxis.set_major_locator(plt.NullLocator())
#     ax.yaxis.set_major_locator(plt.NullLocator())
    ax.axis('off')
    ax.text(0.35, 0.4, '+', color='k', fontsize=20, weight=True)
    return ax

def lotto_plotter(results):
    colors = ['y', 'c', 'r', 'm', 'g']
    
    fig, axes = plt.subplots(nrows=1, ncols=8, figsize=(9, 1.0))

    for idx, num in enumerate(results):
        if idx == 5:
            ax = axes[idx]
            digit_plotter(ax, num, colors)
            ax_plus = axes[idx+1]
            plus_plotter(ax_plus)
        elif idx == 6:
            ax = axes[idx+1]
            digit_plotter(ax, num, colors)
        else:
            ax = axes[idx]
            digit_plotter(ax, num, colors)
    plt.show()
            
def Main():
    results = [10, 32, 42, 37, 16, 22, 7]
    lotto_plotter(results)
    
if __name__ == '__main__':
    Main()