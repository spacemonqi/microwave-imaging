import os
import cv2
import math
import base64
from google.cloud import aiplatform
from google.cloud.aiplatform.gapic.schema import predict


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
    print(file_content)

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


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'key.json'
aiplatform.init(
    project        = 'abiogenesis',
    location       = 'us-central1',
    staging_bucket = 'gs://my_staging_bucket_abiogenesis',
    credentials    = 'key.json'
)

images_dir = '/home/dve/Desktop/microwave-imaging/images/highres/old'
files = os.listdir(images_dir)
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
    img            = cv2.imread(image)
    dimensions     = img.shape
    dim            = dimensions[0]
    bboxes         = result['bboxes']
    displayNames   = result['displayNames']
    mapping        = {
        'paper'  : (255, 0, 0),
        'plastic': (0, 255, 0),
        'metal'  : (0, 0, 255)
    }
    for bb, dn in zip(bboxes, displayNames):
        width  = bb[1] - bb[0]
        height = bb[3] - bb[2]
        tl     = (int(bb[0]*dim), int(bb[3]*dim))
        br     = (int(bb[1]*dim), int(bb[2]*dim))
        cv2.rectangle(
            img       = img,
            pt1       = tl,
            pt2       = br,
            color     = mapping[dn],
            thickness = math.ceil(4 * dim / scaling_factor)
        )
        font = cv2.FONT_HERSHEY_PLAIN
        cv2.putText(img, dn, br, font, 2, mapping[dn], 2, cv2.LINE_AA)

    cv2.namedWindow("resize", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("resize", scaling_factor, scaling_factor)
    cv2.imshow('resize', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    exit()
