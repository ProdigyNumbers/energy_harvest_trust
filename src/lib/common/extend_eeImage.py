import ee


class EnergyHarvestImage(ee.Image):
    def linear_to_decibel(self) -> ee.Image:
        """
        Convert linear reflectance to decibel reflectance.
        """
        band_names = self.bandNames().remove("angle")
        decibel = (
            ee.Image.constant(10.0)
            .multiply(self.select(band_names).log10())
            .rename(band_names)
        )
        return self.addBands(decibel, None, True)

    def linear_to_decibel_without_ratio(self) -> ee.Image:
        """Convert backscatter from linear to decibel by removing the ratio band.

        Returns:
            ee.Image: converts backscatter to decibel.
        """
        decibel = (
            ee.Image.constant(10.0)
            .multiply(self.select(["VV", "VH"]).log10())
            .rename(["VV", "VH"])
        )
        return self.addBands(decibel, None, True)

    def add_ratio_linear(self) -> ee.Image:
        """
        Add ratio band to image for visualization.
        """
        ratio = self.addBands(
            self.select("VV").divide(self.select("VH")).rename("VVVH_ratio")
        )
        return ratio.set("system:time_start", self.get("system:time_start"))

    def mask_angles_lt_45degrees(self) -> ee.Image:
        """
        Mask out angles less than equals 45.23993 degrees.
        """
        angle = self.select(["angle"])
        return self.updateMask(angle.lt(45.23993)).set(
            "system:time_start", self.get("system:time_start")
        )

    def mask_angles_gt_30degrees(self) -> ee.Image:
        """mask out angles greater than 30 degrees

        Returns:
            ee.Image:
        """
        angle = self.select(["angle"])
        return self.updateMask(angle.gt(30.63993)).set(
            "system:time_start", self.get("system:time_start")
        )

    def mask_border_noise_artefacts(self) -> ee.Image:
        output = (
            self.linear_to_decibel()
            .mask_angles_lt_45degrees()
            .mask_angles_gt_30degrees()
            .decibel_to_linear()
        )
        return output.set("system:time_start", self.get("system:time_start"))
