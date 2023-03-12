# Importe la classe PixelMaster du module PixelMaster
from PixelMaster import *

# Crée une instance de la classe PixelMaster à partir de l'image 'OriginalPicture.png'
picture = PixelMaster(Image.open('doc/OriginalPicture.png'))

# Dessine une image carrée à partir de l'image d'origine avec une taille de carré de 4 pixels
# et sauvegarde l'image sous le nom 'SquarePicture.png'
picture.drawSquarePicture(4).save('doc/SquarePicture.png')

# Dessine une image triangulaire à partir de l'image d'origine avec un nombre de niveaux de 10
# et sauvegarde l'image sous le nom 'TriangularPicture.png'
picture.drawTriangularPicture(10).save('doc/TriangularPicture.png')

# Dessine une image circulaire à partir de l'image d'origine avec un rayon de 4 pixels
# et sauvegarde l'image sous le nom 'CircularPicture.png'
picture.drawCircularPicture(4).save('doc/CircularPicture.png')

# Dessine une image floue à partir de l'image d'origine avec un rayon de flou de 2 pixels
# et sauvegarde l'image sous le nom 'BlurredPicture.png'
picture.drawBlurredPicture(2).save('doc/BlurredPicture.png')

# Dessine une image améliorée à partir de l'image d'origine en renforçant les couleurs des pixels
# et sauvegarde l'image sous le nom 'EnhancePicture.png'
picture.drawEnhancePicture().save('doc/EnhancePicture.png')