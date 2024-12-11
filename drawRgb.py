import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import osmnx as ox
import prettymaps as pm
import argparse


def main(options):

    palette = ['#433633', '#FF5E5B']
    background_c = '#F2F4CB'
    dilate = 100

    cm = 1./2.54
    fig, ax = plt.subplots(figsize = (74*cm, 55*cm), constrained_layout = True)

    ox.config(use_cache=False,
          log_console=True,
          useful_tags_way=ox.settings.useful_tags_way + ['railway']
         )

    layers = pm.plot(
        '46.4464, 6.5314', radius = 100000,
        ax = ax,
        
        layers = {
            'perimeter': {'circle': False, 'dilate': dilate},
            'railway': {'width': {'rail': 4}, 'custom_filter': '["railway"~"subway|rail"]', 'circle': False, 'dilate': dilate},
            'streets': {
                'width': {
                    'motorway': 5,
                    'trunk': 5,
                    'primary': 4.5,
                    'secondary': 4,
                    'tertiary': 3.5,
                    'cycleway': 3.5,
                    'residential': 3,
                    'service': 2,
                    'unclassified': 2,
                    'pedestrian': 1,
                    'footway': 1,
                },
                'circle': False, 'dilate': dilate
            },
            'argiculture': {'tags': {'landuse': 'farmland'}, 'circle': False, 'union': True, 'dilate': dilate},
            'building': {'tags': {'building': True, 'landuse': 'construction'}, 'union': True, 'circle': False, 'dilate': dilate},
            'water': {'tags': {'natural': ['water', 'bay']}, 'circle': False, 'dilate': dilate},
            'forest': {'tags': {'landuse': 'forest'}, 'circle': False, 'dilate': dilate},
            'green': {'tags': {'landuse': ['grass', 'orchard'], 'natural': ['island', 'wood'], 'leisure': 'park'}, 'circle': False, 'dilate': dilate},
            'beach': {'tags': {'natural': 'beach'}, 'circle': False, 'dilate': dilate},
            'parking': {'tags': {'amenity': 'parking', 'highway': 'pedestrian', 'man_made': 'pier'}, 'circle': False}
        },
        drawing_kwargs = {
            'perimeter': {'fill': False, 'lw': 0, 'zorder': 0},
            'background': {'fc': background_c, 'zorder': -1},
            'green': {'fc': '#8BB174', 'ec': '#2F3737', 'hatch_c': '#A7C497', 'hatch': 'ooo...', 'lw': 1, 'zorder': 1},
            'forest': {'fc': '#64B96A', 'ec': '#2F3737', 'lw': 1, 'zorder': 2},
            'water': {'fc': '#a8e1e6', 'ec': '#2F3737', 'hatch_c': '#9bc3d4', 'hatch': 'ooo...', 'lw': 1, 'zorder': 3},
            'beach': {'fc': '#FCE19C', 'ec': '#2F3737', 'hatch_c': '#d4d196', 'hatch': 'ooo...', 'lw': 1, 'zorder': 3},
            'parking': {'fc': background_c, 'ec': '#2F3737', 'lw': 1, 'zorder': 3},
            'streets': {'fc': '#2F3737', 'ec': '#475657', 'alpha': 1, 'lw': 0, 'zorder': 4},
            'railway': {'fc': '#2F3737', 'ec': '#475657', 'alpha': 1, 'lw': 0, 'zorder': 5},
            'building': {'palette': ['#FFC857', '#E9724C', '#C5283D'], 'ec': '#2F3737', 'lw': .5, 'zorder': 3},
            'public_transport': {'fc': '#2B90E6', 'ec': '#2b90e6', 'lw': .5, 'zorder': 5},
            'argiculture' : {'palette': ['#89d689', '#D0F1BF'], 'ec': '#2F3737', 'lw': .5,  'zorder': 3} #'#F7EAB5'
        },
        osm_credit = {'text': 'data © OpenStreetMap contributors', 'x': .1, 'y': .86, 'color': '#2F3737'}
    )

    xmin, ymin, xmax, ymax = layers['perimeter'].bounds
    dx, dy = xmax-xmin, ymax-ymin
    bdX = .08
    bdY = .095
    a = 0.2
    ax.set_xlim(xmin+a*dx, xmax-a*dx)
    ax.set_ylim(ymin+a*dy, ymax-a*dy)

    ax.text(
        0.1, 0.87,
        'Le Leman',
        color='#2F3737',
        fontproperties=fm.FontProperties(fname='/home/thomas/Documents/Privat/prettymaps/prettymaps/assets/Permanent_Marker/PermanentMarker-Regular.ttf', size=60),
        transform=ax.transAxes
    )

    out = [ot.split('.')[0] for ot in options.out]
    exts = [ot.split('.')[-1] for ot in options.out]
    if 'all' in exts:
        oA = out[exts.index('all')]
        out.remove(oA)
        exts.remove('all')
        exts += ['png', 'pdf']
        out += [oA, oA]

    print(out, exts)
    for i, ext in enumerate(exts):
        fwidth, fheight = fig.get_size_inches()
        fig.savefig(out[i]+'_padded.'+ext, bbox_inches='tight', pad_inches=59.4*cm-fheight)
        fig.savefig(out[i]+'.'+ext)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', '-o', nargs='+', type=str, required=True)
    options = parser.parse_args()
    main(options)
