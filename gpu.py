#!/usr/bin/env python

if torch.cuda.is_available():
    GPU = 'cuda:{}'.format(args.gpu_id)
elif torch.backends.mps.is_built():
    GPU = 'mps'
else:
    GPU = None
