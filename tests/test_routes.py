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
        self.assertIn(b'=== INPUT FEATURES ===', response.data)
        self.assertIn(b'Physical Activity', response.data)
        self.assertNotIn(b'Frequent High-Calorie Food (FAVC)', response.data)

    @patch('src.predict.predict_advanced')
    def test_download_report_advanced_includes_advanced_features(self, mock_predict_advanced):
        mock_predict_advanced.return_value = {
            'class_label': 'Normal_Weight',
            'confidence': 94.1,
            'bmi': 22.1,
            'all_probs': {'Normal_Weight': 94.1},
            'status': 'success',
        }

        with patch.object(app_module, 'MODEL_EXISTS', True):
            response = self.client.post('/download-report', data={
                'mode': 'advanced',
                'age': '25',
                'gender': 'Male',
                'height': '175',
                'weight': '69',
                'physical_activity': 'Moderate',
                'family_history': 'No',
                'favc': 'yes',
                'fcvc': '2.0',
                'ncp': '3.0',
                'caec': 'Sometimes',
                'smoke': 'no',
                'ch2o': '2.0',
                'scc': 'yes',
                'tue': '1.0',
                'calc': 'no',
                'mtrans': 'Walking',
            })

        self.assertEqual(response.status_code, 200)
        self.assertIn('text/csv', response.content_type)
        self.assertIn(b'=== INPUT FEATURES ===', response.data)
        self.assertIn(b'Frequent High-Calorie Food (FAVC)', response.data)
        self.assertIn(b'Primary Transport (MTRANS)', response.data)
        self.assertIn(b'BMI', response.data)


if __name__ == '__main__':
    unittest.main()
