"""TODO PEP 257"""
import numpy as np
import pandas as pd

from learning_machines_drift import FileBackend, Monitor, Registry, datasets

# Generate a reference dataset
X, Y, latents = datasets.logistic_model(
    x_mu=np.array([0.0, 0.0, 0.0]), size=100, return_latents=True
)

features_df = pd.DataFrame(
    {
        "age": X[:, 0],
        "height": X[:, 1],
        "bp": X[:, 2],
    }
)
labels_df = pd.DataFrame({"y": Y})
latents_df = pd.DataFrame({"latents": latents})

# Log our reference dataset
detector = Registry(tag="simple_example", backend=FileBackend("my-data"))
detector.register_ref_dataset(
    features=features_df, labels=labels_df, latents=latents_df
)


for i in range(3):
    # Generate drift data
    X_monitor, Y_monitor, latents_monitor = datasets.logistic_model(
        x_mu=np.array([0.0, 1.0, 0.0]), alpha=10, size=10, return_latents=True
    )

    features_monitor_df = pd.DataFrame(
        {
            "age": X_monitor[:, 0],
            "height": X_monitor[:, 1],
            "bp": X_monitor[:, 2],
        }
    )

    labels_monitor_df = pd.DataFrame({"y": Y_monitor})
    latents_monitor_df = pd.DataFrame({"latents": latents_monitor})

    # Log features
    with detector:
        detector.log_features(features_monitor_df)
        detector.log_labels(labels_monitor_df)
        detector.log_latents(latents_monitor_df)


measure = Monitor(tag="simple_example", backend=FileBackend("my-data"))
measure.load_data()
print(measure.hypothesis_tests.scipy_kolmogorov_smirnov())
print(measure.hypothesis_tests.scipy_permutation())
print(measure.hypothesis_tests.scipy_mannwhitneyu())
print(measure.hypothesis_tests.scipy_chisquare())
print(measure.hypothesis_tests.gaussian_mixture_log_likelihood())
print(measure.hypothesis_tests.gaussian_mixture_log_likelihood(normalize=True))
print(measure.hypothesis_tests.logistic_detection())
print(measure.hypothesis_tests.logistic_detection_custom())
print(measure.hypothesis_tests.logistic_detection_custom(score_type="f1"))
print(measure.hypothesis_tests.logistic_detection_custom(score_type="roc_auc"))
# print(measure.hypothesis_tests.sd_evaluate())


# logged_datasets = detector.backend.load_logged_dataset("simple_example")
# print(logged_datasets.labels)


# print(detector.registered_features)
# print(detector.registered_labels)
# print(detector.ref_dataset)
# print(measure.hypothesis_tests.kolmogorov_smirnov())
# print(measure.hypothesis_tests.sdv_evaluate())


# logged_datasets = detector.backend.load_logged_dataset("simple_example")

# print(logged_datasets.features)
# print(logged_datasets.labels)
