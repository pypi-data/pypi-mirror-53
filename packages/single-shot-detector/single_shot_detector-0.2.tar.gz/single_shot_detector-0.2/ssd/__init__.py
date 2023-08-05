from ssd_rg import train

def make_train(img_height, img_width, img_channels, n_classes, images_dir, train_labels_filepath, val_labels_filepath):  
    history = train_ssd_model(img_height, img_width, img_channels, n_classes, images_dir, train_labels_filepath, val_labels_filepath)
    return history