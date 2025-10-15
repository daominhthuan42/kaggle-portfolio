from PIL import Image

# Mở ảnh
img = Image.open("C:/Users/Admin/Downloads/input.png").convert("RGBA")
datas = img.getdata()

# Chuyển màu nền trắng (255,255,255) thành trong suốt
new_data = []
for item in datas:
    if item[:3] == (255, 255, 255):
        new_data.append((255, 255, 255, 0))  # alpha = 0 => trong suốt
    else:
        new_data.append(item)

img.putdata(new_data)
img.save("C:/Users/Admin/Downloads/output.png", "PNG")
