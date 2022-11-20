import json
import os
import uuid
import csv
import sys
import base64
import pathlib
import nibabel
import numpy as np

import boto3
import dash
import dash_core_components as dcc
import dash_html_components as html
import requests
from dash.dependencies import Input, Output, State
from flask_caching import Cache

import dash_reusable_components as drc
import utils
import os
import cv2
import math
import plotly.graph_objects as go

import base64
from google.cloud import aiplatform
from google.cloud.aiplatform.gapic.schema import predict

IMAGEDIR = '/home/dve/Desktop/microwave-imaging/data/'


def set_fig():
    with open('tempfile.txt', 'r') as f:
        filename = f.read()
    filepath  = (IMAGEDIR + filename).replace('.png', '_reco.img')
    vol       = import_volume(filepath)
    vol       = np.abs(vol)
    vol      /= vol.max()
    vol      *= 380
    vol      -= 20
    volume    = vol.T
    c, r, nb_frames = vol.shape
    dim = nb_frames - 1
    plot_dim = 10 / 10  # dim / 10

    fig = go.Figure(
        frames=[go.Frame(
            data=go.Surface(
                z            = (plot_dim - k * 1/dim) * np.ones((r, c)),
                surfacecolor = np.flipud(volume[dim - k]),
                cmin         = 0,
                cmax         = 200
            ),
            name = str(k) # you need to name the frame for the animation to behave properly
        ) for k in range(nb_frames)],
        # layout = {
        #     'plot_bgcolor' : 'rgb(230, 230, 255)',
        #     'paper_bgcolor': 'rgb(230, 230, 255)',
        # }
    )

    # Add data to be displayed before animation starts
    fig.add_trace(go.Surface(
        z            = (plot_dim+5) * np.ones((r, c)),
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
            title        = 'Microwave Imaging Slices',
            font=dict(
                family = "Major Mono Display",
                size   = 18,
            ),
            width        = 1200,
            height       = 1200,
            scene        = dict(
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

    return fig



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




with open('tempfile.txt', 'r') as f:
    filename = f.read()
filepath = (IMAGEDIR + filename).replace('.png', '_reco.img')
vol = import_volume(filepath)
vol     = np.abs(vol)
vol    /= vol.max()
vol    *= 380
vol    -= 20
volume  = vol.T
c, r, nb_frames = vol.shape
dim = nb_frames - 1
plot_dim = 10 / 10  # dim / 10

fig = go.Figure(
    frames=[go.Frame(
        data=go.Surface(
            z            = (plot_dim - k * 1/dim) * np.ones((r, c)),
            surfacecolor = np.flipud(volume[dim - k]),
            cmin         = 0,
            cmax         = 200
        ),
        name = str(k) # you need to name the frame for the animation to behave properly
    ) for k in range(nb_frames)],
    # layout = {
    #     'plot_bgcolor' : 'rgb(230, 230, 255)',
    #     'paper_bgcolor': 'rgb(230, 230, 255)',
    # }
)

# Add data to be displayed before animation starts
fig.add_trace(go.Surface(
    z            = (plot_dim+5) * np.ones((r, c)),
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
        title        = 'Microwave Imaging Slices',
        font=dict(
            family = "Major Mono Display",
            size   = 18,
        ),
        width        = 1200,
        height       = 1200,
        scene        = dict(
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


def predict_image_object_detection_sample(
    project: str,
    endpoint_id: str,
    filename: str,
    location: str = "us-central1",
    api_endpoint: str = "us-central1-aiplatform.googleapis.com",
):
    # The AI Platform services require regional API endpoints.
    client_options = {"api_endpoint": api_endpoint}
    # Initialize client that will be used to create and send requests.
    # This client only needs to be created once, and can be reused for multiple requests.
    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)
    with open(filename, "rb") as f:
        file_content = f.read()

    # The format of each instance should conform to the deployed model's prediction input schema.
    encoded_content = base64.b64encode(file_content).decode("utf-8")
    instance = predict.instance.ImageObjectDetectionPredictionInstance(
        content=encoded_content,
    ).to_value()
    instances = [instance]
    # See gs://google-cloud-aiplatform/schema/predict/params/image_object_detection_1.0.0.yaml for the format of the parameters.
    parameters = predict.params.ImageObjectDetectionPredictionParams(
        confidence_threshold=0.5, max_predictions=5,
    ).to_value()
    endpoint = client.endpoint_path(
        project=project, location=location, endpoint=endpoint_id
    )
    response = client.predict(
        endpoint=endpoint, instances=instances, parameters=parameters
    )
    print("response")
    print(" deployed_model_id:", response.deployed_model_id)
    # See gs://google-cloud-aiplatform/schema/predict/prediction/image_object_detection_1.0.0.yaml for the format of the predictions.
    predictions = response.predictions
    for prediction in predictions:
        print(" prediction:", dict(prediction))

    return prediction


def predict_image(image):
    result = predict_image_object_detection_sample(
        project     = "44054203076",
        endpoint_id = "6030922433421115392",
        location    = "us-central1",
        filename    = image
    )

    scaling_factor = 1024
    img            = cv2.imread(image)
    dimensions     = img.shape
    dim            = dimensions[0]
    bboxes         = result['bboxes']
    displayNames   = result['displayNames']
    mapping        = {
        'paper'  : (255, 255, 0),
        'plastic': (0, 165, 255),
        'metal'  : (0, 0, 255)
    }
    for bb, dn in zip(bboxes, displayNames):
        tl     = (int(bb[0]*dim), int(bb[3]*dim))
        br     = (int(bb[1]*dim), int(bb[2]*dim))
        width  = (br[0] - tl[0])
        cv2.rectangle(
            img       = img,
            pt1       = tl,
            pt2       = br,
            color     = mapping[dn],
            thickness = math.ceil(4 * dim / scaling_factor)
        )
        font = cv2.FONT_HERSHEY_PLAIN
        cv2.putText(img, dn, (br[0]-width, br[1]-10), font, 2, mapping[dn], 2, cv2.LINE_AA)

    out_image = image.replace('.', '-bboxed.')
    cv2.imwrite(out_image, img)

    return out_image



DEBUG = True
LOCAL = False
APP_PATH = str(pathlib.Path(__file__).parent.resolve())

app = dash.Dash(__name__)
app.title = "Image Processing App"
server = app.server

if "BUCKET_NAME" in os.environ:
    # Change caching to redis if hosted on dds
    cache_config = {
        "CACHE_TYPE": "redis",
        "CACHE_REDIS_URL": os.environ["REDIS_URL"],
        "CACHE_THRESHOLD": 400,
    }
# Local Conditions
else:
    LOCAL = True
    # Caching with filesystem when served locally
    cache_config = {
        "CACHE_TYPE": "filesystem",
        "CACHE_DIR": os.path.join(APP_PATH, "data"),
    }

# S3 Client. It is used to store user images. The bucket name
# is stored inside the utils file, the key is
# the session id generated by uuid

access_key_id = os.environ.get("ACCESS_KEY_ID")
secret_access_key = os.environ.get("SECRET_ACCESS_KEY")
bucket_name = os.environ.get("BUCKET_NAME")

# Empty cache directory before running the app
folder = os.path.join(APP_PATH, "data")
for the_file in os.listdir(folder):
    file_path = os.path.join(folder, the_file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(e)

# If local, image data is stored locally in image_string.csv
if LOCAL:
    f = open("image_string.csv", "w+")
    f.close()

    # Store images are very long strings, so allowed csv
    # reading length is increased to its maximum allowed value
    maxInt = sys.maxsize
    while True:
        # decrease the maxInt value by factor 10
        # as long as the OverflowError occurs.
        try:
            csv.field_size_limit(maxInt)
            break
        except OverflowError:
            maxInt = int(maxInt / 10)

if not LOCAL:
    s3 = boto3.client(
        "s3",
        endpoint_url="https://storage.googleapis.com",
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
    )

# Caching
cache = Cache()
cache.init_app(app.server, config=cache_config)


# Store key value value (session_id, stringed_image)
def store_image_string(string_image, key_name):
    if DEBUG:
        print(key_name)
    # If local, the string is stored in image_string.csv
    if LOCAL:
        with open("image_string.csv", mode="w+") as image_file:
            image_writer = csv.DictWriter(image_file, fieldnames=["key", "image"])
            image_writer.writeheader()
            image_writer.writerow(dict(key=key_name, image=string_image))
    # Generate the POST attributes
    else:
        post = s3.generate_presigned_post(Bucket=bucket_name, Key=key_name)

        files = {"file": string_image}
        # Post the string file using requests
        requests.post(post["url"], data=post["fields"], files=files)


def serve_layout():
    # Generates a session ID
    session_id = str(uuid.uuid4())

    # Post the image to the right key, inside the bucket named after the
    # session ID
    store_image_string(utils.IMAGE_STRING_PLACEHOLDER, session_id)

    # App Layout
    return html.Div(
        id="root",
        children=[
            # Session ID
            html.Div(session_id, id="session-id"),
            # Main body
            html.Div(
                id="app-container",
                children=[
                    # Banner display
                    html.Div(
                        id="banner",
                        children=[
                            html.Img(
                                id="logo", src=app.get_asset_url("abiogenesis.png"), style={'height':'8%', 'width':'80%'}
                            )
                            # html.H1("ABIOGENESIS", id="title"),
                        ],
                        # style={'width': '90vh', 'height': '40vh'}
                    ),
                    html.Div([
                        dcc.Graph(id="graph", figure=fig),
                    ])
                ],
            ),
            # Sidebar
            html.Div(
                id="sidebar",
                children=[
                    drc.Card(
                        [
                            dcc.Upload(
                                id="upload-image",
                                children=[
                                    "Drag and Drop or ",
                                    html.A(children="Select an Image"),
                                ],
                                # No CSS alternative here
                                style={
                                    "color"        : "darkgray",
                                    "width"        : "100%",
                                    "height"       : "50px",
                                    "lineHeight"   : "50px",
                                    "borderWidth"  : "1px",
                                    "borderStyle"  : "dashed",
                                    "borderRadius" : "5px",
                                    "bdorderColor"  : "darkgray",
                                    "textAlign"    : "center",
                                    "padding"      : "2rem 0",
                                    "margin-bottom": "2rem",
                                },
                                accept="image/*",
                            ),
                        ]
                    ),
                    drc.Card(
                        [
                            html.Div(
                                id="button-group",
                                children=[
                                    html.Button(
                                        "Run Detection", id = "button-run-operation"
                                    ),
                                    html.Button("Undo", id="button-undo"),
                                ],
                            ),
                        ]
                    ),
                    # dcc.Graph(
                    #     id="graph-histogram-colors",
                    #     figure={
                    #         "layout": {
                    #             "paper_bgcolor": "#272a31",
                    #             "plot_bgcolor" : "#272a31",
                    #         }
                    #     },
                    #     config={"displayModeBar": False},
                    # ),
                    html.Div(
                        id="image",
                        children=[
                            # The Interactive Image Div contains the dcc Graph
                            # showing the image, as well as the hidden div storing
                            # the true image
                            html.Div(
                                id="div-interactive-image",
                                children=[
                                    utils.GRAPH_PLACEHOLDER,
                                    html.Div(
                                        id="div-storage",
                                        children=utils.STORAGE_PLACEHOLDER,
                                    ),
                                ],
                            )
                        ],
                    ),
                ],
            ),
        ],
    )


app.layout = serve_layout


# Helper functions for callbacks
def add_action_to_stack(action_stack, operation, operation_type, selectedData):
    """
    Add new action to the action stack, in-place.
    :param action_stack: The stack of action that are applied to an image
    :param operation: The operation that is applied to the image
    :param operation_type: The type of the operation, which could be a filter,
    an enhancement, etc.
    :param selectedData: The JSON object that contains the zone selected by
    the user in which the operation is applied
    :return: None, appending is done in place
    """

    new_action = {
        "operation": operation,
        "type": operation_type,
        "selectedData": selectedData,
    }

    action_stack.append(new_action)


def undo_last_action(n_clicks, storage):
    action_stack = storage["action_stack"]

    if n_clicks is None:
        storage["undo_click_count"] = 0

    # If the stack isn't empty and the undo click count has changed
    elif len(action_stack) > 0 and n_clicks > storage["undo_click_count"]:
        # Remove the last action on the stack
        action_stack.pop()

        # Update the undo click count
        storage["undo_click_count"] = n_clicks

    return storage




# @app.callback(
#     [Input("button-undo", "n-clicks")]
# )
# def update_histogram(clicks):
#     print('aaaaaa')
    # Retrieve the image stored inside the figure
    # enc_str = figure["layout"]["images"][0]["source"].split(";base64,")[-1]
    # Creates the PIL Image object from the b64 png encoding
    # im_pil = drc.b64_to_pil(string=enc_str)

    # return utils.show_histogram(im_pil)



# @app.callback(
#     Output("graph-histogram-colors", "figure"), [Input("interactive-image", "figure")]
# )
# def update_histogram(figure):
#     # Retrieve the image stored inside the figure
#     enc_str = figure["layout"]["images"][0]["source"].split(";base64,")[-1]
#     # Creates the PIL Image object from the b64 png encoding
#     im_pil = drc.b64_to_pil(string=enc_str)

#     return utils.show_histogram(im_pil)


# @app.callback(
#     # [
#     #     Output("div-interactive-image", "children"),
#     # ],
#     # [
#     [Input("button-run-operation", "n_clicks")],
#     # ],
#     # [
#     #     # State("interactive-image", "selectedData"),
#     #     State("upload-image", "filename"),
#     #     State("div-storage", "children"),
#     # ],
#     prevent_initial_call=True
# )
# def update_bbox_interactive_image(
#     # content,
#     # undo_clicks,
#     n_clicks,
#     # fig,
#     # selectedData,
#     # filters,
#     # enhance,
#     # enhancement_factor,
#     # filename,
#     # storage,
#     # session_id,
# ):
#     print('aaaaaaaaaaaaaaaaaaaaaaaaaa')
#     pass
#     # storage = json.loads(storage)
#     # filepath = IMAGEDIR + filename
#     # print(f'\nPredicting {filepath}\n')
#     # new_filepath = predict_image(filepath)
#     # with open(new_filepath, "rb") as image_file:
#     #     encoded_string = base64.b64encode(image_file.read()).decode()
#     # print(encoded_string[:100])
#     # im_pil = drc.b64_to_pil(encoded_string)
    
#     # return [
#     #     drc.InteractiveImagePIL(
#     #         image_id   = "interactive-image",
#     #         image      = im_pil,
#     #         verbose    = DEBUG,
#     #     ),
#     #     html.Div(
#     #         id="div-storage", children=json.dumps(storage), style={"display": "none"}
#     #     ),
#     # ]


@app.callback(
    [
        Output("div-interactive-image", "children"),
        Output("graph", "figure")
    ],
    [
        Input("upload-image", "contents"),
        # Input("button-undo", "n_clicks"),
        Input("button-run-operation", "n_clicks"),
        Input("graph", "figure")
    ],
    [
        State("interactive-image", "selectedData"),
        # State("dropdown-filters", "value"),
        # State("dropdown-enhance", "value"),
        # State("slider-enhancement-factor", "value"),
        State("upload-image", "filename"),
        State("div-storage", "children"),
        State("session-id", "children"),
    ],
)
def update_graph_interactive_image(
    content,
    # undo_clicks,
    n_clicks,
    fig,
    selectedData,
    # filters,
    # enhance,
    # enhancement_factor,
    new_filename,
    storage,
    session_id,
):

    # Retrieve information saved in storage, which is a dict containing
    # information about the image and its action stack
    storage = json.loads(storage)
    filename = storage["filename"]  # Filename is the name of the image file.
    image_signature = storage["image_signature"]

    # # Runs the undo function if the undo button was clicked. Storage stays
    # # the same otherwise.
    # storage = undo_last_action(undo_clicks, storage)

    # If a new file was uploaded (new file name changed)
    if new_filename and new_filename != filename:

        # Update the storage dict
        storage["filename"] = new_filename

        # Parse the string and convert to pil
        print(f'\nShowing {new_filename}\n')
        string = content.split(";base64,")[-1]
        print(string[:100])
        with open('tempfile.txt', 'w') as f:
            f.write(new_filename)
        im_pil = drc.b64_to_pil(string)

        # Update the image signature, which is the first 200 b64 characters of the string encoding
        storage["image_signature"] = string[:200]

        # Resets the action stack
        storage["action_stack"] = []


        # print('json')
        # print(fig_json.keys())
        fig = set_fig()


    # If an operation was applied (when the filename wasn't changed)
    else:
        filepath = IMAGEDIR + filename
        print(f'\nPredicting {filepath}\n')
        new_filepath = predict_image(filepath)
        with open(new_filepath, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        print(encoded_string[:100])
        im_pil = drc.b64_to_pil(encoded_string)
        fig = None

    return [
        drc.InteractiveImagePIL(
            image_id   = "interactive-image",
            image      = im_pil,
            verbose    = DEBUG,
        ),
        html.Div(
            id="div-storage", children=json.dumps(storage), style={"display": "none"}
        ),
    ], fig






# @app.callback(
#     Output("div-interactive-image", "figure"),
#     [Input("button-run-operation", "n-clicks")],
#     [
#      State("upload-image", "filename"),
#      State("div-storage", "children"),
#      State("session-id", "children")
#     ],
#     prevent_initial_call=True
# )
# def update_bboxes(
#     clicks,
#     filename,
#     storage,
#     session_id
# ):
#     print(filename)
#     filepath = IMAGEDIR + filename
#     print(f'\nPredicting {filepath}\n')
#     new_filepath = predict_image(filepath)
#     with open(new_filepath, "rb") as image_file:
#         encoded_string = base64.b64encode(image_file.read()).decode()
#     print(encoded_string[:100])
#     im_pil = drc.b64_to_pil(encoded_string)

#     return [
#         drc.InteractiveImagePIL(
#             image_id   = "interactive-image",
#             image      = im_pil,
#             verbose    = DEBUG,
#         ),
#         html.Div(
#             id="div-storage", children=json.dumps(storage), style={"display": "none"}
#         ),
#     ]



# Running the server
if __name__ == "__main__":
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'key.json'
    aiplatform.init(
        project        = 'abiogenesis',
        location       = 'us-central1',
        staging_bucket = 'gs://my_staging_bucket_abiogenesis',
        credentials    = 'key.json'
    )
    app.run_server(debug=False)