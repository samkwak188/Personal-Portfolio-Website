from PIL import Image

img = Image.open("assets/profile.png")
w, h = img.size
side = min(w, h)
left = (w - side) // 2
upper = (h - side) // 2
right = left + side
lower = upper + side
img.crop((left, upper, right, lower)).save("assets/profile_cropped.jpg", quality=95)

