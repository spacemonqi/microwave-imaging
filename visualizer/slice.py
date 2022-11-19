# Import data
import os
import time
import json
import math
import nibabel
import numpy as np
from skimage import io
import plotly.graph_objects as go
from matplotlib import pyplot as plt


def import_volume(file_path):
    """Import 3D volumetric data from file.

    Args:
        file_path (basestring): Absolute path for .img, .hdr or .json file.

    Returns:
        The volume definition given as the coordinate vectors in x, y, and z-direction.
    """

    path, filename = os.path.split(file_path)
    filename = os.path.splitext(filename)[0]

    file_path_img = os.path.join(path, f"{filename}.img")
    file_path_hdr = os.path.join(path, f"{filename}.hdr")
    file_path_json = os.path.join(path, f"{filename}.json")

    if not os.path.exists(file_path_img):
        raise Exception(f"Does not exist file: {file_path_img}")
    if not os.path.exists(file_path_hdr):
        raise Exception(f"Does not exist file: {file_path_hdr}")
    if not os.path.exists(file_path_json):
        raise Exception(f"Does not exist file: {file_path_json}")

    v_mag_phase = nibabel.load(file_path_hdr)
    _volume = v_mag_phase.dataobj[:, :, : v_mag_phase.shape[2] // 2] * np.exp(
        1j * v_mag_phase.dataobj[:, :, v_mag_phase.shape[2] // 2 :]
    )
    if len(_volume.shape) > 3:
        _volume = np.squeeze(_volume)

    with open(file_path_json, "rb") as vol_definition_file:
        def_json = json.load(vol_definition_file)
        _x_vec = def_json["origin"]["x"] + np.arange(def_json["dimensions"]["x"]) * def_json["spacing"]["x"]
        _y_vec = def_json["origin"]["y"] + np.arange(def_json["dimensions"]["y"]) * def_json["spacing"]["y"]
        _z_vec = def_json["origin"]["z"] + np.arange(def_json["dimensions"]["z"]) * def_json["spacing"]["z"]

        return _volume, _x_vec, _y_vec, _z_vec


vol = io.imread("https://s3.amazonaws.com/assets.datacamp.com/blog_assets/attention-mri.tif")
volume = vol.T
r, c, nb_frames = vol.shape


vol_ = import_volume('/home/dve/Desktop/microwave-imaging/images/layered/20221119-135731-220_reco.img')
vol_ = vol_[0]
volume_ = vol_.T
r_, c_, nb_frames_ = vol_.shape

volume = volume_
r = r_
c = c_
nb_frames = nb_frames_

fig = go.Figure(frames=[go.Frame(data=go.Surface(
    z=(6.7 - k * 0.1) * np.ones((r, c)),
    surfacecolor=np.flipud(volume[67 - k]),
    cmin=0, cmax=200
    ),
    name=str(k) # you need to name the frame for the animation to behave properly
    )
    for k in range(nb_frames)])

# Add data to be displayed before animation starts
fig.add_trace(go.Surface(
    z=6.7 * np.ones((r, c)),
    surfacecolor=np.flipud(volume[67]),
    colorscale='Gray',
    cmin=0, cmax=200,
    colorbar=dict(thickness=20, ticklen=4)
    ))


def frame_args(duration):
    return {
            "frame": {"duration": duration},
            "mode": "immediate",
            "fromcurrent": True,
            "transition": {"duration": duration, "easing": "linear"},
        }

sliders = [
            {
                "pad": {"b": 10, "t": 60},
                "len": 0.9,
                "x": 0.1,
                "y": 0,
                "steps": [
                    {
                        "args": [[f.name], frame_args(0)],
                        "label": str(k),
                        "method": "animate",
                    }
                    for k, f in enumerate(fig.frames)
                ],
            }
        ]

# Layout
fig.update_layout(
         title='Slices in volumetric data',
         width=600,
         height=600,
         scene=dict(
                    zaxis=dict(range=[-0.1, 6.8], autorange=False),
                    aspectratio=dict(x=1, y=1, z=1),
                    ),
         updatemenus = [
            {
                "buttons": [
                    {
                        "args": [None, frame_args(50)],
                        "label": "&#9654;", # play symbol
                        "method": "animate",
                    },
                    {
                        "args": [[None], frame_args(0)],
                        "label": "&#9724;", # pause symbol
                        "method": "animate",
                    },
                ],
                "direction": "left",
                "pad": {"r": 10, "t": 70},
                "type": "buttons",
                "x": 0.1,
                "y": 0,
            }
         ],
         sliders=sliders
)

fig.show()