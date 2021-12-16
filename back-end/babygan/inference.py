
import pickle
import os
import os.path as osp
import numpy as np
#import dnnlib
#import dnnlib.tflib as tflib
from .dnnlib import *
from .dnnlib import tflib as tflib
from .encoder.generator_model import Generator
import math
from PIL import Image
import warnings
warnings.filterwarnings('ignore')

ROOT = "./"

age_direction = np.load(osp.join(ROOT, './ffhq_dataset/latent_directions/age.npy'))
# horizontal_direction = np.load(osp.join(ROOT, "./ffhq_dataset/latent_directions/angle_horizontal.npy"))
# vertical_direction = np.load(osp.join(ROOT, './ffhq_dataset/latent_directions/angle_vertical.npy'))
# eyes_open_direction = np.load(osp.join(ROOT, './ffhq_dataset/latent_directions/eyes_open.npy'))
# gender_direction = np.load(osp.join(ROOT, './ffhq_dataset/latent_directions/gender.npy'))
# smile_direction = np.load(osp.join(ROOT, './ffhq_dataset/latent_directions/smile.npy'))


def run_align_images():
    # run align_images.py with father and mother
    for p in ["father", "mother"]:
        # init file dir with ROOT path
        _python_file = osp.join(ROOT, "align_images.py") 
        _src = osp.join(ROOT, f"{p}_image")
        _dst = osp.join(ROOT, f"aligned_images")
        
        # run align_images.py with src(father, mother) dst(cropped father, mother)
        os.system(f"python {_python_file} {_src} {_dst}")

        # created img file
        _img = osp.join(_dst, f'{p}_01.png')
        # check if face exist
        if not os.path.isfile(_img):
           raise ValueError('No face was found or there is more than one in the photo.')


def run_encode_images():
    # init file dir with ROOT path
    _python_file = osp.join(ROOT, "encode_images.py") 
    _src = osp.join(ROOT, f"aligned_images")
    _dst = osp.join(ROOT, f"generated_images")
    _dla = osp.join(ROOT, f"latent_representations")

    # run encode_images.py
    os.system(f"python {_python_file} --early_stopping False --batch_size=2 --lr=0.25 --iterations=100 --output_video=False {_src} {_dst} {_dla}")


def generate_final_image(generator, latent_vector, direction, coeffs):
    new_latent_vector = latent_vector.copy()
    new_latent_vector[:8] = (latent_vector + coeffs*direction)[:8]
    new_latent_vector = new_latent_vector.reshape((1, 18, 512))
    generator.set_dlatents(new_latent_vector)
    img_array = generator.generate_images()[0]
    img = Image.fromarray(img_array, 'RGB')
    img.thumbnail(size, Image.ANTIALIAS)
    # img.save("face.png")
    # if download_image == True: files.download("face.png")
    return img

def main():
    # run align_images.py with mother and father images
    run_align_images()
    run_encode_images()

    tflib.init_tf()
    # generate latent vector
    with open(osp.join(ROOT, "karras2019stylegan-ffhq-1024x1024.pkl"), "rb") as f:
        generator_network, discriminator_network, Gs_network = pickle.load(f)
    generator = Generator(Gs_network, batch_size=1, randomize_noise=False)
    model_scale = int(2*(math.log(1024,2)-1))
    if len(os.listdir(osp.join(ROOT, 'generated_images'))) >= 2:
        first_face = np.load(osp.join(ROOT, 'latent_representations/father_01.npy'))
        second_face = np.load(osp.join(ROOT, 'latent_representations/mother_01.npy'))
        print("Generation of latent representation is complete! Now comes the fun part.")
    else: 
        raise ValueError('Something wrong. It may be impossible to read the face in the photos. Upload other photos and try again.')
    
    # gender : the closer to 0, the more influence the father's genotype will have. Closer to 1 - mother.
    genes_influence = 0.3
    style = "Default" #@param ["Default", "Father's photo", "Mother's photo"]
    if style == "Father's photo": 
        lr = ((np.arange(1,model_scale+1)/model_scale)**genes_influence).reshape((model_scale,1))
        rl = 1-lr
        hybrid_face = (lr*first_face) + (rl*second_face)
    elif style == "Mother's photo": 
        lr = ((np.arange(1,model_scale+1)/model_scale)**(1-genes_influence)).reshape((model_scale,1))
        rl = 1-lr
        hybrid_face = (rl*first_face) + (lr*second_face)
    else: 
        hybrid_face = ((1-genes_influence)*first_face)+(genes_influence*second_face)
    
    # Child's approximate age
    person_age = 10 # min:10, max:50, step:1
    intensity = -((person_age/5)-6)
    resolution = "512" # [256, 512, 1024]
    size = int(resolution), int(resolution)
    face = generate_final_image(generator, hybrid_face, age_direction, intensity)
    face.save(osp.join(ROOT, "final_image/final.png"))

if __name__ == "__main__":
    main()