import * as PropTypes from "prop-types";

export function ImageDisplay({coordinates, image}) {
    return (
        <div className="card relative">
            {image && <img src={image} alt="uploaded, preferably a cross-section from the microwave scanner"/>}
        </div>
    )
}

ImageDisplay.propTypes = {
    image: PropTypes.any,
    coordinates: PropTypes.arrayOf(PropTypes.any)
};
