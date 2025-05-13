import torch
from safetensors.torch import save_file
import json
import os
# Load the config
config_path = "/home/ubuntu/TRELLIS/configs/vae/slat_vae_dec_mesh_swin8_B_64l8_fp16.json"
with open(config_path, 'r') as f:
    config = json.load(f)
# Load the EMA checkpoint
ckpt_path = "/home/ubuntu/TRELLIS/test_data/1dot5k-models/ckpts/decoder_ema0.9999_step1000000.pt"
state_dict = torch.load(ckpt_path, map_location='cpu', weights_only=True)
# Save as safetensors
output_path = "/home/ubuntu/TRELLIS/test_data/1dot5k-models/ckpts/slat_dec_mesh_swin8_B_64l8m256c_fp16.safetensors"
save_file(state_dict, output_path)
# The config.json should already exist, but if you need to create it:
config_output = {
    "name": "SLatMeshDecoder",  # or whatever your decoder class name is
    "args": config['models']['decoder']['args']
}
with open("test_data/1dot5k-models/ckpts/slat_dec_mesh_swin8_B_64l8m256c_fp16.json", 'w') as f:
    json.dump(config_output, f, indent=4)