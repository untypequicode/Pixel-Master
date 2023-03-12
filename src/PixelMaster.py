from PIL import Image
import math


class PixelMaster():

    def __init__(self, picture: Image):
        """
        Initialise une instance de PixelMaster avec l'image passée en argument.

        Args:
            picture (Image): une instance de la classe Image de la bibliothèque PIL
        """
        self.m_picture = picture

    def __getPictureSeparation(self, division_nb: int, proportional: bool = True) -> tuple[list, list, int, int]:
        """
        Divise l'image en sections carrées de taille égale, en fonction du nombre de divisions souhaitées et
        renvoie les coordonnées de chaque section ainsi que la largeur et la hauteur de l'image.

        Args:
            division_nb (int): Le nombre de sections carrées souhaitées pour diviser l'image.
            proportional (bool, optionnel): Si True, divise l'image de manière proportionnelle. Si False, divise
                l'image de sorte que la taille des sections soit la même quelle que soit la direction.
                Defaults to True.

        Returns:
            tuple[list, list, int, int]: Un tuple contenant deux listes d'entiers, représentant les coordonnées
            x et y de chaque section de l'image, ainsi que la largeur et la hauteur de l'image.
        """
        width, height = self.m_picture.size
        if proportional:
            nb_pixel_width = width//division_nb
            nb_pixel_height = height//division_nb
        else:
            if width <= height:
                nb_pixel_width, nb_pixel_height = width//division_nb, width//division_nb
            else:
                nb_pixel_width, nb_pixel_height = height//division_nb, height//division_nb
        width_list = []
        height_list = []

        width_index = 0
        while width >= nb_pixel_width * (width_index + 1):
            width_list.append(nb_pixel_width * width_index)
            width_list.append(nb_pixel_width*(width_index+1)-1)
            width_index += 1
        height_index = 0
        while height >= nb_pixel_height * (height_index + 1):
            height_list.append(nb_pixel_height * height_index)
            height_list.append(nb_pixel_height*(height_index+1)-1)
            height_index += 1
        if proportional:
            if width_list[-1] < width:
                width_list.append(nb_pixel_width*width_index)
                width_list.append(width)
            if height_list[-1] < height:
                height_list.append(nb_pixel_height*height_index)
                height_list.append(height)

        return width_list, height_list, width, height

    def __totalPixelColor(self, red_total: int, green_total: int, blue_total: int, nb_pixel: int, x: int, y: int, coef: int = 1, a: int = 0, b: int = 0, c: int = 0, d: int = 0) -> tuple[int, int, int, int]:
        """
        Calcule la somme des valeurs des composantes rouge, verte et bleue de tous les pixels dans une zone donnée.

        Args:
            red_total (int): La somme actuelle des valeurs de la composante rouge de tous les pixels dans la zone.
            green_total (int): La somme actuelle des valeurs de la composante verte de tous les pixels dans la zone.
            blue_total (int): La somme actuelle des valeurs de la composante bleue de tous les pixels dans la zone.
            nb_pixel (int): Le nombre actuel de pixels dans la zone.
            x (int): La coordonnée x du pixel courant dans la zone.
            y (int): La coordonnée y du pixel courant dans la zone.
            coef (int, optional): Le coefficient de zoom appliqué à la zone. Par défaut, 1.
            a (int, optional): La coordonnée de début en x de la zone de zoom. Par défaut, 0.
            b (int, optional): La coordonnée de fin en x de la zone de zoom. Par défaut, 0.
            c (int, optional): La coordonnée de début en y de la zone de zoom. Par défaut, 0.
            d (int, optional): La coordonnée de fin en y de la zone de zoom. Par défaut, 0.

        Returns:
            tuple[int, int, int, int]: Un tuple contenant la nouvelle somme des valeurs de la composante rouge, 
            la nouvelle somme des valeurs de la composante verte, la nouvelle somme des valeurs de la composante bleue 
            et le nouveau nombre de pixels dans la zone.

        Raises:
            None
        """
        if a <= b and c <= d:
            red, green, blue = self.m_picture.getpixel((x, y))
            red_total += red*coef
            green_total += green*coef
            blue_total += blue*coef
            if coef == 1:
                nb_pixel += 1
            else:
                nb_pixel += 1 + coef
        return red_total, green_total, blue_total, nb_pixel

    def __averagePixelColor(self, red_total: int, green_total: int, blue_total: int, nb_pixel: int) -> tuple[int, int, int]:
        """
        Calcule la couleur moyenne d'un ensemble de pixels.

        Args:
            red_total (int): somme de la composante rouge de chaque pixel
            green_total (int): somme de la composante verte de chaque pixel
            blue_total (int): somme de la composante bleue de chaque pixel
            nb_pixel (int): nombre total de pixels considérés

        Returns:
            tuple[int, int, int]: une tuple contenant les valeurs moyennes des composantes rouge, verte et bleue respectivement.

        Raises:
            Aucune exception n'est levée.
        """
        if nb_pixel == 0:
            return 0, 0, 0
        else:
            red_avg = red_total // nb_pixel
            green_avg = green_total // nb_pixel
            blue_avg = blue_total // nb_pixel
            return red_avg, green_avg, blue_avg

    def drawTriangularPicture(self, division_nb: int) -> Image:
        """
        Génère une image pixelisée en forme de triangles.

        Args:
            division_nb (int): Le nombre de divisions de l'image.

        Returns:
            Image: L'image pixelisée en forme de triangles.
        """
        width_list, height_list, width, height = self.__getPictureSeparation(
            division_nb)
        pixelated_picture = Image.new('RGB', (width, height))
        index_x = 0
        for i in range(len(width_list)//2):
            index_y = 0
            for i in range(len(height_list)//2):
                start_x = width_list[index_x]
                start_y = height_list[index_y]
                end_x = width_list[index_x+1]
                end_y = height_list[index_y+1]
                red_t_total, green_t_total, blue_t_total, px_triangle_t = 0, 0, 0, 0
                red_l_total, green_l_total, blue_l_total, px_triangle_l = 0, 0, 0, 0
                red_r_total, green_r_total, blue_r_total, px_triangle_r = 0, 0, 0, 0
                red_d_total, green_d_total, blue_d_total, px_triangle_d = 0, 0, 0, 0
                if end_y - start_y != 0:
                    ratio = (end_x - start_x) / (end_y - start_y)
                else:
                    ratio = 1
                for x in range(start_x - 1, end_x):
                    for y in range(start_y-1, end_y):
                        red_t_total, green_t_total, blue_t_total, px_triangle_t = self.__totalPixelColor(
                            red_t_total, green_t_total, blue_t_total, px_triangle_t, x, y, 1, (y-start_y)*ratio, (x-start_x), (y-start_y)*ratio, (end_x-x))
                        red_l_total, green_l_total, blue_l_total, px_triangle_l = self.__totalPixelColor(
                            red_l_total, green_l_total, blue_l_total, px_triangle_l, x, y, 1, (x-start_x), (y-start_y)*ratio, (y-start_y)*ratio, (end_x-x))
                        red_r_total, green_r_total, blue_r_total, px_triangle_r = self.__totalPixelColor(
                            red_r_total, green_r_total, blue_r_total, px_triangle_r, x, y, 1, (y-start_y)*ratio, (x-start_x), (end_x-x), (y-start_y)*ratio)
                        red_d_total, green_d_total, blue_d_total, px_triangle_d = self.__totalPixelColor(
                            red_d_total, green_d_total, blue_d_total, px_triangle_d, x, y, 1, (x-start_x), (y-start_y)*ratio, (end_x-x), (y-start_y)*ratio)

                red_t_avg, green_t_avg, blue_t_avg = self.__averagePixelColor(
                    red_t_total, green_t_total, blue_t_total, px_triangle_t)
                red_l_avg, green_l_avg, blue_l_avg = self.__averagePixelColor(
                    red_l_total, green_l_total, blue_l_total, px_triangle_l)
                red_r_avg, green_r_avg, blue_r_avg = self.__averagePixelColor(
                    red_r_total, green_r_total, blue_r_total, px_triangle_r)
                red_d_avg, green_d_avg, blue_d_avg = self.__averagePixelColor(
                    red_d_total, green_d_total, blue_d_total, px_triangle_d)

                for x in range(start_x - 1, end_x):
                    for y in range(start_y-1, end_y):
                        if (x-start_x) >= (y-start_y)*ratio and (end_x-x) >= (y-start_y)*ratio:
                            pixelated_picture.putpixel(
                                (x, y), (red_t_avg, green_t_avg, blue_t_avg))
                        elif (x-start_x) <= (y-start_y)*ratio and (end_x-x) >= (y-start_y)*ratio:
                            pixelated_picture.putpixel(
                                (x, y), (red_l_avg, green_l_avg, blue_l_avg))
                        elif (x-start_x) >= (y-start_y)*ratio and (end_x-x) <= (y-start_y)*ratio:
                            pixelated_picture.putpixel(
                                (x, y), (red_r_avg, green_r_avg, blue_r_avg))
                        elif (x-start_x) <= (y-start_y)*ratio and (end_x-x) <= (y-start_y)*ratio:
                            pixelated_picture.putpixel(
                                (x, y), (red_d_avg, green_d_avg, blue_d_avg))
                index_y += 2
            index_x += 2
        return pixelated_picture

    def drawCircularPicture(self, division_nb: int) -> Image:
        """
        Dessine une image circulaire divisée en plusieurs sections, chaque section étant remplie avec la même couleur moyenne
        de pixels.

        Args:
            division_nb (int): Le nombre de divisions de l'image circulaire. Plus la valeur est grande, plus l'image aura de 
            sections.

        Returns:
            Image: L'image dessinée.

        """
        # Obtenir les coordonnées de séparation de chaque section de l'image
        width_list, height_list, width, height = self.__getPictureSeparation(
            division_nb, False)
        # Créer une nouvelle image pixelisée avec la taille de l'image d'origine
        pixelated_picture = Image.new('RGB', (width, height))
        index_x = 0
        # Parcourir chaque section horizontale de l'image
        for i in range(len(width_list)//2):
            index_y = 0
            # Parcourir chaque section verticale de l'image
            for i in range(len(height_list)//2):
                # Obtenir les coordonnées de début et de fin de la section actuelle
                start_x = width_list[index_x]
                start_y = height_list[index_y]
                end_x = width_list[index_x+1]
                end_y = height_list[index_y+1]
                width_pixel = end_x - start_x
                height_pix = end_y - start_y
                x_loc_zone = (width_pixel + 1) // 2
                y_loc_zone = (height_pix + 1) // 2
                x_loc = start_x + x_loc_zone
                y_loc = start_y + y_loc_zone
                # Calculer la couleur moyenne de pixels de la section actuelle
                red_total, green_total, blue_total, px_circle = 0, 0, 0, 0
                for x in range(start_x - 1, end_x):
                    for y in range(start_y-1, end_y):
                        red_total, green_total, blue_total, px_circle = self.__totalPixelColor(
                            red_total, green_total, blue_total, px_circle, x, y)
                red_avg, green_avg, blue_avg = self.__averagePixelColor(
                    red_total, green_total, blue_total, px_circle)
                # Dessiner un cercle rempli de la couleur moyenne dans la section actuelle
                for i_width in range(x_loc_zone):
                    for x in range(i_width):
                        # Calculer la position en y du pixel à dessiner en fonction de sa position en x
                        if i_width > 0:
                            y = int((math.sqrt(1-(x/i_width)**2))*i_width)
                        else:
                            y = 0
                        # Dessiner les pixels dans les quatre quarts du cercle
                        pixelated_picture.putpixel(
                            (x+x_loc, y+y_loc), (red_avg, green_avg, blue_avg))
                        pixelated_picture.putpixel(
                            (x+x_loc, y_loc-y), (red_avg, green_avg, blue_avg))
                        pixelated_picture.putpixel(
                            (x_loc-x, y+y_loc), (red_avg, green_avg, blue_avg))
                        pixelated_picture.putpixel(
                            (x_loc-x, y_loc-y), (red_avg, green_avg, blue_avg))
                for i_height in range(y_loc_zone):
                    for y in range(i_height):
                        # Calculer la position en x du prochain cercle en fonction de sa position en y
                        if i_height > 0:
                            x = int((math.sqrt(1-(y/i_height)**2))*i_height)
                        else:
                            x = 0
                        pixelated_picture.putpixel(
                            (x+x_loc, y+y_loc), (red_avg, green_avg, blue_avg))
                        pixelated_picture.putpixel(
                            (x+x_loc, y_loc-y), (red_avg, green_avg, blue_avg))
                        pixelated_picture.putpixel(
                            (x_loc-x, y+y_loc), (red_avg, green_avg, blue_avg))
                        pixelated_picture.putpixel(
                            (x_loc-x, y_loc-y), (red_avg, green_avg, blue_avg))
                index_y += 2
            index_x += 2
        return pixelated_picture

    def drawSquarePicture(self, division_nb: int) -> Image:
        """
        Crée une nouvelle image en utilisant des carrés de pixels pour réduire la résolution de l'image.

        Args:
            division_nb (int): Le nombre de divisions à effectuer sur l'image.

        Returns:
            Image: L'image réduite créée en utilisant des carrés de pixels.
        """
        width_list, height_list, width, height = self.__getPictureSeparation(
            division_nb)
        pixelated_picture = Image.new('RGB', (width, height))
        index_x = 0
        for i in range(len(width_list)//2):
            index_y = 0
            for i in range(len(height_list)//2):
                start_x = width_list[index_x]
                start_y = height_list[index_y]
                end_x = width_list[index_x+1]
                end_y = height_list[index_y+1]
                red_total, green_total, blue_total, px_square = 0, 0, 0, 0
                for x in range(start_x - 1, end_x):
                    for y in range(start_y-1, end_y):
                        red_total, green_total, blue_total, px_square = self.__totalPixelColor(
                            red_total, green_total, blue_total, px_square, x, y)
                red_avg, green_avg, blue_avg = self.__averagePixelColor(
                    red_total, green_total, blue_total, px_square)
                for x in range(start_x - 1, end_x):
                    for y in range(start_y-1, end_y):
                        pixelated_picture.putpixel(
                            (x, y), (red_avg, green_avg, blue_avg))
                index_y += 2
            index_x += 2
        return pixelated_picture

    def drawBlurredPicture(self, blur_nb: int) -> Image:
        """
        Cette fonction floute une image.

        Args:
            blur_nb (int): Le nombre de pixels à prendre en compte pour le flou.

        Returns:
            Image : L'image floutée.

        """
        width, height = self.m_picture.size
        pixelated_picture = Image.new('RGB', (width, height))
        for x in range(width):
            for y in range(height):
                red_total, green_total, blue_total, px_blur = 0, 0, 0, 0
                for i in range(1, blur_nb+1):
                    if x-1 >= 0:
                        red_total, green_total, blue_total, px_blur = self.__totalPixelColor(
                            red_total, green_total, blue_total, px_blur, x-i, y)
                    if x+i < width:
                        red_total, green_total, blue_total, px_blur = self.__totalPixelColor(
                            red_total, green_total, blue_total, px_blur, x+i, y)
                    if y-i >= 0:
                        red_total, green_total, blue_total, px_blur = self.__totalPixelColor(
                            red_total, green_total, blue_total, px_blur, x, y-i)
                    if y+i < height:
                        red_total, green_total, blue_total, px_blur = self.__totalPixelColor(
                            red_total, green_total, blue_total, px_blur, x, y+i)
                for x_ref in range(blur_nb):
                    y_ref = int((math.sqrt(1-(x_ref/blur_nb)**2))*blur_nb)
                    coef = (math.sqrt(x_ref**2+y_ref**2))
                    if x - x_ref >= 0 and y - y_ref >= 0:
                        red_total, green_total, blue_total, px_blur = self.__totalPixelColor(
                            red_total, green_total, blue_total, px_blur, x-x_ref, y-y_ref, coef)
                    if x + x_ref < width and y + y_ref < height:
                        red_total, green_total, blue_total, px_blur = self.__totalPixelColor(
                            red_total, green_total, blue_total, px_blur, x+x_ref, y+y_ref, coef)
                    if y - y_ref >= 0 and x + x_ref < width:
                        red_total, green_total, blue_total, px_blur = self.__totalPixelColor(
                            red_total, green_total, blue_total, px_blur, x+x_ref, y-y_ref, coef)
                    if x - x_ref >= 0 and y + y_ref < height:
                        red_total, green_total, blue_total, px_blur = self.__totalPixelColor(
                            red_total, green_total, blue_total, px_blur, x-x_ref, y+y_ref, coef)
                red_avg, green_avg, blue_avg = self.__averagePixelColor(
                    red_total, green_total, blue_total, px_blur)
                pixelated_picture.putpixel(
                    (x, y), (int(red_avg), int(green_avg), int(blue_avg)))
        return pixelated_picture

    def __even(self, numbre: int) -> bool:
        """
        Vérifie si un nombre est pair.

        Args:
            numbre (int): Le nombre à vérifier.

        Returns:
            bool: True si le nombre est pair, False sinon.
        """
        return numbre / 2 == numbre // 2

    def __totalPixelColorEnhanceInner(self, enhance_picture: Image, nb_pixel, red_total, green_total, blue_total, x, y) -> tuple[int, int, int, int]:
        """
        Cette méthode calcule la somme des valeurs de rouge, vert et bleu des pixels voisins du pixel de coordonnées (x, y) sur l'image d'amélioration.

        Args:
            enhance_picture (Image): L'image d'amélioration sur laquelle on veut appliquer l'effet de flou.
            nb_pixel (int): Le nombre de pixels voisins déjà considérés.
            red_total (int): La somme des valeurs de rouge des pixels voisins déjà considérés.
            green_total (int): La somme des valeurs de vert des pixels voisins déjà considérés.
            blue_total (int): La somme des valeurs de bleu des pixels voisins déjà considérés.
            x (int): La coordonnée x du pixel central pour lequel on veut calculer la somme des couleurs de ses voisins.
            y (int): La coordonnée y du pixel central pour lequel on veut calculer la somme des couleurs de ses voisins.

        Returns:
            tuple[int, int, int, int]: Un tuple contenant la somme des valeurs de rouge, vert et bleu des pixels voisins et le nombre total de pixels voisins considérés.
        """
        width, height = enhance_picture.size
        if not (x < 0 or y < 0 or x > width-1 or y > height-1):
            r, g, b = enhance_picture.getpixel((x, y))
            red_total += r
            green_total += g
            blue_total += b
            nb_pixel += 1
        return red_total, green_total, blue_total, nb_pixel

    def __totalPixelColorEnhance(self, enhance_picture: Image, x, y) -> tuple[int, int, int, int]:
        """
        Retourne un tuple contenant la somme des valeurs de rouge, de vert, de bleu et du nombre de pixels pour les pixels voisins.

        :param enhance_picture: Une instance de la classe Image représentant l'image.
        :type enhance_picture: Image
        :param x: La position x du pixel.
        :type x: int
        :param y: La position y du pixel.
        :type y: int
        :return: Un tuple contenant la somme des valeurs de rouge, de vert, de bleu et du nombre de pixels.
        :rtype: tuple[int, int, int, int]
        """
        red_total, green_total, blue_total, px_blur = 0, 0, 0, 0
        if not self.__even(x) and self.__even(y):
            red_total, green_total, blue_total, px_blur = self.__totalPixelColorEnhanceInner(
                enhance_picture, px_blur, red_total, green_total, blue_total, x-1, y)
            red_total, green_total, blue_total, px_blur = self.__totalPixelColorEnhanceInner(
                enhance_picture, px_blur, red_total, green_total, blue_total, x+1, y)
        if not self.__even(y) and self.__even(x):
            red_total, green_total, blue_total, px_blur = self.__totalPixelColorEnhanceInner(
                enhance_picture, px_blur, red_total, green_total, blue_total, x, y-1)
            red_total, green_total, blue_total, px_blur = self.__totalPixelColorEnhanceInner(
                enhance_picture, px_blur, red_total, green_total, blue_total, x, y+1)
        elif not self.__even(x) and not self.__even(y):
            red_total, green_total, blue_total, px_blur = self.__totalPixelColorEnhanceInner(
                enhance_picture, px_blur, red_total, green_total, blue_total, x-1, y-1)
            red_total, green_total, blue_total, px_blur = self.__totalPixelColorEnhanceInner(
                enhance_picture, px_blur, red_total, green_total, blue_total, x-1, y+1)
            red_total, green_total, blue_total, px_blur = self.__totalPixelColorEnhanceInner(
                enhance_picture, px_blur, red_total, green_total, blue_total, x+1, y-1)
            red_total, green_total, blue_total, px_blur = self.__totalPixelColorEnhanceInner(
                enhance_picture, px_blur, red_total, green_total, blue_total, x+1, y+1)
        return red_total, green_total, blue_total, px_blur

    def __averagePixelColorEnhance(self, red_total, green_total, blue_total, nb_pixel) -> tuple[int, int, int]:
        """
        Calcule la couleur moyenne d'un ensemble de pixels.

        Args:
            red_total (int): somme des valeurs de rouge des pixels
            green_total (int): somme des valeurs de vert des pixels
            blue_total (int): somme des valeurs de bleu des pixels
            nb_pixel (int): nombre de pixels dans l'ensemble

        Returns:
            tuple[int, int, int]: la couleur moyenne sous forme de tuple (rouge, vert, bleu)
        """
        nb_pixel = nb_pixel // 2
        if nb_pixel > 0:
            r = red_total//nb_pixel
            g = green_total//nb_pixel
            b = blue_total//nb_pixel
            return r, g, b
        return 0, 0, 0

    def drawEnhancePicture(self) -> Image:
        """
        Crée une nouvelle image améliorée en appliquant une technique de flou.
        Cette technique consiste à prendre quatre pixels voisins et à remplacer le pixel central par une couleur moyenne pondérée.

        Returns:
            Image: l'image améliorée
        """
        width, height = self.m_picture.size
        enhance_picture = Image.new('RGB', (width*2, height*2))
        new_width, new_height = enhance_picture.size
        for x in range(new_width):
            for y in range(new_height):
                if self.__even(x) and self.__even(y):
                    r, g, b = self.m_picture.getpixel((x/2, y/2))
                    enhance_picture.putpixel((x, y), (r, g, b))
                else:
                    red_total, green_total, blue_total, px_blur = self.__totalPixelColorEnhance(
                        enhance_picture, x, y)
                    red_avg, green_avg, blue_avg = self.__averagePixelColorEnhance(
                        red_total, green_total, blue_total, px_blur)
                    enhance_picture.putpixel(
                        (x, y), (red_avg, green_avg, blue_avg))
        return enhance_picture
