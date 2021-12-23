import os
import sys
import bz2
import argparse
from keras.utils import get_file

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__)))
)
from ffhq_dataset.face_alignment import image_align
from ffhq_dataset.landmarks_detector import LandmarksDetector
import multiprocessing
from dotmap import DotMap

def unpack_bz2(src_path):
    data = bz2.BZ2File(src_path).read()
    dst_path = src_path[:-4]
    with open(dst_path, "wb") as fp:
        fp.write(data)
    return dst_path


#if __name__ == "__main__":
def align_images(raw_dir, aligned_dir, ):
    """
    Extracts and aligns all faces from images using DLib and a function from original FFHQ dataset preparation step
    python align_images.py /raw_images /aligned_images
    """
    args = { 
        "raw_dir" : raw_dir,
        "aligned_dir" : aligned_dir,
        "output_size" : 1024,
        "x_scale" : 1,
        "y_scale" : 1,
        "em_scale": 0.1,
        "use_alpha": False
    }
    args = DotMap(args)

    landmarks_model_path = unpack_bz2(
        "./babygan/shape_predictor_68_face_landmarks.dat.bz2"
    )
    RAW_IMAGES_DIR = args.raw_dir
    ALIGNED_IMAGES_DIR = args.aligned_dir
    print(ALIGNED_IMAGES_DIR)
    os.makedirs(ALIGNED_IMAGES_DIR, exist_ok=True)
    url = RAW_IMAGES_DIR

    landmarks_detector = LandmarksDetector(landmarks_model_path)
    for img_name in os.listdir(RAW_IMAGES_DIR):
        print("Aligning %s ..." % img_name)
        try:
            raw_img_path = os.path.join(RAW_IMAGES_DIR, img_name)
            fn = face_img_name = "%s_%02d.png" % (
                os.path.splitext(img_name)[0],
                1,
            )
            if os.path.isfile(fn):
                continue
            print("Getting landmarks...")
            for i, face_landmarks in enumerate(
                landmarks_detector.get_landmarks(raw_img_path),
                start=1,
            ):
                try:
                    print("Starting face alignment...")
                    face_img_name = "%s_%02d.png" % (
                        os.path.splitext(img_name)[0],
                        i,
                    )
                    aligned_face_path = os.path.join(
                        ALIGNED_IMAGES_DIR, face_img_name
                    )
                    image_align(
                        raw_img_path,
                        aligned_face_path,
                        face_landmarks,
                        output_size=args.output_size,
                        x_scale=args.x_scale,
                        y_scale=args.y_scale,
                        em_scale=args.em_scale,
                        alpha=args.use_alpha,
                    )
                    print("Wrote result %s" % aligned_face_path)
                except:
                    print("Exception in face alignment!")
        except:
            print("Exception in landmark detection!")
