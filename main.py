from PixelMaster import *

picture = PixelMaster(Image.open('doc/OriginalPicture.png'))
picture.drawSquarePicture(4).save('doc/SquarePicture.png')
picture.drawTriangularPicture(10).save('doc/TriangularPicture.png')
picture.drawCircularPicture(4).save('doc/CircularPicture.png')
picture.drawBlurredPicture(2).save('doc/BlurredPicture.png')
picture.drawEnhancePicture().save('doc/EnhancePicture.png')