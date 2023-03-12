# Pixel Master

PixelMaster is a Python library for creating modified images from an original image. This library uses the Python Imaging Library (PIL) to process images.

## Installation

To install PixelMaster, simply clone this GitHub repository.

## Usage

To use PixelMaster, you first need to import the PixelMaster class from the PixelMaster module:

``` python
from PixelMaster import PixelMaster
```

Then, you can create an instance of the PixelMaster class from an original image:

``` python
picture = PixelMaster(Image.open('OriginalPicture.png'))
```

Now, you can create a modified image from the original image using the different available methods, such as drawing a square, triangular, or circular image, blurring the image, or enhancing the colors of the pixels.

For example, to draw a square image from the original image with a square size of 4 pixels and save the image as 'SquarePicture.png', you can use the drawSquarePicture() method:

``` python
picture.drawSquarePicture(4).save('SquarePicture.png')
```

Similarly, you can use the ```drawTriangularPicture()```, ```drawCircularPicture()```, ```drawBlurredPicture()```, and ```drawEnhancePicture()``` methods to create other types of modified images.

## Examples

Examples of using PixelMaster are available in the 'examples' folder. You can run them to see how to use the different PixelMaster methods.

<p align="center">
  <img src="doc/img/PixelMaster.gif" alt="PixelMaster" width=75%"/>
</p>

## Authors

PixelMaster was created by [@untypequicode](https://github.com/untypequicode)
