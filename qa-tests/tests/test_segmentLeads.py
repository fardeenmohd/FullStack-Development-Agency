import unittest

class TestSegmentLeads(unittest.TestCase):
    def test_segment_by_attribute(self):
        attributes = ['country', 'industry', 'product_interest']
        for attr in attributes:
            leads = [
                {'name': f'{letter} {name}', attr: letter.upper()} for letter, name in zip('ABC', ['Doe', 'Smith', 'Johnson'])
            ]
            segmented_leads = segment_leads(leads, attr)
            expected_segments = {value: [item for item in leads if item[attr] == value] for value in set(item[attr] for item in leads)}
            self.assertEqual(segmented_leads, expected_segments)

if __name__ == '__main__':
    unittest.main()
