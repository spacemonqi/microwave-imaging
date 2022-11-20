import {useState} from "react";
import {ImageLoader} from "./ImageLoader";
import {ImageDisplay} from "./ImageDisplay";


function ImageScreen() {
    const [image, setImage] = useState(undefined)
    const [coordinates, setCoordinates] = useState([])

    return (
        <div className="flex justify-center items-center bg-background-color">
            <div className="bg-background-color h-screen grid grid-cols-1 lg:grid-cols-2 place-items-center lg:w-1/2">
                <ImageLoader image={image} setImage={setImage} setCoordinates={setCoordinates}/>
                <ImageDisplay image={image} coordinates={coordinates}/>
            </div>
        </div>
    )
}

export default ImageScreen