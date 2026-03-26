import unittest
from unittest.mock import patch

import app as app_module


class RouteTests(unittest.TestCase):
    def setUp(self):
        app_module.app.config['TESTING'] = True
        self.client = app_module.app.test_client()

    def test_predict_invalid_input_shows_validation_error(self):
        with patch.object(app_module, 'MODEL_EXISTS', True):
            response = self.client.post('/predict', data={
                'age': '300',
                'gender': 'Male',
                'height': '175',
                'weight': '72',
                'physical_activity': 'Moderate',
                'family_history': 'Yes',
            })

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid input values', response.data)

    def test_download_report_invalid_input_returns_500(self):
        with patch.object(app_module, 'MODEL_EXISTS', True):
            response = self.client.post('/download-report', data={
                'age': '25',
                'gender': 'Male',
                'height': '10',
                'weight': '72',
                'physical_activity': 'Moderate',
                'family_history': 'Yes',
            })

        self.assertEqual(response.status_code, 500)
        self.assertIn(b'Error generating report', response.data)

    @patch('src.predict.predict')
    def test_download_report_valid_returns_csv(self, mock_predict):
        mock_predict.return_value = {
            'class_label': 'Normal_Weight',
            'confidence': 95.2,
            'bmi': 22.5,
            'all_probs': {'Normal_Weight': 95.2},
            'status': 'success',
        }

        with patch.object(app_module, 'MODEL_EXISTS', True):
            response = self.client.post('/download-report', data={
                'age': '25',
                'gender': 'Male',
                'height': '175',
                'weight': '69',
                'physical_activity': 'Moderate',
                'family_history': 'No',
            })

        self.assertEqual(response.status_code, 200)
        self.assertIn('text/csv', response.content_type)
        self.assertIn('attachment; filename=', response.headers.get('Content-Disposition', ''))


if __name__ == '__main__':
    unittest.main()
