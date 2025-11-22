
# DyCoke : **Dynamic Compression of Tokens for Fast Video Large Language Models**

[Keda Tao](), [Can Qin](https://canqin.tech/), [Haoxuan You](https://hxyou.github.io/), [Yang Sui](https://eclipsess.github.io/yangsui.github.io/), [Huan Wang](https://huanwang.tech/), "DyCoke 🥤Dynamic Compression of Tokens for Fast Video Large Language Models"

[[Paper](https://arxiv.org/abs/2411.15024)]

### Demo

![video](figures/video-ezgif.com-resize-2.gif)
#### 🔥🔥🔥 News

- **2025-11-20**: Our new work **[OmniZip](https://github.com/KD-TAO/OmniZip)**, an audio-guided token compression method for OmniLLMs, has been released.
- **2025-11-10**: Thanks to [mvish7](https://github.com/mvish7), DyCoke can be used on **Gemma3** and **Qwen2.5-VL** now! ([Link)](https://github.com/mvish7/dycoke_token_compression/)
- **2025-02-26**: **Our paper has been accepted by CVPR 2025!**
- **2024-11-25**: The paper is released.
- **2024-11-22:** This repo is released.

![overview](figures/overview.png)


> **Abstract:** Video large language models (VLLMs) have significantly advanced recently in processing complex video content, yet their inference efficiency remains constrained because of the high computational cost stemming from the thousands of visual tokens generated from the video inputs. We empirically observe that, unlike single image inputs, VLLMs typically attend visual tokens from different frames at different decoding iterations, making a one-shot pruning strategy prone to removing important tokens by mistake. Motivated by this, we present DyCoke, a training-free token compression method to optimize token representation and accelerate VLLMs. DyCoke incorporates a plug-and-play temporal compression module to minimize temporal redundancy by merging redundant tokens across frames, and applies dynamic KV cache reduction to prune spatially redundant tokens selectively. It ensures high-quality inference by dynamically retaining the critical tokens at each decoding step. Extensive experimental results demonstrate that DyCoke can outperform the prior SoTA counterparts, achieving 1.5X inference speedup, 1.4X memory reduction against the baseline VLLM, while still improving the performance, with no training.

## ⚒️ TODO

* [x] Release Paper 
* [x] Release code 
* [x] Support more models

## Install
##### 1. **Clone this repository and navigate to the LLaVA folder:**
```bash
git clone https://github.com/KD-TAO/DyCoke.git
cd DyCoke
```

##### 2. **Install the inference package:**
```bash
conda create -n dycoke python=3.10 -y
conda activate dycoke
pip install --upgrade pip  # Enable PEP 660 support.
pip install lmms-eval
pip install -e ".[train]"
```

## Evaluation
#### Set the DyCoke parameters
- We use the [lmms-eval](https://github.com/EvolvingLMMs-Lab/lmms-eval) toolkit to evaluate our models. It's worth noting that you can specify DyCoke Settings via parameters, such as:
```bash
...
--model_args pretrained=lmms-lab/llava-onevision-qwen2-7b-ov,conv_template=qwen_1_5,model_name=llava_qwen,dycoke=True,dycoke_l=3,dycoke_p=0.7,dycoke_k=0.7 \
...
```
- Our main baseline model is [LLaVA-OV](https://github.com/LLaVA-VL/LLaVA-NeXT/tree/main), if you want to switch between different model frameworks, please change the following parameters:
```bash
...
--model_args pretrained=lmms-lab/llava-onevision-qwen2-0.5b-ov,conv_template=qwen_1_5,model_name=llava_qwen,dycoke=True,dycoke_num_image_per_frame=$YOUR_NUM,image_token_start_index=$YOUR_IDX \
...
```
##### 1. Test on the specified task：
```bash
accelerate launch --num_processes=8 \
-m lmms_eval \
--model llava_onevision \
--model_args pretrained=lmms-lab/llava-onevision-qwen2-7b-ov,conv_template=qwen_1_5,model_name=llava_qwen,dycoke=True \
--tasks $YOUR-TASKS \  # Such as "activitynetqa,video_dc499,perceptiontest_val_mc,videomme_w_subtitle,videomme,nextqa_mc_test..."
--batch_size 1 \
--log_samples \
--log_samples_suffix llava_onevision \
--output_path ./logs/
```
##### 2. **Reproduce the results**：
```bash
bash eval.sh
```
##### 3. **Test on the LLaVA-OV-72B**：
```bash
CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7,8 accelerate launch --num_processes=1 \
-m lmms_eval \
--model llava_onevision \
--model_args pretrained=lmms-lab/llava-onevision-qwen2-7b-ov,conv_template=qwen_1_5,model_name=llava_qwen,dycoke=True,device_map=auto \
--tasks $YOUR-TASKS \  # Such as "activitynetqa,video_dc499,perceptiontest_val_mc,videomme_w_subtitle,videomme,nextqa_mc_test..."
--batch_size 1 \
--log_samples \
--log_samples_suffix llava_onevision \
--output_path ./logs/
```

## 👀 Results on Video-Language Models

![overview](figures/table.png)

![overview](figures/case.png)
## Acknowledgement

This project is based on [LLaVA-NeXT](https://github.com/LLaVA-VL/LLaVA-NeXT). Thanks for their awesome work.

## Contact

If you have any questions, please feel free to contact with me at KD.TAO.CT@outlook.com

## Citation

If you find this work useful for your research, please consider citing our paper:

```bibtex
@inproceedings{tao2025dycoke,
  title={DyCoke: Dynamic Compression of Tokens for Fast Video Large Language Models},
  author={Tao, Keda and Qin, Can and You, Haoxuan and Sui, Yang and Wang, Huan},
  booktitle={Proceedings of the Computer Vision and Pattern Recognition Conference},
  pages={18992--19001},
  year={2025}
}
```
