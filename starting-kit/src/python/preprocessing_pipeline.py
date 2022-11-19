import pathlib
import time
import pickle

import preprocessing_functions

def pipeline():
    root = pathlib.Path('C:\\Users\\Алексей\\Documents\\Crypto\\HackaTUM\\microwave-imaging\\data\\corrupted')
    target_folder = pathlib.Path('C:\\Users\\Алексей\\Documents\\Crypto\\HackaTUM\\microwave-imaging\\data\\processed_corrupted')

    pickle_path = pathlib.Path('test_files/preprocessed.pkl')
    # if pickle_path.exists():
    #     with open(pickle_path, 'rb') as f:
    #         filtered_images, image_names = pickle.load(f)

    filtered_images = []
    image_names = []
    for img_folder in root.iterdir() :
        if img_folder.is_dir():
            processed = process_raw_image(img_folder)
            filtered_images.append(processed[0])
            image_names.append(processed[1])

    with open(pickle_path, 'wb') as f:
        pickle.dump([filtered_images, image_names], f)

    reduced_images = preprocessing_functions.reduce_dimensionality(filtered_images)

    for img, name in zip(reduced_images, image_names):
        preprocessing_functions.layer_to_png(
            img,
            target_folder / f"{name}.png"
        )



# def filter_images():

def process_raw_image(img_folder):
    image = preprocessing_functions.import_volume(
        img_folder / f"{img_folder.stem}_reco.img"
    )
    img_filtered = preprocessing_functions.filter_noise(image)
    return img_filtered, img_folder.stem

if __name__ == '__main__':
    start_time = time.time()
    pipeline()
    print('pipeline took', time.time() - start_time)
    # process_raw_image(
    #     pathlib.Path(
    #         'C:/Users/Алексей/Documents/Crypto/HackaTUM/microwave-imaging/team-3/20221119-114924-969/20221119-114924-969_reco.img'
    #     )
    # )