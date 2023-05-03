#!/usr/bin/env python

from huggingface_hub import snapshot_download

snapshot_download(repo_id="xxai-art/minigpt4", local_dir="model")
