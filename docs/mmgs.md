# MMGS operator

## Usage

If mmgs is installed on your system, an operator called "mmgs remesh" will be accessible from the "external tools" section of the ISCD panel:
<p align="center">
<img src="https://user-images.githubusercontent.com/11873158/28729061-5d2197da-73cb-11e7-84a4-896861dea480.png"/>
<h4 align="center">mmgs remesh button</h4>
</p>

You can use the weight paint mode and its built-in tools to paint a weight field on your object, which, if it exists, will be used by mmgs as a metric. Blue colors will correspond to zones with the lower edge length, while red colors will correspond to the higher edge length:
<p align="center">
<img src="https://user-images.githubusercontent.com/11873158/28729303-49be772a-73cc-11e7-8fa6-2562d2467231.png"/>
<h4 align="center">weight paint mode</h4>
</p>
<p align="center">
<img src="https://user-images.githubusercontent.com/11873158/28728852-89826350-73ca-11e7-81fb-9091ba32e444.png"/>
<h4 align="center">A painted mesh</h4>
</p>

While in object mode, you can launch this operator to use the mmgs tool, specifying parameters such as the minimum and maximum edge sizes, the hausdorff value and the gradation parameter.
If medit is installed on your system, the operator will give you a preview of the resulting mesh, before importing it if you unchecked the "Preview" checkbox.
When clicking on the "OK" button, mmgs will launch in the background, so depending on the size of your mesh the processing might take quite some time...
<p align="center">
<img src="https://user-images.githubusercontent.com/11873158/28729439-ba75de68-73cc-11e7-9661-7c475e6186e6.png"/>
<h4 align="center">Operator options</h4>
</p>

## Results

Here are screenshots of a fragment of a frisae of the roman theatre of Orange partly remeshed with the previous procedure:
<p align="center">
<img src="https://user-images.githubusercontent.com/11873158/28728860-8dd08338-73ca-11e7-9e45-ff6ad0c3d0cb.png"/>
<h4 align="center">Original fragment + painted metric</h4>
</p>
<p align="center">
<img src="https://user-images.githubusercontent.com/11873158/28728863-8feb0e0e-73ca-11e7-8d99-c6428f215da9.png"/>
<h4 align="center">Remeshed fragment + computed metric</h4>
</p>
