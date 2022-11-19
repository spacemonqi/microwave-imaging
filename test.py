import os
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from google.cloud import aiplatform
from predict_image_object_detection_sample import predict_image_object_detection_sample

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'key.json'

aiplatform.init(
    project        = 'abiogenesis',
    location       = 'us-central1',
    staging_bucket = 'gs://my_staging_bucket_abiogenesis',
    credentials    = 'key.json'
)

image = "images/20221119-115341-596.png"

result = predict_image_object_detection_sample(
    project     = "44054203076",
    endpoint_id = "6030922433421115392",
    location    = "us-central1",
    filename    = image
)

im = Image.open(image)

# Create figure and axes
fig, ax = plt.subplots()

# Display the image
ax.imshow(im)

bboxes       = result['bboxes']
displayNames = result['displayNames']
mapping = {
    'paper'  : 'magenta',
    'plastic': 'coral',
    'metal'  : 'red'
}

for bb, dn in zip(bboxes, displayNames):
    x      = (bb[0] + bb[1])/2
    y      = (bb[2] + bb[3])/2
    width  = abs(bb[1]) - abs(bb[0])
    height = abs(bb[3]) - abs(bb[2])
    rect   = patches.Rectangle((x, y), width, height, linewidth=1, edgecolor=mapping[dn], facecolor='none')

    # Add the patch to the Axes
    ax.add_patch(rect)

plt.show()