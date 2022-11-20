import * as PropTypes from "prop-types";
import {useEffect, useRef, useState} from "react";
const {BigQuery} = require('@google-cloud/bigquery');


const ENDPOINT_ID = "6030922433421115392"
const PROJECT_ID = "abiogenesis"
export const FETCH_CLASSIFICATION = `https://us-central1-aiplatform.googleapis.com/v1/projects/${PROJECT_ID}/locations/us-central1/endpoints/${ENDPOINT_ID}:predict`

const options = {
    keyFilename: 'path/to/service_account.json',
    projectId: PROJECT_ID,
};

const bigquery = new BigQuery(options);

export function ImageLoader({image, setImage, setCoordinates}) {
    const [base64String, setBase64String] = useState()
    const fileInput = useRef(null)

    useEffect(() => {
        const data = {
            "instances": [{
                "content": base64String
            }],
            "parameters": {
                "confidenceThreshold": 0.5,
                "maxPredictions": 5
            }
        }
        fetch(FETCH_CLASSIFICATION, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        })
            .then(response => {
                if (response.ok) {
                    return response.json()
                }
                throw response;
            })
            .then(data => {
                setCoordinates(data)
            })
            .catch(error => {
                console.error("Error fetching image details: ", error)
            })
    }, [base64String, setCoordinates])


    const handleSubmit = (event) => {
        event.preventDefault()
        const file = fileInput.current.files[0]
        const reader = new FileReader()
        reader.onload = (e) => {
            setImage(e.target.result)
            setBase64String(reader.result.replace("data:", "").replace(/^.+,/, ""))
        }
        reader.readAsDataURL(file)
    }

    return (
        <>
            <div className="card relative">
                {!image && <form onSubmit={handleSubmit} className="h-full w-full">
                    <div className="h-full w-full relative">
                        <div className="h-full w-full flex justify-center items-center absolute font-title italic">
                            Click to upload image
                        </div>
                        <label className="absolute h-full w-full" htmlFor="image_upload">
                            <input type="file" accept="image/png" ref={fileInput}
                                   id="image_upload" name="image_upload"
                                   className="h-full w-full bg-primary-color opacity-0"/>
                        </label>
                    </div>
                    <br/>
                    <button type="submit" className="bg-primary-color">Submit</button>
                </form>}
                {image && <img src={image} alt="uploaded, preferably a cross-section from the microwave scanner"/>}
            </div>
        </>
    )
}

ImageLoader.propTypes = {
    setImage: PropTypes.func,
    image: PropTypes.any,
    setCoordinates: PropTypes.func
};
