# import libraries from python
import glob
import os
import shutil

# import library from Pillow
from PIL import Image, ImageOps, ImageEnhance, ImageDraw, ImageFont

# make a new class
class Digitizer:
  def __init__(self, filepath):
    # initialize a new object with a filepath
    self.filepath = filepath
    self.img = Image.open(filepath).convert("RGBA")

  def adjust_contrast(self, amount=1.5):
    enhancer = ImageEnhance.Contrast(self.img)
    self.img = enhancer.enhance(amount)

  def make_grayscale(self):
    self.img = ImageOps.grayscale(self.img)
    self.img = self.img.convert("RGBA")

  def make_upside_down(self):
    print("make upside down!!!")
    self.img = self.img.rotate(180)

  def make_thumbnail_size(self, size=(128, 128)):
    self.img.thumbnail(size)

  def make_square(self, size=200):
    print("make it a square")

    # get the width and height
    (w, h) = self.img.size 

    # if portrait
    if w > h:
      # find the diff between width and height
      # then account for cutting off half on left
      # and half on right
      x = (w - h) * 0.5
      y = 0
      box = (x, y, h + x, h + y)
    else:
      # find the diff between height and width
      # then account for cutting off half on top
      # and half on bottom
      x = 0
      y = (h - w) * 0.5
      box = (x, y, x + w, y + w)

    self.img = self.img.resize((size, size), box=box)

  def add_watermark(self):
    # load the font file
    font = ImageFont.truetype("ibm-plex-mono.ttf", 24)

    # set up something to draw on the image
    drawer = ImageDraw.Draw(self.img)

    # draw multiple lines of text
    drawer.multiline_text(
      (32, 32), 
      "SuperHi\nwatermark", 
      font=font, 
      fill=(255, 0, 0, 100)
    )

  def convert_to_ascii(self):
    # set up a font size
    font_size = 10

    # what letters to draw with
    letters = [" ", ".", "!", "i", "u", "r", "e", "p", "S", "H"]

    # get the current image size
    (w, h) = self.img.size

    # make a new size based on the font size
    new_width = int(w / font_size)
    new_height = int(h / font_size)

    # what to resize the image to
    # and what the final image will be
    sample_size = (new_width, new_height)
    final_size = (new_width * font_size, new_height * font_size)

    # make it black and white as we don't care
    # about color, just how bright each pixel is
    self.make_grayscale()

    # up the contrast
    self.adjust_contrast(5.0)

    # resize it smaller
    self.img = self.img.resize(sample_size)

    # make a new RGBA image with a blue background
    ascii_img = Image.new("RGBA", final_size, color="#2727e6")

    font = ImageFont.truetype("ibm-plex-mono.ttf", font_size)
    drawer = ImageDraw.Draw(ascii_img)

    # for each pixel in the resized original image
    for x in range(new_width):
      for y in range(new_height):
        # get each channel
        (r, g, b, a) = self.img.getpixel((x, y))

        # as its black and white, just
        # need one channel (red for us!)
        brightness = r / 256

        # using that percentage, pick a letter in the
        # letters array based on how bright
        letter_num = int(len(letters) * brightness)
        letter = letters[letter_num]

        # place the text in the right position
        position = (x * font_size, y * font_size)
        drawer.text(position, letter, font=font, fill=(255, 255, 255, 255))

    # finally overwrite the image
    # with the new image
    self.img = ascii_img

  def save(self, output_filepath):
    print("This has saved!!!!")
    if self.filepath.endswith(".jpg"):
      self.img = self.img.convert("RGB")

    self.img.save(output_filepath)



# this will only run if we run this file directly
# if it gets imported, this code won't run
if __name__ == "__main__":
  # find all the images in inputs folder
  inputs = glob.glob("inputs/*")

  # make a new outputs folder (ok if it already exists)
  os.makedirs("outputs", exist_ok=True)

  # for each one
  for filepath in inputs:
    # make a new filepath
    output = filepath.replace("inputs", "outputs")

    # pass this into the digitizer class
    # convert it and then save
    image = Digitizer(filepath)
    image.convert_to_ascii()
    image.save(output)