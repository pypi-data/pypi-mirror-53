import unittest

from automl.client.core.common.exceptions import ConfigException
from azureml.automl.core.featurization.featurizationconfig import FeaturizationConfig
from azureml.automl.core.constants import SupportedTransformers, FeatureType


class TestFeaturizationConfig(unittest.TestCase):
    def test_initialize_by_param(self):
        column_purposes = {'column1': FeatureType.Numeric,
                           'column2': FeatureType.Categorical,
                           'column3': FeatureType.Numeric}
        transformer_param = {'Imputer': [(['column1', 'column2'], {"strategy": "median"}),
                                         (['column3'], {"strategy": "mean"})]}
        blocked_transformers = [SupportedTransformers.CatTargetEncoder]

        config = FeaturizationConfig(column_purposes=column_purposes,
                                     transformer_params=transformer_param,
                                     blocked_transformers=blocked_transformers)

        self.assertEqual(config.column_purposes, column_purposes)
        self.assertEqual(config.transformer_params, transformer_param)
        self.assertEqual(config.blocked_transformers, blocked_transformers)

    def test_column_purpose(self):
        config = FeaturizationConfig()
        column_purposes = {'column1': FeatureType.Numeric, 'column2': FeatureType.Categorical}
        config.set_column_purpose('column1', FeatureType.Numeric)
        config.set_column_purpose('column2', FeatureType.Categorical)

        self.assertEqual(config.column_purposes, column_purposes)

        config.remove_column_purpose('column1')
        column_purposes.pop('column1')
        self.assertEqual(config.column_purposes, column_purposes)

        with self.assertRaises(ConfigException):
            config.set_column_purpose('column1', 'SomeFeature')

    def test_transformer_param(self):
        config = FeaturizationConfig()
        transformer_params = {
            SupportedTransformers.Imputer: [
                (['column1', 'column2'], {"strategy": "median"}),
                (['column3'], {"strategy": "mean"})
            ]
        }
        config.customize_transformer_params(SupportedTransformers.Imputer,
                                            ['column1', 'column2'],
                                            {"strategy": "median"})
        config.customize_transformer_params(SupportedTransformers.Imputer,
                                            ['column3'],
                                            {"strategy": "mean"})
        self.assertEqual(config.transformer_params, transformer_params)

        config.remove_customized_transformer_params(SupportedTransformers.Imputer)
        self.assertTrue(len(config.transformer_params) == 0)

        with self.assertRaises(ConfigException):
            config.customize_transformer_params('TestTransformer', ['column1', 'column2'], {"strategy": "median"})

    def test_blocked_transformers(self):
        config = FeaturizationConfig()
        self.assertEqual(config.blocked_transformers, None)
        blocked_transformers = [SupportedTransformers.TfIdf, SupportedTransformers.WoETargetEncoder]
        config.set_blocked_transformers(blocked_transformers)
        self.assertEqual(config.blocked_transformers, blocked_transformers)

        blocked_transformers.append(SupportedTransformers.CatTargetEncoder)
        config.add_blocked_transformers(blocked_transformers)
        self.assertEqual(config.blocked_transformers, blocked_transformers)

        config = FeaturizationConfig()
        blocked_transformers = [SupportedTransformers.CatTargetEncoder]
        config.add_blocked_transformers(SupportedTransformers.CatTargetEncoder)
        self.assertEqual(config.blocked_transformers, blocked_transformers)


if __name__ == "__main__":
    unittest.main()
