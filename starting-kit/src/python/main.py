"""
HackaTUM 2022 - Rohde & Schwarz
"""

import os
import json
import math
import nibabel
import numpy as np
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


def compute_slice(_volume, _z_idx=0):
    """Compute a single slice of the given 3D volumetric data in z-direction.

    Args:
        _volume: 3D volumetric data.
        _z_idx: Index on z-direction.

    Returns:
        A single slice (img) of the given 3D volumetric data in z-direction.
    """

    img = _volume[:, :, _z_idx]
    return img


def compute_mip(_volume):
    """Compute the maximum intensity projection (MIP) of a 3D volume.

    Args:
        _volume (ndarray): 3D volumetric data.

    Returns:
        The MIP of the 3D volume (v_max) and the estimated maximum indices in z-direction (k_max).
    """

    k_max = np.argmax(np.abs(_volume), axis=2)
    i, j = np.indices(k_max.shape)
    v_max = _volume[i, j, k_max]

    return v_max, k_max


def complex2magphase(data):
    """Computes the magnitude and the phase of each data.

    Args:
         data: Any complex data (a + bi).

    Returns:
        Computes the magnitude (mag) and the phase (phi) for each element of the complex data.
    """

    mag = np.abs(data)
    phi = np.angle(data)

    return mag, phi


def compute_fft(img):
    """Compute the 2D FFT of an image.

    Args:
        img (ndarray): 2D array.

    Returns:
        2D FFT of the image in x and y-direction.
    """

    fft_img = np.fft.fftshift(np.fft.fft2(img), axes=(0, 1))
    return fft_img


def display(
    img,
    color_map=plt.get_cmap("viridis"),
    img_title=None,
    cmap_label=None,
    alphadata=None,
    xvec=None,
    yvec=None,
    dynamic_range=None,
    clim=None,
    xlabel=None,
    ylabel=None,
):
    """Helper function to display data as an image, i.e., on a 2D regular raster.

    Args:
        img: 2D array.
        color_map: The Colormap instance or registered colormap name to map scalar data to colors.
        img_title: Text to use for the title.
        cmap_label: Set the label for the x-axis.
        alphadata: The alpha blending value, between 0 (transparent) and 1 (opaque).
        xvec: coordinate vectors in x.
        yvec: coordinate vectors in y.
        dynamic_range: The dynamic range that the colormap will cover.
        clim: Set the color limits of the current image.
    """

    max_image = np.max(img)
    if dynamic_range is None:
        imshow_args = {}
    else:
        imshow_args = {"vmin": max_image - dynamic_range, "vmax": max_image}

    if xvec is None or yvec is None:
        plt.imshow(img, cmap=color_map, alpha=alphadata, origin="lower", **imshow_args)
    else:
        plt.imshow(
            img,
            cmap=color_map,
            alpha=alphadata,
            extent=[xvec[0], xvec[-1], yvec[0], yvec[-1]],
            origin="lower",
            **imshow_args,
        )

    if clim is not None:
        plt.clim(clim)

    if img_title is not None:
        plt.title(img_title)

    if xlabel is not None:
        plt.xlabel(xlabel)

    if ylabel is not None:
        plt.ylabel(ylabel)

    cbar = plt.colorbar()
    cbar.ax.set_ylabel(cmap_label)
    plt.show()


if __name__ == "__main__":
    C0 = 299792458
    FC = 77e9
    LAMBDA = C0 / FC

    Z_IDX = 13

    volume, x_vec, y_vec, z_vec = import_volume(
        r"../../volumes/example-1.img"
    )

    Nx = x_vec.size
    Ny = y_vec.size

    kx = (np.arange(-Nx / 2, Nx / 2 - 1)) / ((Nx - 1) * np.diff(x_vec[:2]))
    ky = (np.arange(-Ny / 2, Ny / 2 - 1)) / ((Ny - 1) * np.diff(y_vec[:2]))

    kx_n = kx * LAMBDA
    ky_n = ky * LAMBDA

    volume_max, kmax = compute_mip(volume)
    volume_max_range = (np.min(np.abs(volume_max)), np.max(np.abs(volume_max)))
    alpha_data = np.clip(
        1.8 * ((np.abs(volume_max) - volume_max_range[0]) / (volume_max_range[1] - volume_max_range[0])) - 0.25, 0, 1,
    )

    # 1 --> visualize magnitude of the MIP
    image = 20 * np.log10(np.abs(volume_max / np.max(volume_max)))
    display(
        image,
        img_title="Maximum intensity projection (MIP)",
        cmap_label="Normalized magnitude in dB",
        xvec=x_vec,
        yvec=y_vec,
        dynamic_range=30,
        xlabel="$x$ in m",
        ylabel="$y$ in m",
    )

    # 2 --> visualize phase of the MIP (opacity scaled by alpha_data)
    _, volume_max_phase = complex2magphase(
        np.multiply(volume_max, np.exp(((1j * 2 * math.pi) / LAMBDA) * 2 * z_vec[kmax]))
    )
    display(
        180 / math.pi * volume_max_phase,
        color_map=plt.get_cmap("twilight"),
        img_title="MIP Phase",
        cmap_label="Phase in degree",
        alphadata=alpha_data,
        xvec=x_vec,
        yvec=y_vec,
        xlabel="$x$ in m",
        ylabel="$y$ in m",
    )

    # 3 --> visualize the phase of a selected slice (opacity scaled by alpha_data)
    _, V_slice_phase = complex2magphase(volume[:, :, Z_IDX - 1])
    display(
        180 / math.pi * V_slice_phase,
        color_map=plt.get_cmap("twilight"),
        img_title=f"Single slice phase (z = {z_vec[Z_IDX - 1]:.4f} m)",
        cmap_label="Phase in degree",
        alphadata=alpha_data,
        xvec=x_vec,
        yvec=y_vec,
        xlabel="$x$ in m",
        ylabel="$y$ in m",
    )

    # 4 --> visualize the distance of the MIP (opacity scaled by alpha_data)
    display(
        z_vec[kmax],
        img_title="MIP Distance",
        cmap_label="Distance in m",
        alphadata=alpha_data,
        xvec=x_vec,
        yvec=y_vec,
        clim=(0.15, 0.28),
        xlabel="$x$ in m",
        ylabel="$y$ in m",
    )

    # 5 --> visualize the 2D FFT of the MIP
    S_MIP = compute_fft(volume_max)
    S_MIP_mag_dB = 20 * np.log10(np.abs(S_MIP))
    display(
        S_MIP_mag_dB,
        img_title="MIP 2D FFT",
        dynamic_range=35,
        xvec=kx_n,
        yvec=ky_n,
        xlabel="$k_x$ in $2\\pi \\,/\\, \\lambda$",
        ylabel="$k_y$ in $2\\pi \\,/\\, \\lambda$",
    )

    # 6 --> visualize the 2D FFT of a single slice
    S_slice = compute_fft(volume[:, :, Z_IDX - 1])
    S_slice_mag_dB = 20 * np.log10(np.abs(S_slice))
    display(
        S_slice_mag_dB,
        img_title=f"Single slice 2D FFT (z = {z_vec[Z_IDX - 1]:.4f} m)",
        dynamic_range=35,
        xvec=kx_n,
        yvec=ky_n,
        xlabel="$k_x$ in $2\\pi \\,/\\, \\lambda$",
        ylabel="$k_y$ in $2\\pi \\,/\\, \\lambda$",
    )
