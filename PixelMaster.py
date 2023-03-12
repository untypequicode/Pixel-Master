from PIL import Image
import requests
from io import BytesIO
import math
# import matplotlib.pyplot as plt


class PixelMaster():

    def __init__(self, picture: Image):
        self.m_picture = picture

    def __getPictureSeparation(self, division_nb: int, proportional: bool = True) -> tuple[list, list, int, int]:
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
        if nb_pixel == 0:
            return 0, 0, 0
        else:
            red_avg = red_total // nb_pixel
            green_avg = green_total // nb_pixel
            blue_avg = blue_total // nb_pixel
            return red_avg, green_avg, blue_avg

    def drawTriangularPicture(self, division_nb: int) -> Image:
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
        width_list, height_list, width, height = self.__getPictureSeparation(
            division_nb, False)
        pixelated_picture = Image.new('RGB', (width, height))
        index_x = 0
        for i in range(len(width_list)//2):
            index_y = 0
            for i in range(len(height_list)//2):
                start_x = width_list[index_x]
                start_y = height_list[index_y]
                end_x = width_list[index_x+1]
                end_y = height_list[index_y+1]
                red_total, green_total, blue_total, px_circle = 0, 0, 0, 0
                width_pixel = end_x - start_x
                height_pix = end_y - start_y
                x_loc_zone = (width_pixel + 1) // 2
                y_loc_zone = (height_pix + 1) // 2
                x_loc = start_x + x_loc_zone
                y_loc = start_y + y_loc_zone
                for x in range(start_x - 1, end_x):
                    for y in range(start_y-1, end_y):
                        red_total, green_total, blue_total, px_circle = self.__totalPixelColor(
                            red_total, green_total, blue_total, px_circle, x, y)
                red_avg, green_avg, blue_avg = self.__averagePixelColor(
                    red_total, green_total, blue_total, px_circle)
                for i_width in range(x_loc_zone):
                    for x in range(i_width):
                        if i_width > 0:
                            y = int((math.sqrt(1-(x/i_width)**2))*i_width)
                        else:
                            y = 0
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
        return numbre / 2 == numbre // 2

    def __totalPixelColorEnhanceInner(self, enhance_picture: Image, nb_pixel, red_total, green_total, blue_total, x, y) -> tuple[int, int, int, int]:
        width, height = enhance_picture.size
        if not (x < 0 or y < 0 or x > width-1 or y > height-1):
            r, g, b = enhance_picture.getpixel((x, y))
            red_total += r
            green_total += g
            blue_total += b
            nb_pixel += 1
        return red_total, green_total, blue_total, nb_pixel

    def __totalPixelColorEnhance(self, enhance_picture: Image, x, y) -> tuple[int, int, int, int]:
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
        nb_pixel = nb_pixel // 2
        if nb_pixel > 0:
            r = red_total//nb_pixel
            g = green_total//nb_pixel
            b = blue_total//nb_pixel
            return r, g, b
        return 0, 0, 0

    def drawEnhancePicture(self) -> Image:
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
