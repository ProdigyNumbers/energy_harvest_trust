import ee


def linear_to_decibel(image: ee.Image) -> ee.Image:
    """
    Convert linear reflectance to decibel reflectance.
    """
    band_names = image.bandNames().remove("angle")
    decibel = (
        ee.Image.constant(10.0)
        .multiply(image.select(band_names).log10())
        .rename(band_names)
    )
    return image.addBands(decibel, None, True)


def linear_to_decibel_without_ratio(image: ee.Image) -> ee.Image:
    """
    Convert backscatter from linear to decibel by removing the ratio band.
    """
    decibel = (
        ee.Image.constant(10.0)
        .multiply(image.select(["VV", "VH"]).log10())
        .rename(["VV", "VH"])
    )
    return image.addBands(decibel, None, True)


def add_ratio_linear(image: ee.Image) -> ee.Image:
    """
    Add ratio band to image for visualization.
    """
    ratio = image.addBands(
        image.select("VV").divide(image.select("VH")).rename("VVVH_ratio")
    )
    return ratio.set("system:time_start", image.get("system:time_start"))
