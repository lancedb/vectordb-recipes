import torch
import torch.nn as nn

class Attention(nn.Module):
    def __init__(self, input_dim):
        super(Attention, self).__init__()
        self.input_dim = input_dim
        
        # Define linear layers for computing attention scores
        self.W_q = nn.Linear(input_dim, input_dim, bias=False)
        self.W_k = nn.Linear(input_dim, input_dim, bias=False)
        self.W_v = nn.Linear(input_dim, input_dim, bias=False)
        
    def forward(self, query, key, value):
        # Compute query, key, and value projections
        Q = self.W_q(query) # query.shape[0] x input_dim
        K = self.W_k(key) # key.shape[0] x input_dim
        V = self.W_v(value) # value.shape[0] x input_dim
        
        
        # Step 1: Compute attention scores
        # The attention mechanism computes a score for each pair of Query and Key. This score indicates how much focus or importance 
        # should be given to the corresponding Value. Mathematically, it's computed as the dot product of the Query and Key vectors.
        # (query.shape[0] x input_dim) x (input_dim x key.shape[0]) = query.shape[0] x key.shape[0]
        # (query.shape[0] x input_dim)
        scores = torch.matmul(Q, K.transpose(-2, -1)) 
        attn_scores = scores / torch.sqrt(torch.tensor(self.input_dim).float())

        # Step 2: Softmax to get attention weights
        # Attention Weights: After computing the scores, they are usually normalized (often with a softmax function) to obtain attention weights. 
        # These weights represent how much each element in the sequence is relevant to the query, i.e, model should pay more 
        # attention to that element that has a higher weight.
        # (query.shape[0] x query.shape[0])
        attn_weights = torch.nn.functional.softmax(attn_scores, dim=-1)
        
        # Step 3: Apply attention weights to value
        # The resultant dimention of the attention weights is (query.shape[0] x ). This is then multiplied with the Value vector to get the
        # (query.shape[0] x key.shape[0]) x (value.shape[0] x input_dim) = query.shape[0] x input_dim
        # query.shape[0] x input_dim
        attention_output = torch.matmul(attn_weights, V)
        return attn_weights, attention_output


if __name__ == "__main__":
    input_dim = 512  # Example input dimension
    attention = Attention(input_dim)

    query = torch.randn(1, 10, input_dim)  # Batch size 1, sequence length 10, input dimension
    key = torch.randn(1, 10, input_dim)
    value = torch.randn(1, 10, input_dim)

    attn_weights, attention_output, context_vector = attention(query, key, value)
    print(attn_weights.shape)
    print(attention_output.shape)

