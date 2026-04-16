# Local Inference Notes

This repository ships two main local inference paths: vLLM for higher-throughput runs, and Transformers for simpler single-machine debugging.

## Environment summary

| Component | Recommended baseline | Notes |
|---|---|---|
| Python | 3.12 for the documented Conda flow | Match the wheel you install for vLLM |
| CUDA | 11.8+ | The root install instructions use the cu118 PyTorch index |
| PyTorch | `2.6.0` | Keep the Torch / torchvision / torchaudio versions aligned |
| vLLM | `0.8.5` wheel or newer upstream recipe | Prefer the upstream recipe when testing official support paths |
| `flash-attn` | `2.7.3` | Building this package may require a working CUDA toolchain |

## Choosing a runtime

### Use vLLM when:

- you need PDF parsing or batched evaluation;
- you want higher throughput on a GPU server;
- you are comfortable managing a dedicated inference environment.

### Use Transformers when:

- you want to debug one image at a time;
- you prefer a smaller, script-first setup;
- you do not need the vLLM serving stack.

## GPU sizing guidance

- Small image experiments are the safest place to validate the environment first.
- Large page sizes, PDF runs, and high `MAX_CONCURRENCY` values increase memory pressure quickly.
- If your GPU memory is limited, lower `MAX_CROPS`, `MAX_CONCURRENCY`, or test with smaller modes before moving to `Base` / `Large`.
