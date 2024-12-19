# IMPORTANT: Set your OpenAI API key
export OPENAI_API_KEY="YOUR_OPENAI_API_KEY"

CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7,8 accelerate launch \
    --num_processes=9 \
    --main_process_port=25001 \
    -m lmms_eval \
    --model llava_onevision \
   --model_args pretrained=lmms-lab/llava-onevision-qwen2-7b-ov,conv_template=qwen_1_5,model_name=llava_qwen,device_map=auto,dycoke=True \
    --tasks activitynetqa,video_dc499,perceptiontest_val_mc,videomme_w_subtitle,videomme,nextqa_mc_test \
    --batch_size 1 \
    --log_samples \
    --log_samples_suffix llava_onevision \
    --output_path ./logs/
