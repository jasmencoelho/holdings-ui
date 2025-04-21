import os
import matplotlib.pyplot as plt

# Color mapping for layers
layer_colors = {
    'd': 'green',
    'c': 'yellow',
    'e': 'red'
}

def save_plot(gdf, region_code, tag, basemap_gdf, out_dir):
    import os
    import matplotlib.pyplot as plt

    os.makedirs(out_dir, exist_ok=True)
    filename = f"{region_code}_{tag}.png"
    filepath = os.path.join(out_dir, filename)

    fig, ax = plt.subplots(figsize=(6, 6))

    # Plot base country polygon
    basemap_gdf.plot(ax=ax, color='beige', edgecolor='lightgray', linewidth=1)

    # Plot data layer
    layer_colors = {'d': 'green', 'c': 'yellow', 'e': 'red'}
    gdf.plot(ax=ax, color=layer_colors.get(tag, 'black'), edgecolor='black', linewidth=0.5, alpha=0.7)

    # Lock map extent and aspect
    xmin, ymin, xmax, ymax = basemap_gdf.total_bounds
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_aspect('equal')
    ax.axis('off')

    plt.tight_layout()
    plt.savefig(filepath, bbox_inches='tight', dpi=150)
    plt.close()

    return filepath