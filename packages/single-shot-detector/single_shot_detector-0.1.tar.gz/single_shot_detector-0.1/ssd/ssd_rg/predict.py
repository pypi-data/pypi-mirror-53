from keras import backend as K
from keras.models import load_model
from keras.preprocessing import image
from keras.optimizers import Adam
from imageio import imread
import numpy as np
from matplotlib import pyplot as plt

from ssd_keras.keras_loss_function.keras_ssd_loss import SSDLoss
from ssd_keras.keras_layers.keras_layer_AnchorBoxes import AnchorBoxes
from ssd_keras.keras_layers.keras_layer_DecodeDetections import DecodeDetections
from ssd_keras.keras_layers.keras_layer_DecodeDetectionsFast import DecodeDetectionsFast
from ssd_keras.keras_layers.keras_layer_L2Normalization import L2Normalization

from ssd_keras.ssd_encoder_decoder.ssd_output_decoder import decode_detections, decode_detections_fast

from ssd_keras.data_generator.object_detection_2d_data_generator import DataGenerator
from ssd_keras.data_generator.object_detection_2d_photometric_ops import ConvertTo3Channels
from ssd_keras.data_generator.object_detection_2d_geometric_ops import Resize
from ssd_keras.data_generator.object_detection_2d_misc_utils import apply_inverse_transforms


def predict_img(model_path, image):
    K.clear_session()

    # We need to create an SSDLoss object in order to pass that to the model loader.
    ssd_loss = SSDLoss(neg_pos_ratio=3, n_neg_min=0, alpha=1.0)

    model = load_model("ssd7_epoch-07_loss-0.7073_val_loss-0.4394.h5",custom_objects={'AnchorBoxes': AnchorBoxes,
                                                   'L2Normalization': L2Normalization,
                                                   'DecodeDetections': DecodeDetections,
                                                   'compute_loss': ssd_loss.compute_loss} )

    imgs = np.expand_dims(img, axis=0)

    y_pred = model.predict(imgs)


    y_pred_decoded = decode_detections(y_pred,
                                       confidence_thresh=0.5,
                                       iou_threshold=0.45,
                                       top_k=200,
                                       normalize_coords=True,
                                       img_height=300,
                                       img_width=300)

    np.set_printoptions(precision=2, suppress=True, linewidth=90)

    print("Predicted boxes:\n")
    print('   class   conf xmin   ymin   xmax   ymax')
    print(y_pred_decoded)

    return(y_pred_decoded)
