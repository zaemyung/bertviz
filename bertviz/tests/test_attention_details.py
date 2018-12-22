from bertviz.attention_details import AttentionDetailsData
from bertviz.pytorch_pretrained_bert import BertTokenizer, BertModel, BertConfig
import unittest


class TestAttentionDetails(unittest.TestCase):

    def setUp(self):
        self.config = BertConfig.from_json_file('fixtures/config.json')
        model = BertModel(self.config)
        tokenizer = BertTokenizer('fixtures/vocab.txt')
        self.attention_details_data = AttentionDetailsData(model, tokenizer)

    def test_get_inputs(self):
        sentence1 = 'The quickest brown fox jumped over the lazy dog'
        tokens_ids1 = [2, 3, 4, 5, 6, 8, 9, 2, 14, 12]
        sentence2 = "the quick brown fox jumped over the laziest lazy elmo"
        token_ids2 = [2, 3, 5, 6, 8, 9, 2, 15, 10, 11, 14, 1]
        tokens_tensor, token_type_tensor, tokens_a, tokens_b = self.attention_details_data._get_inputs(sentence1, sentence2)
        cls_id = 17
        sep_id = 16
        self.assertEqual(tokens_tensor.tolist()[0],
                         [cls_id] + tokens_ids1 + [sep_id] + token_ids2 + [sep_id])
        self.assertEqual(token_type_tensor.tolist()[0],
                         ([0] * 12) + ([1] * 13))

    def test_get_data(self):
        sentence1 = 'The quickest brown fox jumped over the lazy dog'
        tokens1 = ['the', 'quick', '##est', 'brown', 'fox', 'jumped', 'over', 'the', 'lazy', 'dog']
        sentence2 = "the quick brown fox jumped over the laziest lazy elmo"
        tokens2 = ['the', 'quick', 'brown', 'fox', 'jumped', 'over', 'the', 'la', '##zie', '##st', 'lazy', '[UNK]']
        tokens_a, tokens_b, queries, keys = self.attention_details_data.get_data(sentence1, sentence2)
        self.assertEqual(tokens_a, ['[CLS]'] + tokens1 + ['[SEP]'])
        self.assertEqual(tokens_b, tokens2 + ['[SEP]'])
        batch_size = 1
        query_key_size = self.config.hidden_size / self.config.num_attention_heads
        seq_len = len(tokens_a) + len(tokens_b)
        expected_shape = (self.config.num_hidden_layers, batch_size, self.config.num_attention_heads, seq_len, query_key_size)
        self.assertEqual(queries.shape, expected_shape)
        self.assertEqual(keys.shape, expected_shape)

if __name__ == "__main__":
    unittest.main()

