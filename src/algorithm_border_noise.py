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


def decibel_to_linear(image: ee.Image):
    """Convert backscatter from decibel to linear."""
    band_names = image.bandNames().remove("angle")
    linear = (
        image.constant(10.0)
        .pow(image.select(band_names).divide(10.0))
        .rename(band_names)
    )
    return image.addBands(linear, None, True)


def linear_to_decibel_without_ratio(image: ee.Image) -> ee.Image:
    """Convert backscatter from linear to decibel by removing the ratio band.
    Returns:
        ee.Image: converts backscatter to decibel.
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


def mask_angles_lt_45degrees(image: ee.Image) -> ee.Image:
    """
    Mask out angles less than equals 45.23993 degrees.
    """
    angle = image.select(["angle"])
    return image.updateMask(angle.lt(45.23993)).set(
        "system:time_start", image.get("system:time_start")
    )


def mask_angles_gt_30degrees(image: ee.Image) -> ee.Image:
    """mask out angles greater than 30 degrees

    Returns:
    ee.Image:
    """
    angle = image.select(["angle"])
    return image.updateMask(angle.gt(30.63993)).set(
        "system:time_start", image.get("system:time_start")
    )


def mask_border_noise_artefacts(image: ee.Image) -> ee.Image:
    output = decibel_to_linear(
        mask_angles_gt_30degrees(mask_angles_lt_45degrees(linear_to_decibel(image)))
    )
    return output.set("system:time_start", image.get("system:time_start"))
