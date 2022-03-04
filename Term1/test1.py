import PIL.Image as Image
im = Image.open('/Users/ihyeonjun/Documents/python_task/Term1/Image/7f2d8674-9ac0-11ec-8434-b8e85641a9861.png')
size = (128, 128)
im.thumbnail(size)
im.save("Term1/search/test_th.jpeg")