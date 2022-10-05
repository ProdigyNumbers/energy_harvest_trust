from black import out
import ee
from matplotlib import units
import math


class SpeckleFilter:
    def __init__(self, image, kernel_size) -> None:
        self.image = image
        self.kernel_size = kernel_size

    def boxcar_filtering(self):
        """
        Apply boxcar filter to image to reduce any measurement noise.
        """
        band_names = self.image.bandNames().remove("angle")
        kernel = ee.Kernel.square(
            (self.kernel_size / 2), units="pixels", normalize=True
        )
        filter_image = self.image.select(band_names).convolve(kernel).rename(band_names)
        return self.image.addBands(filter_image, None, True)

    def lee_filtering(self):
        """Lee filter used to reduce speckle in images while preserving texture.
        J. S. Lee, “Digital image enhancement and noise filtering by use of local statistics,”
        """
