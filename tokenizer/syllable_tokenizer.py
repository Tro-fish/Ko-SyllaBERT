from transformers import PreTrainedTokenizer
import json
import os

class SyllableTokenizer(PreTrainedTokenizer):
    def __init__(
        self,
        vocab_file,
        do_lower_case=False,
        do_basic_tokenize=True,
        never_split=None,
        unk_token="[UNK]",
        sep_token="[SEP]",
        eos_token="[EOS]",
        bos_token="[BOS]",
        pad_token="[PAD]",
        cls_token="[CLS]",
        mask_token="[MASK]",
        tokenize_chinese_chars=True,
        **kwargs
    ):
        # Load vocabulary
        with open(vocab_file, 'r', encoding='utf-8') as f:
            self.vocab = json.load(f)
        # Initialize special tokens
        self.mask_token = mask_token
        self.sep_token = sep_token
        self.cls_token = cls_token
        self.pad_token = pad_token
        self.eos_token = eos_token
        self.bos_token = bos_token
        self.unk_token = unk_token

        self.ids_to_tokens = {id: token for token, id in self.vocab.items()}
        super().__init__(pad_token=self.pad_token, eos_token=self.eos_token, bos_token=self.bos_token, unk_token=self.unk_token, mask_token=self.mask_token, **kwargs)
        
    @property
    def vocab_size(self):
        return len(self.vocab)
    
    def get_vocab(self):
        return dict(self.vocab, **self.added_tokens_encoder)
    
    def _tokenize(self, text):
        return list(" ".join(text.split()))  # Erase duplicate space

    def _convert_token_to_id(self, token):
        """ Converts a token (str) in an id using the vocab. """
        return self.vocab.get(token, self.vocab.get(self.unk_token))

    def _convert_id_to_token(self, index):
        """Converts an index (integer) in a token (str) using the vocab."""
        return self.ids_to_tokens.get(index, self.unk_token)

    def convert_tokens_to_string(self, tokens):
        """ Converts a sequence of tokens (string) in a single string. """
        return "".join(tokens).strip()

    def save_vocabulary(self, vocab_path, filename_prefix=None):
        """
        Save the tokenizer vocabulary and special tokens file to a directory.

        Args:
            vocab_path (str): The directory in which to save the vocabulary.
            filename_prefix (str, optional): A prefix to add to the saved vocabulary filename.

        Returns:
            Tuple[str]: Paths to the files saved.
        """
        index = 0
        if os.path.isdir(vocab_path):
            vocab_filename = "vocab.txt" if filename_prefix is None else f"{filename_prefix}_vocab.txt"
            vocab_file = os.path.join(vocab_path, vocab_filename)
        else:
            vocab_file = vocab_path

        with open(vocab_file, "w", encoding="utf-8") as writer:
            for token, token_index in sorted(self.vocab.items(), key=lambda kv: kv[1]):
                if index != token_index:
                    logger.warning(
                        f"Saving vocabulary to {vocab_file}: vocabulary indices are not consecutive. "
                        "Please check that the vocabulary is not corrupted!"
                    )
                    index = token_index
                writer.write(token + "\n")
                index += 1

        return (vocab_file,)
