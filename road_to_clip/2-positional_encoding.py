import torch
import torch.nn as nn
from torch import Tensor

import torch
import torch.nn as nn
import math

class SinusoidalPositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=512):
        super(SinusoidalPositionalEncoding, self).__init__()

        # Create an empty tensor for positional encoding with dimensions (max_len, d_model)
        self.encoding = torch.zeros(max_len, d_model)

        # Create a tensor representing positions from 0 to max_len - 1
        position = torch.arange(0, max_len).unsqueeze(1).float()

        # Calculate the div_term for sinusoidal function
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * -(math.log(10000.0) / d_model))

        # Apply sinusoidal functions to even and odd indices of the tensor
        self.encoding[:, 0::2] = torch.sin(position * div_term)
        self.encoding[:, 1::2] = torch.cos(position * div_term)

        # Add an extra dimension to make the encoding tensor of shape (1, max_len, d_model)
        self.encoding = self.encoding.unsqueeze(0)

    def forward(self, x):
        # Add the sinusoidal positional encoding to the input tensor x
        return x + self.encoding[:, :x.size(1)].detach()

