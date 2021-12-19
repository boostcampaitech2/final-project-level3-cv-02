import os
import argparse
import pickle
from tqdm import tqdm
import PIL.Image
from PIL import ImageFilter
import numpy as np
#import .dnnlib
#import .dnnlib.tflib as tflib
from . import dnnlib
from .dnnlib import tflib as tflib 
from dotmap import DotMap
from . import config
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))
from encoder.generator_model import Generator
from encoder.perceptual_model import PerceptualModel, load_images
#from tensorflow.keras.models import load_model 
from keras.models import load_model
from keras.applications.resnet50 import preprocess_input

model_resnet = None

def split_to_batches(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def encode_images(u2id):
    ROOT = "./babygan/"
    #args, other_args = parser.parse_known_args()
    args = {
        'src_dir' : ROOT+f"{u2id}aligned",
        'mask_dir' : ROOT+f"{u2id}masks",
        'generated_images_dir': ROOT+f"{u2id}generated",
        'dlatent_dir' : ROOT+f"{u2id}latent_representations",
        'data_dir' : 'data',
        'load_last' : '',
        'dlatent_avg': '',
        'model_url' : 'karras2019stylegan-ffhq-1024x1024.pkl',
        'architecture' : 'vgg16_zhang_perceptual.pkl',
        'model_res':1024,
        'batch_size' : 1,
        'optimizer' : "ggt",
        'image_size' : 256,
        'resnet_image_size' : 256,
        'lr' : 0.5,
        'decay_rate' : 0.9,
        'iterations' : 200,
        'decay_steps' : 4 ,
        'early_stopping' : True,
        'early_stopping_threshold' : 0.5,
        'early_stopping_patience' : 10,
        'load_effnet': 'data/finetuned_resnet.h5',
        'load_resnet': 'data/finetuned_resnet.h5',
        'use_preprocess_input' : True, 
        'use_best_loss' : True,
        'average_best_loss' : 0.25,
        'sharpen_input' : True ,
        'use_vgg_loss' : 0.4 ,
        'use_vgg_layer' : 9 ,
        'use_pixel_loss' : 1.5,
        'use_mssim_loss' : 200 ,
        'use_lpips_loss' : 100,
        'use_l1_penalty' : 0.5,
        'use_discriminator_loss' : 0.5,
        'use_adaptive_loss' : False ,
        'randomize_noise' : False,
        'tile_dlatents': False,
        'clipping_threshold' : 2.0,
        'load_mask' : False,
        'face_mask' : True ,
        'use_grabcut' : True,
        'scale_mask' : 1.4,
        'composite_mask' : True,
        'composite_blur' : 8,
        'video_dir' : 'videos',
        'output_video' : False,
        'video_codec' : 'MJPG',
        'video_frame_rate' : 24,
        'video_size' : 512,
        'video_skip' : 1
    }
    
    args = DotMap(args)
    args.decay_steps *= 0.01 * args.iterations # Calculate steps as a percent of total iterations

    if args.output_video:
      import cv2
      synthesis_kwargs = dict(output_transform=dict(func=tflib.convert_images_to_uint8, nchw_to_nhwc=False), minibatch_size=args.batch_size)

    ref_images = [os.path.join(args.src_dir, x) for x in os.listdir(args.src_dir)]
    ref_images = list(filter(os.path.isfile, ref_images))

    if len(ref_images) == 0:
        raise Exception('%s is empty' % args.src_dir)

    os.makedirs(args.data_dir, exist_ok=True)
    os.makedirs(args.mask_dir, exist_ok=True)
    os.makedirs(args.generated_images_dir, exist_ok=True)
    os.makedirs(args.dlatent_dir, exist_ok=True)
    os.makedirs(args.video_dir, exist_ok=True)

    # Initialize generator and perceptual model
    tflib.init_tf()
    global model_resnet 
    if model_resnet == None:
        from keras.applications.resnet50 import preprocess_input
        print("Loading model resnet first time ")
        model_resnet = load_model("./data/finetuned_resnet.h5")
    with dnnlib.util.open_url(args.model_url, cache_dir=config.cache_dir) as f:
        generator_network, discriminator_network, Gs_network = pickle.load(f)

    generator = Generator(Gs_network, args.batch_size, clipping_threshold=args.clipping_threshold, tiled_dlatent=args.tile_dlatents, model_res=args.model_res, randomize_noise=args.randomize_noise)
    if (args.dlatent_avg != ''):
        generator.set_dlatent_avg(np.load(args.dlatent_avg))

    perc_model = None
    if (args.use_lpips_loss > 0.00000001):
        with dnnlib.util.open_url(args.architecture, cache_dir=config.cache_dir) as f:
            perc_model =  pickle.load(f)
    perceptual_model = PerceptualModel(args, perc_model=perc_model, batch_size=args.batch_size)
    perceptual_model.build_perceptual_model(generator, discriminator_network)

    ff_model = None
    #ff_model = model_resnet

    # Optimize (only) dlatents by minimizing perceptual loss between reference and generated images in feature space
    for images_batch in tqdm(split_to_batches(ref_images, args.batch_size), total=len(ref_images)//args.batch_size):
        names = [os.path.splitext(os.path.basename(x))[0] for x in images_batch]
        if args.output_video:
          video_out = {}
          for name in names:
            video_out[name] = cv2.VideoWriter(os.path.join(args.video_dir, f'{name}.avi'),cv2.VideoWriter_fourcc(*args.video_codec), args.video_frame_rate, (args.video_size,args.video_size))

        perceptual_model.set_reference_images(images_batch)
        dlatents = None
        if (args.load_last != ''): # load previous dlatents for initialization
            for name in names:
                dl = np.expand_dims(np.load(os.path.join(args.load_last, f'{name}.npy')),axis=0)
                if (dlatents is None):
                    dlatents = dl
                else:
                    dlatents = np.vstack((dlatents,dl))
        else:
            if (ff_model is None):
                if os.path.exists(args.load_resnet):
                    from keras.applications.resnet50 import preprocess_input
                    print("Loading ResNet Model:")
                    #ff_model = load_model(args.load_resnet)
                    ff_model = model_resnet
                    print("Finish ")
            if (ff_model is None):
                if os.path.exists(args.load_effnet):
                    import efficientnet
                    #from efficientnet import preprocess_input
                    print("Loading EfficientNet Model:")
                    ff_model = load_model(args.load_effnet)
            if (ff_model is not None): # predict initial dlatents with ResNet model
                if (args.use_preprocess_input):
                    #tf.initialize_all_variables().run()
                    #tf.global_variables_initializer().run()
                    dlatents = ff_model.predict(preprocess_input(load_images(images_batch,image_size=args.resnet_image_size)))
                else:
                    dlatents = ff_model.predict(load_images(images_batch,image_size=args.resnet_image_size))
        if dlatents is not None:
            generator.set_dlatents(dlatents)
        op = perceptual_model.optimize(generator.dlatent_variable, iterations=args.iterations, use_optimizer=args.optimizer)
        pbar = tqdm(op, leave=False, total=args.iterations)
        vid_count = 0
        best_loss = None
        best_dlatent = None
        avg_loss_count = 0
        if args.early_stopping:
            avg_loss = prev_loss = None
        for loss_dict in pbar:
            if args.early_stopping: # early stopping feature
                if prev_loss is not None:
                    if avg_loss is not None:
                        avg_loss = 0.5 * avg_loss + (prev_loss - loss_dict["loss"])
                        if avg_loss < args.early_stopping_threshold: # count while under threshold; else reset
                            avg_loss_count += 1
                        else:
                            avg_loss_count = 0
                        if avg_loss_count > args.early_stopping_patience: # stop once threshold is reached
                            print("")
                            break
                    else:
                        avg_loss = prev_loss - loss_dict["loss"]
            pbar.set_description(" ".join(names) + ": " + "; ".join(["{} {:.4f}".format(k, v) for k, v in loss_dict.items()]))
            if best_loss is None or loss_dict["loss"] < best_loss:
                if best_dlatent is None or args.average_best_loss <= 0.00000001:
                    best_dlatent = generator.get_dlatents()
                else:
                    best_dlatent = 0.25 * best_dlatent + 0.75 * generator.get_dlatents()
                if args.use_best_loss:
                    generator.set_dlatents(best_dlatent)
                best_loss = loss_dict["loss"]
            if args.output_video and (vid_count % args.video_skip == 0):
              batch_frames = generator.generate_images()
              for i, name in enumerate(names):
                video_frame = PIL.Image.fromarray(batch_frames[i], 'RGB').resize((args.video_size,args.video_size),PIL.Image.LANCZOS)
                video_out[name].write(cv2.cvtColor(np.array(video_frame).astype('uint8'), cv2.COLOR_RGB2BGR))
            generator.stochastic_clip_dlatents()
            prev_loss = loss_dict["loss"]
        if not args.use_best_loss:
            best_loss = prev_loss
        print(" ".join(names), " Loss {:.4f}".format(best_loss))

        if args.output_video:
            for name in names:
                video_out[name].release()

        # Generate images from found dlatents and save them
        if args.use_best_loss:
            generator.set_dlatents(best_dlatent)
        generated_images = generator.generate_images()
        generated_dlatents = generator.get_dlatents()
        for img_array, dlatent, img_path, img_name in zip(generated_images, generated_dlatents, images_batch, names):
            mask_img = None
            if args.composite_mask and (args.load_mask or args.face_mask):
                _, im_name = os.path.split(img_path)
                mask_img = os.path.join(args.mask_dir, f'{im_name}')
            if args.composite_mask and mask_img is not None and os.path.isfile(mask_img):
                orig_img = PIL.Image.open(img_path).convert('RGB')
                width, height = orig_img.size
                imask = PIL.Image.open(mask_img).convert('L').resize((width, height))
                imask = imask.filter(ImageFilter.GaussianBlur(args.composite_blur))
                mask = np.array(imask)/255
                mask = np.expand_dims(mask,axis=-1)
                img_array = mask*np.array(img_array) + (1.0-mask)*np.array(orig_img)
                img_array = img_array.astype(np.uint8)
                #img_array = np.where(mask, np.array(img_array), orig_img)
            img = PIL.Image.fromarray(img_array, 'RGB')
            img.save(os.path.join(args.generated_images_dir, f'{img_name}.png'), 'PNG')
            np.save(os.path.join(args.dlatent_dir, f'{img_name}.npy'), dlatent)

        generator.reset_dlatents()


if __name__ == "__main__":
    main()
