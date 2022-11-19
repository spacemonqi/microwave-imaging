# Import data
import os
import nibabel
import numpy as np
import plotly.graph_objects as go


def import_volume(file_path):
    """Import 3D volumetric data from file.

    Args:
        file_path (basestring): Absolute path for .img, .hdr or .json file.

    Returns:
        The volume definition given as the coordinate vectors in x, y, and z-direction.
    """

    path, filename = os.path.split(file_path)
    filename       = os.path.splitext(filename)[0]

    file_path_img  = os.path.join(path, f"{filename}.img")
    file_path_hdr  = os.path.join(path, f"{filename}.hdr")
    file_path_json = os.path.join(path, f"{filename}.json")

    if not os.path.exists(file_path_img):
        raise Exception(f"Does not exist file: {file_path_img}")
    if not os.path.exists(file_path_hdr):
        raise Exception(f"Does not exist file: {file_path_hdr}")
    if not os.path.exists(file_path_json):
        raise Exception(f"Does not exist file: {file_path_json}")

    v_mag_phase = nibabel.load(file_path_hdr)
    _volume     = v_mag_phase.dataobj[:, :, : v_mag_phase.shape[2] // 2] * np.exp(
        1j * v_mag_phase.dataobj[:, :, v_mag_phase.shape[2] // 2 :]
    )
    if len(_volume.shape) > 3:
        _volume = np.squeeze(_volume)

    return _volume


vol     = import_volume('/home/dve/Desktop/microwave-imaging/images/layered/20221119-141049-198_reco.img')
vol     = np.abs(vol)
vol    /= vol.max()
vol    *= 380
vol    -= 20
volume  = vol.T
c, r, nb_frames = vol.shape
dim = nb_frames - 1
plot_dim = 10 / 10  # dim / 10

fig = go.Figure(frames=[go.Frame(
    data=go.Surface(
        z            = (plot_dim - k * 1/dim) * np.ones((r, c)),
        surfacecolor = np.flipud(volume[dim - k]),
        cmin         = 0,
        cmax         = 200
    ),
    name = str(k) # you need to name the frame for the animation to behave properly
) for k in range(nb_frames)])

# Add data to be displayed before animation starts
fig.add_trace(go.Surface(
    z            = plot_dim * np.ones((r, c)),
    surfacecolor = np.flipud(volume[dim]),
    colorscale   = 'viridis',
    cmin         = 0,
    cmax         = 200,
    colorbar     = dict(thickness=20, ticklen=4)
))


def frame_args(duration):
    return {
            "frame"      : {"duration": duration},
            "mode"       : "immediate",
            "fromcurrent": True,
            "transition" : {"duration": duration, "easing": "linear"},
        }

sliders = [
            {
                "pad"  : {"b": 10, "t": 60},
                "len"  : 0.9,
                "x"    : 0.1,
                "y"    : 0,
                "steps": [
                    {
                        "args"  : [[f.name], frame_args(0)],
                        "label" : str(k),
                        "method": "animate",
                    } for k, f in enumerate(fig.frames)
                ],
            }
        ]

# Layout
fig.update_layout(
         title  = 'Slices in volumetric data',
         width  = 900,
         height = 900,
         scene  = dict(
            zaxis       = dict(
                range     = [-0.1, plot_dim+0.1],
                autorange = False
            ),
            aspectratio = dict(
                x = 1,
                y = 1,
                z = 0.75
            ),
        ),
         updatemenus = [
            {
                "buttons": [
                    {
                        "args"  : [None, frame_args(50)],
                        "label" : "&#9654;",              # play symbol
                        "method": "animate",
                    },
                    {
                        "args"  : [[None], frame_args(0)],
                        "label" : "&#9724;",               # pause symbol
                        "method": "animate",
                    },
                ],
                "direction": "left",
                "pad"      : {"r": 10, "t": 70},
                "type"     : "buttons",
                "x"        : 0.1,
                "y"        : 0,
            }
         ],
         sliders = sliders
)

fig.show()