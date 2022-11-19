import {useState} from "react";
import * as PropTypes from "prop-types";
import {ImageLoader} from "./ImageLoader";
import {ImageDisplay} from "./ImageDisplay";



function ImageScreen() {
    const [image, setImage] = useState(undefined)
    const [coordinates, setCoordinates] = useState([])


    return (
        <div className="bg-background-color h-screen">
            <ImageLoader image={image} setImage={setImage} setCoordinates={setCoordinates}/>
            <ImageDisplay image={image} coordinates={coordinates}/>
            <h1> There's nothing here yet! GO AWAY IM WORKING</h1>
        </div>
    )
}

export default ImageScreen