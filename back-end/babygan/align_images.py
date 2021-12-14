import os
import sys
import bz2
import argparse
from keras.utils import get_file


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))
from ffhq_dataset.face_alignment import image_align
from ffhq_dataset.landmarks_detector import LandmarksDetector
import multiprocessing


def unpack_bz2(src_path):
    data = bz2.BZ2File(src_path).read()
    dst_path = src_path[:-4]
    with open(dst_path, 'wb') as fp:
        fp.write(data)
    return dst_path


if __name__ == "__main__":
    """
    Extracts and aligns all faces from images using DLib and a function from original FFHQ dataset preparation step
    python align_images.py /raw_images /aligned_images
    """
    parser = argparse.ArgumentParser(description='Align faces from input images', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('raw_dir', help='Directory with raw images for face alignment')
    parser.add_argument('aligned_dir', help='Directory for storing aligned images')
    parser.add_argument('--output_size', default=1024, help='The dimension of images for input to the model', type=int)
    parser.add_argument('--x_scale', default=1, help='Scaling factor for x dimension', type=float)
    parser.add_argument('--y_scale', default=1, help='Scaling factor for y dimension', type=float)
    parser.add_argument('--em_scale', default=0.1, help='Scaling factor for eye-mouth distance', type=float)
    parser.add_argument('--use_alpha', default=False, help='Add an alpha channel for masking', type=bool)

    args, other_args = parser.parse_known_args()

    landmarks_model_path = unpack_bz2("./babygan/shape_predictor_68_face_landmarks.dat.bz2")
    RAW_IMAGES_DIR = args.raw_dir 
    ALIGNED_IMAGES_DIR = args.aligned_dir 
    url = RAW_IMAGES_DIR 
    #os.system("curl " + url + "> ./babygan/hi.jpg")  #이게 맞아?,,.
    #RAW_IMAGES_DIR2 = "./babygan/hyundong"
    landmarks_detector = LandmarksDetector(landmarks_model_path)
    for img_name in os.listdir(RAW_IMAGES_DIR): 
    #for img_name in RAW_IMAGES_DIR: 
        print('Aligning %s ...' % img_name)
        try:
            raw_img_path = os.path.join(RAW_IMAGES_DIR, img_name) 
            print(raw_img_path , "#"*100)
            fn = face_img_name = '%s_%02d.png' % (os.path.splitext(img_name)[0], 1) #<< 여기서 오류인가본디 아 이제 아내얼굴이 없다.
            print(fn , "#"*100)
            if os.path.isfile(fn):
                continue
            print('Getting landmarks...') 
            for i, face_landmarks in enumerate(landmarks_detector.get_landmarks(raw_img_path), start=1):
                try:
                    print('Starting face alignment...')
                    face_img_name = '%s_%02d.png' % (os.path.splitext(img_name)[0], i)
                    aligned_face_path = os.path.join(ALIGNED_IMAGES_DIR, face_img_name)
                    image_align(raw_img_path, aligned_face_path, face_landmarks, output_size=args.output_size, x_scale=args.x_scale, y_scale=args.y_scale, em_scale=args.em_scale, alpha=args.use_alpha)
                    print('Wrote result %s' % aligned_face_path)
                except:
                    print("Exception in face alignment!")
        except:
            print("Exception in landmark detection!")
