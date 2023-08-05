
import keras.backend as K
from keras.callbacks import Callback
import numpy as np

class WarmupCallback(Callback):

    def __init__(self, warmup_bs, num_warmup_epochs, len_train_img, len_valid_img, batch_size, num_patches, train_times, valid_times, early_stop_callback, modelcheckpoint, reduceonnplateau):
        self.warmup_bs = warmup_bs
        self.num_warmup_epochs = num_warmup_epochs
        self.len_train_img = len_train_img
        self.len_valid_img = len_valid_img
        self.num_patches = num_patches
        self.batch_size = batch_size
        self.train_times = train_times
        self.valid_times = valid_times
        self.early_stop_callback = early_stop_callback
        self.modelcheckpoint = modelcheckpoint
        self.reduceonnplateau = reduceonnplateau



    def on_epoch_end(self, epoch, logs={}):
        if epoch == self.num_warmup_epochs-1:
            if self.num_warmup_epochs > 0:
                print("###############")
                print("Warm up done.")
                print("###############")
            warmup_bs_help = 0.
            self.early_stop_callback.on_train_begin()
            self.reduceonnplateau.on_train_begin()
            self.modelcheckpoint.reset_best(np.Inf)
            K.set_value(self.warmup_bs, warmup_bs_help)
        elif epoch < self.num_warmup_epochs:
            warmup_bs_help = self.num_warmup_epochs * (
                    self.train_times * (self.len_train_img * self.num_patches * self.num_patches / self.batch_size + 1)
                    + self.valid_times
                    * (self.len_valid_img * self.num_patches * self.num_patches / self.batch_size + 1)
            )
            K.set_value(self.warmup_bs, warmup_bs_help)