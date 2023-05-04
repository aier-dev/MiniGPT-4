#!/usr/bin/env python

import torch
import argparse
from minigpt4.conversation.conversation import Chat
from minigpt4.common.config import Config
from minigpt4.common.registry import registry
from os.path import abspath, dirname, join
from gpu import GPU

ROOT = dirname(abspath(__file__))


def parse_args():
    parser = argparse.ArgumentParser(description="Demo")
    parser.add_argument("--cfg-path", help="path to configuration file.")
    parser.add_argument("--gpu-id", type=int, default=0, help="specify the gpu to load the model.")
    parser.add_argument(
        "--options",
        nargs="+",
        help="override some settings in the used config, the key-value pair "
        "in xxx=yyy format will be merged into config file (deprecate), "
        "change to --cfg-options instead.",
    )
    args = parser.parse_args()
    args.cfg_path = args.cfg_path or join(ROOT, 'eval_configs/minigpt4_eval.yaml')
    return args


# ========================================
#             Model Initialization
# ========================================

print('Initializing Chat')
args = parse_args()
print(args)
cfg = Config(args)

model_config = cfg.model_cfg
model_config.device_8bit = args.gpu_id
model_cls = registry.get_model_class(model_config.arch)
model = model_cls.from_config(model_config).to(GPU)
model = torch.compile(model)

vis_processor_cfg = cfg.datasets_cfg.cc_sbu_align.vis_processor.train
vis_processor = registry.get_processor_class(vis_processor_cfg.name).from_config(vis_processor_cfg)
chat = Chat(model, vis_processor, device=GPU)
print('Initialization Finished')
