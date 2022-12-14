import os
import os.path as osp
import argparse
import sys
import torch
import torch.nn as nn
import torch.nn.functional as F
import pandas as pd

from torch_geometric.datasets import Planetoid, Coauthor, Amazon
import torch_geometric.transforms as T

from model import * 
from dataset import *

parser = argparse.ArgumentParser()
parser.add_argument('--model', type=str, default='CLNR') 
parser.add_argument('--dataset', type=str, default='Physics') 
parser.add_argument('--epochs', type=int, default=5)
parser.add_argument('--n_layers', type=int, default=2)
parser.add_argument('--tau', type=float, default=0.5) 
parser.add_argument('--lr1', type=float, default=1e-3)
parser.add_argument('--wd1', type=float, default=0.0)
parser.add_argument('--lr2', type=float, default=5e-3)
parser.add_argument('--wd2', type=float, default=1e-4)
parser.add_argument('--channels', type=int, default=512) 
parser.add_argument('--fmr', type=float, default=0.2)
parser.add_argument('--edr', type=float, default=0.5)
parser.add_argument('--mlp_use', type=bool, default=False)
parser.add_argument('--result_file', type=str, default="/results/")
args = parser.parse_args()

file_path = os.getcwd() + args.result_file
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

results =[]
data, train_idx, val_idx, test_idx = load(args.dataset, device)
model = ContrastiveLearning(args, data)
model.train()
eval_acc = model.LinearEvaluation(train_idx, val_idx, test_idx)
results += [[args.model, args.dataset, args.epochs, args.n_layers, args.tau, args.lr1, args.lr2, args.wd1, args.wd2, args.channels, args.edr, args.fmr, eval_acc.item()]]
res = pd.DataFrame(results, columns=['model', 'dataset', 'epochs', 'layers', 'tau', 'lr1', 'lr2', 'wd1', 'wd2', 'channels', 'edge_drop_rate', 'feat_mask_rate', 'accuracy'])
res.to_csv(file_path + "_" + args.model + "_" + args.dataset +  ".csv", index=False)
