import torch
import torch.nn.functional as F
import torch.nn as nn

## TODO : annotate

class MultiHeadAttention(nn.Module):
    def __init__(self, input_dim, num_heads):
        super(MultiHeadAttention, self).__init__()
        assert input_dim % num_heads == 0, "Input dimension must be divisible by the number of heads"
        self.input_dim = input_dim
        self.num_heads = num_heads
        self.head_dim = input_dim // num_heads
        
        # Linear projections for queries, keys, and values for each head
        self.W_q = nn.Linear(input_dim, num_heads * self.head_dim, bias=False)
        self.W_k = nn.Linear(input_dim, num_heads * self.head_dim, bias=False)
        self.W_v = nn.Linear(input_dim, num_heads * self.head_dim, bias=False)
        
        # Final linear transformation after concatenation
        self.W_out = nn.Linear(num_heads * self.head_dim, input_dim)

    def forward(self, query, key, value, mask=None):
        """
        Perform multi-head attention
        
        Args:
            query, key, value: Tensors of shape (batch_size, seq_len, input_dim)
            mask: Attention mask to mask padded elements (optional)
        
        Returns:
            output: Contextualized representation of input tensors
        """
        batch_size = query.shape[0]
        
        # Step 1: Linear projections for queries, keys, and values
        # Linear projections for queries, keys, and values
        Q = self.W_q(query).view(batch_size, -1, self.num_heads, self.head_dim)
        K = self.W_k(key).view(batch_size, -1, self.num_heads, self.head_dim)
        V = self.W_v(value).view(batch_size, -1, self.num_heads, self.head_dim)

        # Transpose to get dimensions: (batch_size, self.num_heads, seq_len, self.head_dim)
        Q = Q.transpose(1, 2)
        K = K.transpose(1, 2)
        V = V.transpose(1, 2)

        # Calculate attention scores using scaled dot-product attention. Dim of scores: (batch_size, self.num_heads, seq_len, seq_len)
        scores = torch.matmul(Q, K.transpose(-2, -1)) / torch.sqrt(torch.tensor(self.head_dim).float())

        # Apply mask (if provided)
        if mask is not None:
            scores = scores.masked_fill(mask == 0, float("-1e20"))

        # Apply softmax to get attention weights
        attn_weights = F.softmax(scores, dim=-1)

        # Apply attention weights to the value vectors. Dim of context: (batch_size, self.num_heads, seq_len, self.head_dim)
        context = torch.matmul(attn_weights, V)

        # Transpose and concatenate to get back to the input dimensions. Dim: (batch_size, seq_len, input_dim)
        context = context.transpose(1, 2).contiguous().view(batch_size, -1, self.num_heads * self.head_dim)

        # Apply output linear layer. Dim: (batch_size, seq_len, input_dim)
        output = self.W_out(context)

        return output


if __name__ == "__main__":
    # Test case
    input_size = 128
    num_heads = 8
    seq_len = 10
    batch_size = 32

    # Create a random input tensor
    input_tensor = torch.randn(batch_size, seq_len, input_size)

    # Instantiate the MultiHeadAttention module
    attention = MultiHeadAttention(input_size, num_heads)

    # Forward pass
    query = key = value = input_tensor
    output = attention(query, key, value)

    print("Input shape:", input_tensor.shape)
    print("Output shape:", output.shape)
