
import unittest

from extractor import parse_json_response


class TestJSONParser(unittest.TestCase):

    def test_valid_json(self):
        result = parse_json_response(
            '{"invoice_number": "INV-1001"}'
        )
        self.assertEqual(result["invoice_number"], "INV-1001")

    def test_json_inside_markdown_fences(self):
        response = '''```json
{"invoice_number": "INV-1002"}
```'''
        result = parse_json_response(response)
        self.assertEqual(result["invoice_number"], "INV-1002")

    def test_json_with_explanatory_text(self):
        response = (
            'Here is the extracted invoice:\n'
            '{"invoice_number": "INV-1003"}\n'
            'Extraction complete.'
        )
        result = parse_json_response(response)
        self.assertEqual(result["invoice_number"], "INV-1003")

    def test_empty_response(self):
        with self.assertRaises(ValueError):
            parse_json_response("")

    def test_malformed_json(self):
        with self.assertRaises(ValueError):
            parse_json_response('{"invoice_number": ')


if __name__ == "__main__":
    unittest.main(verbosity=2)
