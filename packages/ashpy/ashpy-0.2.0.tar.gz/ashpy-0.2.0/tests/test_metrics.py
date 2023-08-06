# Copyright 2019 Zuru Tech HK Limited. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test Metrics
"""
import json
import os

from ashpy.metrics import InceptionScore, SlicedWassersteinDistance, SSIM_Multiscale
from ashpy.models.gans import ConvDiscriminator
from tests.utils.fake_training_loop import fake_training_loop


def test_metrics(adversarial_logdir: str):
    """
    Test the integration between metrics and trainer
    """
    # test parameters
    image_resolution = (256, 256)

    metrics = [
        SlicedWassersteinDistance(
            logdir=adversarial_logdir, resolution=image_resolution[0]
        ),
        SSIM_Multiscale(logdir=adversarial_logdir),
        InceptionScore(
            # Fake inception model
            ConvDiscriminator(
                layer_spec_input_res=(299, 299),
                layer_spec_target_res=(7, 7),
                kernel_size=(5, 5),
                initial_filters=16,
                filters_cap=32,
                output_shape=10,
            ),
            logdir=adversarial_logdir,
        ),
    ]

    fake_training_loop(
        adversarial_logdir,
        metrics=metrics,
        image_resolution=image_resolution,
        layer_spec_input_res=(8, 8),
        layer_spec_target_res=(8, 8),
        channels=3,
    )

    # assert there exists folder for each metric
    for metric in metrics:
        metric_dir = os.path.join(adversarial_logdir, "best", metric.name)
        assert os.path.exists(metric_dir)
        json_path = os.path.join(metric_dir, f"{metric.name}.json")
        assert os.path.exists(json_path)
        with open(json_path, "r") as fp:
            metric_data = json.load(fp)

            # assert the metric data contains the expected keys
            assert metric.name in metric_data
            assert "step" in metric_data
