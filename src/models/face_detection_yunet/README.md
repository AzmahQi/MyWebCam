# YuNet (face_detection_yunet)

YuNet is a lightweight, fast and accurate face detector used in OpenCV Zoo.
This folder contains a small demo and a wrapper that use the YuNet model.

Notes
- Model files (ONNX) are tracked by Git LFS in the original repo. The placeholder .onnx files in this directory are LFS pointer files. Use `git lfs pull` in this repo (or download the model files manually) to fetch the actual binaries.
- License: MIT (see LICENSE file)

Python demo

Run the demo (camera):

```bash
python demo.py
```

Run on an image:

```bash
python demo.py --input /path/to/image.jpg -v
```

Default model file
- `face_detection_yunet_2023mar.onnx` (default)
- `face_detection_yunet_2023mar_int8bq.onnx` (quantized)

If you need the real ONNX model files, either run `git lfs pull` in the repo (if git-lfs is configured) or download the model files from the OpenCV Zoo release page and place them here.
