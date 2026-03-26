import unittest

from app import parse_prediction_form
from src.predict import validate_inputs, validate_model_bundle


class DummyForm(dict):
    def get(self, key, default=None):
        return super().get(key, default)


class ValidationTests(unittest.TestCase):
    def test_parse_prediction_form_valid(self):
        form = DummyForm({
            'age': '25',
            'gender': 'Male',
            'height': '175',
            'weight': '72',
            'physical_activity': 'Moderate',
            'family_history': 'Yes',
        })

        parsed = parse_prediction_form(form)
        self.assertEqual(parsed['age'], 25)
        self.assertEqual(parsed['gender'], 'Male')
        self.assertEqual(parsed['family_history'], 'Yes')

    def test_parse_prediction_form_invalid_age(self):
        form = DummyForm({'age': '120'})
        with self.assertRaises(ValueError):
            parse_prediction_form(form)

    def test_validate_inputs_normalizes_family_history(self):
        normalized = validate_inputs(
            age=30,
            gender='Female',
            height_cm=165,
            weight_kg=65,
            physical_activity='Active',
            family_history='Yes',
        )
        self.assertEqual(normalized['family_history'], 'yes')

    def test_validate_inputs_invalid_activity(self):
        with self.assertRaises(ValueError):
            validate_inputs(
                age=30,
                gender='Male',
                height_cm=175,
                weight_kg=80,
                physical_activity='Extreme',
                family_history='No',
            )

    def test_validate_model_bundle_accepts_required_keys(self):
        bundle = {
            'model': object(),
            'scaler': object(),
            'label_encoder': object(),
            'feature_encoders': {},
            'feature_cols': [],
            'metadata': {'schema_version': 1},
        }
        validate_model_bundle(bundle)

    def test_validate_model_bundle_rejects_missing_key(self):
        bundle = {
            'model': object(),
            'scaler': object(),
            'feature_encoders': {},
            'feature_cols': [],
        }
        with self.assertRaises(ValueError):
            validate_model_bundle(bundle)


if __name__ == '__main__':
    unittest.main()
