# Fingerprint-matching-project
A simple Python/CustomTkinter app that lets users upload a fingerprint image and performs matching against the SOCOFing dataset using SIFT feature descriptors.
It computes feature matches between the input and dataset images, applies Lowe’s ratio test with k‑nearest neighbors (KNN) to filter good matches, and displays the best match with accuracy and error rate.
KNN (k‑nearest neighbors) in this context retrieves the two closest feature descriptor matches and uses the ratio test to keep only strong correspondences.
The GUI shows the selected fingerprint, the closest matching fingerprint, and match statistics.
The dataset (SOCOFing) used for matching can be downloaded from Kaggle and placed in the specified dataset path for comparison.

For dataset download link -- https://www.kaggle.com/datasets/ruizgara/socofing
