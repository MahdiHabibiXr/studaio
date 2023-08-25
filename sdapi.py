from PIL import Image, PngImagePlugin
import time
import base64, io, requests, json
import os
from datetime import datetime, date
import time
# from plugins import url

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        base64_string = encoded_string.decode("utf-8")
    return base64_string

def save_encoded_image(b64_image, output_path):
    # Check if file exists, create if it doesn't exist
    if not os.path.exists(output_path):
        open(output_path, 'wb').close()

    # Open file in binary mode     
    with open(output_path, 'wb') as f:
        f.write(base64.b64decode(b64_image))
        f.flush()
        f.close()


def generate_image(prompt, image_input= '',negative_prompt = 'NSFW, no face, invisible face', batch_size = 1, enable_roop = True, output_folder = 'outputdata/', enable_upscale = False, step = 25):
    # negative_prompt = 'NSFW, no face, invisible face'
    # negative_prompt = 'Watermark, Text, censored, deformed, bad anatomy, disfigured, poorly drawn face, mutated, extra limb, ugly, poorly drawn hands, missing limb, floating limbs, disconnected limbs, disconnected head, malformed hands, long neck, mutated hands and fingers, bad hands, missing fingers, cropped, worst quality, low quality, mutation, poorly drawn, huge calf, bad hands, fused hand, missing hand, disappearing arms, disappearing thigh, disappearing calf, disappearing legs, missing fingers, fused fingers, abnormal eye proportion, Abnormal hands, abnormal legs, abnormal feet,  abnormal fingers'
    steps = step

    file_input = image_input                             # the face to swap
    filefolderpath = output_folder

    # # convert input and reference files to base64
    if(enable_roop):
        file_input_base64 = image_to_base64(file_input)

    # Roop arguments:
    if(enable_roop):
        args = [
            file_input_base64,                                                      #0 File Input
            enable_roop,                                                                   #1 Enable Roop
            '0',                                                                    #2 Comma separated face number(s)
            'C:/StableDiffusion/models/roop/inswapper_128.onnx',    #3 Model
            'CodeFormer',                                                           #4 Restore Face: None; CodeFormer; GFPGAN
            1,                                                                      #5 Restore visibility value
            True,                                                                   #6 Restore face -> Upscale
            'None',                                                                 #7 Upscaler (type 'None' if doesn't need), see full list here: http://127.0.0.1:7860/sdapi/v1/script-info -> roop-ge -> sec.8
            1,                                                                      #8 Upscaler scale value
            1,                                                                      #9 Upscaler visibility (if scale = 1)
            True,                                                                  #10 Swap in source image
            False,                                                                   #11 Swap in generated image
        ]
    else : args = []

    payload = {
        "enable_hr": enable_upscale,
        "denoising_strength": 0.7,
        # "firstphase_width": 0,
        # "firstphase_height": 0,
        "hr_scale": 1.5,
        "hr_upscaler": "Latent",
        # "hr_second_pass_steps": 0,
        # "hr_resize_x": 0,
        # "hr_resize_y": 0,
        # "hr_sampler_name": "Euler a",
        # "restore_faces": True ,
        "prompt": prompt,
        "negative_prompt" : negative_prompt,
        "steps": steps,
        "width": 512,
        "height": 512,
        "batch_size": batch_size, # How many images generated each time
        "sampler_index" : 'Euler a',
        "seed" : -1 ,
        "cfg_scale": 7,
        "override_settings": {"sd_model_checkpoint": "realisticVisionV51_v51VAE.safetensors",},
        "alwayson_scripts": {"roop": {"is_alwayson": enable_roop, "args": args}}
        # "styles": [
        #     "Digital Painting",
        #     "Default_Negative"
        # ]
    }

    url = 'http://127.0.0.1:7923'
    resp = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)
    r = resp.json()

    images = []
    counter = batch_size
    for i in r['images']:
        image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))

        time = datetime.now()
        today = date.today()
        current_date = today.strftime('%Y-%m-%d')
        current_time = time.strftime('%H-%M-%S')

        file_output = filefolderpath + 'output_' + current_date + '_' + current_time + str(counter) +'_.png'
        print(f'saving {file_output}')

        image.save(file_output)
        images.append(file_output)

        counter = counter - 1
        # png_payload = {
        #     "image": "data:image/png;base64," + i
        # }
        # response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)

        # pnginfo = PngImagePlugin.PngInfo()
        # pnginfo.add_text("parameters", response2.json().get("info"))

    return(images)





# payloads = {
#     "enable_hr": false,
#     "denoising_strength": 0,
#     "firstphase_width": 0,
#     "firstphase_height": 0,
#     "hr_scale": 2,
#     "hr_upscaler": "string",
#     "hr_second_pass_steps": 0,
#     "hr_resize_x": 0,
#     "hr_resize_y": 0,
#     "hr_sampler_name": "string",
#     "hr_prompt": "",
#     "hr_negative_prompt": "",
#     "prompt": "",
#     "styles": [
#         "string"
#     ],
#     "seed": -1,
#     "subseed": -1,
#     "subseed_strength": 0,
#     "seed_resize_from_h": -1,
#     "seed_resize_from_w": -1,
#     "sampler_name": "string",
#     "batch_size": 1,
#     "n_iter": 1,
#     "steps": 50,
#     "cfg_scale": 7,
#     "width": 512,
#     "height": 512,
#     "restore_faces": false,
#     "tiling": false,
#     "do_not_save_samples": false,
#     "do_not_save_grid": false,
#     "negative_prompt": "string",
#     "eta": 0,
#     "s_min_uncond": 0,
#     "s_churn": 0,
#     "s_tmax": 0,
#     "s_tmin": 0,
#     "s_noise": 1,
#     "override_settings": {},
#     "override_settings_restore_afterwards": true,
#     "script_args": [],
#     "sampler_index": "Euler",
#     "script_name": "string",
#     "send_images": true,
#     "save_images": false,
#     "alwayson_scripts": {}
# }

