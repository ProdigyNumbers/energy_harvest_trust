# Work Packages : 

This document outlines the work packages as described in the paper:
- [High resolution paddy rice maps in cloud-prone Bangladesh and Northeast India using Sentinel-1 data](https://www.nature.com/articles/s41597-019-0036-3)

and gives the plan for implementing the various work packages using Google Earth Engine for the region of Punjab in India.

## Requirements: 

- Cloud free Synthetic Aperture Radar (SAR) images from Sentinel-1 satellite
- Random Forest Classifier
- Google Earth Engine cloud computing platform

## Resources:

- Three distinct rice growing seasons in South Asia:
  - Boro (December / January to April)
  - Aus (April / May to June / July)
  - Aman (July / August to November)
- Validation of generated rice maps is carried out by comparing with existing product from the International Rice Research Institute and Moderate Resolution Imaging Spectroradiometer (MODIS) data.
- [Asia Rice Crop Estimation and Monitoring](http://asia-rice.org/)
- [GEOGLAM, Global Agricultural Monitoring](https://www.earthobservations.org/geoglam.php)
- [International Rice Research Institute (IRRI)](https://www.irri.org/)

## Data:

### Sentinel-1 SAR data and pre-processing

- Sentinel-1 data is collected with several different instrument configurations, resolutions, band combinations during both ascending and descending orbits. Because of this heterogeneity, it's usually necessary to filter the data down to a homogenous subset before starting processing
- Filter the Sentinel-1 Image collection w.r.t. start and end date and the bounding box of the shape of Punjab.
- The SAR imagery is used and only the Interferometric Wide Swath (IW) mode is used since this mode avoids conflicts and preserves revisit performance, provide consistent long-term archives and designed to acquire imagery of land surfaces.
- The SAR imagery of IW mode is provided in dual-polarization with vertical transmit, vertical receive (VV) and vertical transmit, horizontal receive (VH)