from huggingface_hub import snapshot_download
from safetensors import safe_open
import hashlib

def tensor_hashes(path):
    out = {}
    with safe_open(path, framework="pt") as f:
        for key in f.keys():
            out[key] = hashlib.sha256(f.get_tensor(key).numpy().tobytes()).hexdigest()
    return out

# Resolves to the already-cached local snapshot dir, no download since it's all local
model_dir = snapshot_download("convaiinnovations/laya")

root_path = f"{model_dir}/model.safetensors"
td_path = f"{model_dir}/typed-decisions/model.safetensors"

print("root path:", root_path)
print("td path:  ", td_path)

root_h = tensor_hashes(root_path)
td_h = tensor_hashes(td_path)

print("same key set:", set(root_h) == set(td_h))
diffs = [k for k in root_h if root_h.get(k) != td_h.get(k)]
print(f"{len(diffs)} of {len(root_h)} tensors differ")
if diffs:
    print("first few differing keys:", diffs[:5])