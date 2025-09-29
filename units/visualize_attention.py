import torch
import numpy as np
import os
import time
import os
import matplotlib.pyplot as plt

# Load attention maps from saved .npz file
# The attention maps should be saved using np.savez() with each iteration as a separate key
attention_file = "attention_scores.npz"

video_frames = range(16)

start_time = time.time()
loaded_data = np.load(attention_file, allow_pickle=True)
print(
    f"Loaded {len(loaded_data)} attentions. Elapsed time: {time.time() - start_time:.2f} seconds"
)
attentions = [torch.tensor(loaded_data[key]) for key in loaded_data]


output_dir = "attention_visualizations"
os.makedirs(output_dir, exist_ok=True)

attention_matrix = np.zeros((len(video_frames), len(attentions)))

for iteration, iteration_attentions in enumerate(attentions):
    for frame_idx, frame in enumerate(video_frames):
        frame_attention_values = []
        for layer_attention in iteration_attentions:
            head_attention = layer_attention.mean(dim=1)[0][-1]
            frame_attention = head_attention[
                14 + frame_idx * 196 : 14 + (frame_idx + 1) * 196
            ]
            if torch.isnan(frame_attention).any():
                continue
            frame_attention_values.append(frame_attention.mean().item())
        if frame_attention_values:
            attention_matrix[frame_idx, iteration] = np.nanmean(frame_attention_values)
        else:
            attention_matrix[frame_idx, iteration] = float("nan")

plt.figure(figsize=(12, 8))
plt.imshow(attention_matrix, aspect="auto", cmap="viridis", interpolation="nearest")
plt.colorbar(pad=0.005)
plt.xlabel("Iteration Index", fontsize=17, fontweight="bold") 
plt.ylabel("Frame Index", fontsize=17, fontweight="bold")  

num_xticks = 10 
xtick_positions = np.linspace(0, len(attentions) - 1, num_xticks, dtype=int)
xtick_labels = [f"{i + 1}" for i in xtick_positions]
plt.xticks(
    xtick_positions, xtick_labels, rotation=0, fontsize=12
) 


save_name = "attention_heatmap.pdf"
plt.yticks(
    range(len(video_frames)),
    [f"{i + 1}" for i in range(len(video_frames))],
    fontsize=12,
) 
plt.tight_layout()
plt.savefig(os.path.join(output_dir, save_name))
plt.close()

# os.system(f"open {os.path.join(output_dir, save_name)}")
