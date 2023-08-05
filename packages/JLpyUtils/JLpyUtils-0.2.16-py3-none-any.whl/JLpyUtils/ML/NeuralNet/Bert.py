"""
Functions/classes using the transformers API from HuggingFaces, which provides a streamlined interface to google's bert model.

Bert: https://github.com/google-research/bert
transformers: https://huggingface.co/transformers/index.html
"""

import torch as _torch
import transformers as _transformers #pytorch_pretrained_bert
from .. import _devices

class word2vec():
    
    def __init__(self, model_ID = 'bert-base-uncased'):
        """
        Use bert to perform word2vect operations on text of interest
        
        Arguments:
        ---------
            model_ID: string. bert model ID.
                - bert-base-uncased: 12-layer, 768-hidden, 12-heads, 110M parameters
                - bert-large-uncased: 24-layer, 1024-hidden, 16-heads, 340M parameters
                - bert-base-cased: 12-layer, 768-hidden, 12-heads , 110M parameters
                - bert-large-cased: 24-layer, 1024-hidden, 16-heads, 340M parameters
        
        Notes:
        ------
            See the article and docs below for a basic walkthrough from which this class was derived
            https://mccormickml.com/2019/05/14/BERT-word-embeddings-tutorial/
            https://huggingface.co/transformers/index.html
        """
        self.model_ID = model_ID
        self.tokenizer = _transformers.BertTokenizer.from_pretrained(model_ID)
        
    def _insert_transformers_special_tokens(self, text):
        """
        add special ending and starting tokens to text
        """
        return "[CLS] " + text + " [SEP]"
    
    def fit_transform(self, text, verbose = 0):
        """
        Fit and transform the text data of interest. We assume the text is a single "sentence" or a list of different sentence samples
        
        Arguments:
        ----------
            text: a single sentence or a list of sentences
            
        Returns:
        --------
            vect: a vector enconding of length 768
        """

        text = self._insert_transformers_special_tokens(text)
        
        self._tokenized_text = self.tokenizer.tokenize(text)
        self._indexed_tokens = self.tokenizer.convert_tokens_to_ids(self._tokenized_text)
        self._segments_ids = [1] * len(self._indexed_tokens)
        
        # Convert inputs to PyTorch tensors
        self._tokens_tensor = _torch.tensor([self._indexed_tokens])
        self._segments_tensors = _torch.tensor([self._segments_ids])
        
        # Load pre-trained model (weights)
        self.model = _transformers.BertModel.from_pretrained(self.model_ID)

        # Put the model in "evaluation" mode, meaning feed-forward operation.
        self.model.eval()
        
        #check if a gpu is available
        device_counts = _devices.device_counts()
        if device_counts['GPUs']>1:
            self._tokens_tensor = self._tokens_tensor.to('cuda')
            self._segments_tensors = self._segments_tensors.to('cuda')
            self.model.to('cuda')
        
        with _torch.no_grad():
            self.outputs = self.model(self._tokens_tensor, self._segments_tensors)
            self.encoded_layers = self.outputs[0]
            
        self.n_batches = len(self.encoded_layers)
        assert(self.n_batches==1), 'Computed on '+str(self.n_batches)+' batches. Evaluating vector on multiple batches is not supported'
        
        batch_i = 0
        self.n_tokens = len(self.encoded_layers[batch_i])
        
        token_i = 0
        self.n_hidden_units = len(self.encoded_layers[batch_i][token_i])
        
        vect = _torch.mean(self.encoded_layers, 1).tolist()[0]
        
        if self.model_ID == 'bert-base-uncased':
            assert(len(vect)==768), 'len(vect) = '+str(len(vect))+'. Expected len(vect)=768'
        
        return vect