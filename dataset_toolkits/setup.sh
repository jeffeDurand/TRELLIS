pip install pillow==10 \
    "numpy<2" \
    "bpy>=4" \
    torch \
    torchvision \
    torchaudio \
    imageio \
    google-cloud-storage \
    rembg[gpu] \
    imageio-ffmpeg \
    tqdm \
    easydict \
    opencv-python-headless \
    scipy \
    ninja \
    objaverse \
    huggingface_hub \
    trimesh \
    open3d \
    xatlas \
    tensorboard \
    pandas \
    lpips \
    pyvista \
    pymeshfix \
    igraph \
    xformers==0.0.27.post2 \
    spconv-cu126 \
    transformers==4.46.3 \
    gradio_litmodel3d==0.0.1
pip install https://github.com/Dao-AILab/flash-attention/releases/download/v2.7.0.post2/flash_attn-2.7.0.post2+cu12torch2.4cxx11abiFALSE-cp311-cp311-linux_x86_64.whl \
    git+https://github.com/autonomousvision/mip-splatting.git#subdirectory=submodules/diff-gaussian-rasterization \
    git+https://github.com/NVlabs/nvdiffrast.git \
    git+https://github.com/EasternJournalist/utils3d.git#egg=utils3d
CC="cc -mavx2" pip install -U --force-reinstall pillow-simd
pip install kaolin==0.17.0 -f https://nvidia-kaolin.s3.us-east-2.amazonaws.com/torch-2.4.0_cu124.html
