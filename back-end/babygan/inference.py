import pickle
import os
import os.path as osp
import shutil 
import numpy as np

from .dnnlib import *
from .dnnlib import tflib as tflib

from .ffhq_dataset.face_alignment import image_align
from .ffhq_dataset.landmarks_detector import LandmarksDetector

from .encoder.generator_model import Generator
import math
from PIL import Image
import warnings
import requests

warnings.filterwarnings('ignore')

ROOT = "./babygan"
age_direction = np.load(osp.join(ROOT, 'ffhq_dataset/latent_directions/age.npy'))
# horizontal_direction = np.load(osp.join(ROOT, "./ffhq_dataset/latent_directions/angle_horizontal.npy"))
# vertical_direction = np.load(osp.join(ROOT, './ffhq_dataset/latent_directions/angle_vertical.npy'))
# eyes_open_direction = np.load(osp.join(ROOT, './ffhq_dataset/latent_directions/eyes_open.npy'))
# gender_direction = np.load(osp.join(ROOT, './ffhq_dataset/latent_directions/gender.npy'))
# smile_direction = np.load(osp.join(ROOT, './ffhq_dataset/latent_directions/smile.npy'))


def run_align_images(f,m,u2id,P_ROOT):
    # run align_images.py with father and mother
    
    os.makedirs(P_ROOT+"father",exist_ok=True)
    os.makedirs(P_ROOT+"mother",exist_ok=True)
    os.system("curl "+ f + f"> {P_ROOT}father/father.png")
    os.system("curl "+ m + f"> {P_ROOT}mother/mother.png")

    for p in [[P_ROOT+"mother","mother"],[P_ROOT+"father","father"]] :
        # init file dir with ROOT path
        _python_file = osp.join(ROOT, "align_images.py") 
        _src = p[0]
        _dst = osp.join(ROOT, f"{u2id}aligned")
        # run align_images.py with src(father, mother) dst(cropped father, mother)
        os.system(f"python {_python_file} {_src} {_dst}")
        # created img file
        _img = osp.join(_dst,f'{p[1]}_01.png') 
        # check if face exist
        if not os.path.isfile(_img):  
           raise ValueError('No face was found or there is more than one in the photo.')


def run_encode_images(u2id):
    # init file dir with ROOT path 
    _python_file = osp.join(ROOT, "encode_images.py") 
    _src = osp.join(ROOT, f"{u2id}aligned")
    _dst = osp.join(ROOT, f"{u2id}generated")
    _dla = osp.join(ROOT, f"{u2id}latent_representations")
    _mask_dir = osp.join(ROOT, f"{u2id}masks")
    # run encode_images.py
    os.system(f"python {_python_file} --mask_dir {_mask_dir} --early_stopping True --batch_size=2 --lr=0.5 --iterations=200 --output_video=False {_src} {_dst} {_dla}")


def generate_final_image(generator, latent_vector, direction, coeffs, size):
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

def do_inference(f,m, u2id): 
    # run align_images.py with mother and father images
    P_ROOT = ROOT + "/" +u2id 
    print(P_ROOT)
    run_align_images(f,m,u2id,P_ROOT)
    run_encode_images(u2id) 

    tflib.init_tf()
    # generate latent vector
    with open(osp.join(ROOT, "karras2019stylegan-ffhq-1024x1024.pkl"), "rb") as f:
        generator_network, discriminator_network, Gs_network = pickle.load(f)
    generator = Generator(Gs_network, batch_size=1, randomize_noise=True) # 1
    model_scale = int(2*(math.log(1024,2)-1))
    if len(os.listdir(osp.join(ROOT, f'{u2id}generated'))) >= 2:
        #first_face = np.load(osp.join(ROOT, 'latent_representations/father_01.npy'))
        #second_face = np.load(osp.join(ROOT, 'latent_representations/mother_01.npy'))
        first_face = np.load(osp.join(ROOT, f'{u2id}latent_representations/father_01.npy'))
        second_face = np.load(osp.join(ROOT, f'{u2id}latent_representations/mother_01.npy'))
        print("Generation of latent representation is complete! Now comes the fun part.")
    else: 
        raise ValueError('Something wrong. It may be impossible to read the face in the photos. Upload other photos and try again.')
    
    # gender : the closer to 0, the more influence the father's genotype will have. Closer to 1 - mother.
    genes_influence = 0.3 # 0.3
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
    person_age = 20 # min:10, max:50, step:1
    intensity = -((person_age/5)-6) 
    resolution = "512" # [256, 512, 1024]
    size = int(resolution), int(resolution)
    face= []
    for i in np.arange(-4,5,0.5):
        face.append(generate_final_image(generator, hybrid_face, age_direction, i, size))

    os.makedirs(ROOT+f"/{u2id}final_image", exist_ok = True)

    for i in range(len(face)): 
        face[i].save(osp.join(ROOT, f"{u2id}final_image/final{i}.png"))

    for fold in ["mother","father","generated","latent_representations","aligned","masks"]:
        print("del : " , P_ROOT+fold)
        shutil.rmtree(P_ROOT+fold)
    shutil.rmtree('./videos')
    return ROOT+f"/{u2id}final_image/final14.png"
