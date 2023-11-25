import numpy as np

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader

import lance
import lightning

from transformers import GPT2TokenizerFast

tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

class Config:
    vocab_size = 50304 # changing it from 50257 to the nearest multiple of 64 which will boost ops
    n_epochs = 50
    batch_size = 48
    lr = 3e-4
    wd = 1e-6
    n_embed = 256
    num_blocks = 12
    num_heads = 12
    head_size = n_embed // num_heads
    context_len = 224
    attn_dropout_val = 0.2
    mha_dropout_val = 0.2
    ffn_dropout_val = 0.2

class CausalAttentionHead(nn.Module):
    def __init__(self, config):
        super(CausalAttentionHead, self).__init__()
        self.config = config

        # QKV layers
        self.query = nn.Linear(config.n_embed, config.head_size, bias=False)
        self.key = nn.Linear(config.n_embed, config.head_size, bias=False)
        self.value = nn.Linear(config.n_embed, config.head_size, bias=False)
        self.attn_drop = nn.Dropout(config.attn_dropout_val)

        # Mask for ensuring causality during training
        self.register_buffer('mask', torch.tril(torch.ones(config.context_len, config.context_len)))

    def forward(self, x):
        # Shape of x: [bs, context_len, embed_dim]
        bs, context_len, embed_dim = x.shape
        q, k, v = self.query(x), self.key(x), self.value(x)

        # Get the attention weights
        attn_filter = torch.divide(torch.bmm(q, k.transpose(1, 2)), self.config.head_size)
        attn_filter = attn_filter.masked_fill(self.mask[:context_len, :context_len]==0, float('-inf'))
        attn_weights = F.softmax(attn_filter, dim=-1)
        attn_weights = self.attn_drop(attn_weights)

        # Now we do weighted aggregation of values to get the output of attention
        # attn_weights [bs, c, c] x V [bs, c, h] = output [bs, c, head_size]
        output = torch.bmm(attn_weights, v)
        return output
    
class MultiHeadedAttention(nn.Module):
    def __init__(self, config):
        super(MultiHeadedAttention, self).__init__()
        self.config = config

        # Turn all the AttentionHeads into a ModuleList
        self.heads = nn.ModuleList(
            [CausalAttentionHead(config) for _ in range(config.num_heads)]
        )

        # Projection and Dropout that projects mha_output it back to n_embed dim
        self.proj = nn.Linear(config.num_heads*config.head_size, config.n_embed)
        self.mha_drop = nn.Dropout(config.mha_dropout_val)

    def forward(self, x):
        # Concatenate all the attention head outputs together
        mha_output = torch.cat([head(x) for head in self.heads], dim=-1)
        return self.mha_drop(self.proj(mha_output))
    
class FeedForwardNet(nn.Module):
    def __init__(self, config):
        super(FeedForwardNet, self).__init__()

        self.ffn = nn.Sequential(
            nn.Linear(config.n_embed, config.n_embed*4),
            nn.GELU(),
            nn.Linear(config.n_embed*4, config.n_embed),
            nn.Dropout()
        )

    def forward(self, x):
        return self.ffn(x)
    
class Block(nn.Module):
    def __init__(self, config):
        super(Block, self).__init__()

        # Architecture of one block of GPT
        self.mha = MultiHeadedAttention(config)
        self.ln1 = nn.LayerNorm(config.n_embed)
        self.ffn = FeedForwardNet(config)
        self.ln2 = nn.LayerNorm(config.n_embed)

    def forward(self, x):
        x = self.ln1(x + self.mha(x))
        x = self.ln2(x + self.ffn(x))
        return x
    
