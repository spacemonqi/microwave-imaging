import math
import os
import cv2
import time
from PIL import Image
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from google.cloud import aiplatform
from predict_image_object_detection_sample import predict_image_object_detection_sample
# mpl.use('TkAgg')


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'key.json'

aiplatform.init(
    project        = 'abiogenesis',
    location       = 'us-central1',
    staging_bucket = 'gs://my_staging_bucket_abiogenesis',
    credentials    = 'key.json'
)

# image = "images/20221119-115341-596.png"
images_dir = '/home/dve/Desktop/microwave-imaging/images/highres/old'
files = os.listdir(images_dir)
# image = "images_new/20221119-115455-700.png"
for f, file in zip(range(len(files)), files):
    if f%10!=0:
        continue
    print(file)

    image = f'{images_dir}/{file}'
    result = predict_image_object_detection_sample(
        project     = "44054203076",
        endpoint_id = "6030922433421115392",
        location    = "us-central1",
        filename    = image
    )

    scaling_factor = 1024
    img = cv2.imread(image)
    dimensions = img.shape
    dim = dimensions[0]
    print(dimensions)
    bboxes       = result['bboxes']
    displayNames = result['displayNames']
    mapping = {
        # 'paper'  : (255, 0, 0),
        # 'plastic': (0, 255, 0),
        # 'metal'  : (0, 0, 255)
        'paper'  : (255, 0, 0),
        'plastic': (0, 255, 0),
        'metal'  : (0, 0, 255)
    }
    # cv2.rectangle(img, (100, 560), (700, 480),
    #               (0, 0, 255), 3)
    # cv2.rectangle(img, (650, 450), (420, 240),
    #               (255, 0, 0), 5)

    for bb, dn in zip(bboxes, displayNames):
        # x      = (bb[0] + bb[1])/2
        # y      = (bb[2] + bb[3])/2
        # width  = abs(bb[1]) - abs(bb[0])
        # height = abs(bb[3]) - abs(bb[2])
        tl     = (int(bb[0]*dim), int(bb[3]*dim))
        br     = (int(bb[1]*dim), int(bb[2]*dim))
        print(tl)
        print(type(tl))
        cv2.rectangle(
            img       = img,
            # pt1       = (150, 50),
            pt1       = tl,
            # pt2       = (380, 40),
            pt2       = br,
            color     = mapping[dn],
            thickness = math.ceil(4 * dim / scaling_factor)
        )

    cv2.namedWindow("resize", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("resize", scaling_factor, scaling_factor)
    cv2.imshow('resize', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