class GPT(lightning.LightningModule):
    def __init__(self, config):
        super(GPT, self).__init__()
        self.config = config
        self.save_hyperparameters()

        # Define token and positional embeddings
        self.token_embedding = nn.Embedding(config.vocab_size, config.n_embed)
        self.positional_embedding = nn.Embedding(config.context_len, config.n_embed)

        # Define the blocks
        self.backbone = nn.Sequential(*[Block(config) for _ in range(config.num_blocks)])

        # Define the LM head
        self.lm_head = nn.Linear(config.n_embed, config.vocab_size)

    def forward(self, x):
        # Apply token embeddings through the data (B, C) -> (B, C, V)
        tok_emb = self.token_embedding(x)

        # Get positional embeddings using torch.arange
        pos_emb = self.positional_embedding(torch.arange(x.shape[1], device=self.device))

        # Add both embeddings
        x = tok_emb + pos_emb

        # Pass the input data through all blocks
        x = self.backbone(x)

        # Pass it through the lm head
        logits = self.lm_head(x)
        return logits

    def get_loss(self, predictions, target):
        B, C, V = predictions.shape
        predictions = predictions.view(B*C, V)
        target = target.view(B*C)
        loss = F.cross_entropy(predictions, target)
        return loss

    def training_step(self, batch, batch_idx):
        text, target = batch
        text = text.long()
        target = target.long()
        logits = self(text)
        loss = self.get_loss(logits, target)

        self.log('loss', loss.item(), prog_bar=True)

        logs = {'loss': loss}
        return {'log': logs, 'loss': loss}

    def training_end(self, outputs):
        avg_loss = torch.stack([x['log']['loss'] for x in outputs]).mean()

        logs = {'loss': avg_loss}

        print(f"val_loss: {avg_loss}")
        return {'log': logs}

    def configure_optimizers(self):
        opt = torch.optim.AdamW(self.parameters(), lr=self.config.lr, weight_decay=self.config.wd)
        return [opt], []

def generate(model, prompt, max_tokens, temperature=0.7):
    """
    Generates text based on the provided prompt.
    Model determinism can be changed with temperature 
    (range: [0, 1], higher means more unstable but creative predictions)
    """
    model.eval()
    for _ in range(max_tokens):
        prompt = prompt[:, :config.context_len]
        logits = model(prompt)
        logits = logits[:, -1, :] / temperature
        logit_probs = nn.functional.softmax(logits, dim=-1)
        next_prompt = torch.multinomial(logit_probs, num_samples=1)
        prompt = torch.cat((prompt, next_prompt), dim=1)
    return prompt

class GPTDataset(Dataset):
    def __init__(self, dataset_path, context_len):
        # Load the lance dataset from the saved path
        self.ds = lance.dataset(dataset_path)
        self.context_len = context_len
        # Doing this so the sampler never asks for an index at the end of text
        self.length = self.ds.count_rows() - context_len

    def __len__(self):
        return self.length

    def from_idxs(self, idxs):
        """
        Little Utility function to get the data from lance
        """
        data = self.ds.take(idxs).to_pylist()
        data = torch.tensor(list(map(lambda x: x['value'], data)))
        return data

    def __getitem__(self, idx):
        """
        Generate a list of indices starting from the current idx to idx+context_len+1
        Use the from_idxs function to get data in said indexes and then divide it into features (x) and target (y)
        """
        current_window_idxs = np.arange(idx, idx+self.context_len+1)
        data = self.from_idxs(current_window_idxs)
        x = data[0:self.context_len]
        y = data[1:self.context_len+1] # +1 because our target is the sentence is 1 step ahead of input text
        return x, y
    
if __name__ == "__main__":
    # Path of the encoded lance dataset
    dataset_path = "tiny_stories_gpt4_encoded.lance"

    # Init config
    config = Config()

    # Init model
    gpt = GPT(config)

    # Init the dataset
    dataset = GPTDataset(dataset_path, config.context_len)
    loader = DataLoader(
        dataset,
        batch_size=config.batch_size,
        shuffle=False,
    )
    
    print("Starting training run...")

    # Init the trainer
    trainer = lightning.Trainer(accelerator='auto', max_epochs=config.n_epochs)

    # Fit on the data
    trainer.fit(gpt, loader)