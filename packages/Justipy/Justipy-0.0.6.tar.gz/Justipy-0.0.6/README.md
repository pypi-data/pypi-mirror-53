# Justipy

This package allows you to draw justified or centralized text to images.

Usage example:

```python
from PIL import Image
from Justipy.Justipy import Justipy

longtext = "Lorem ipsum vehicula himenaeos turpis odio sollicitudin quis amet suspendisse nisl, libero taciti ante interdum sollicitudin vestibulum felis mi hac, egestas fames luctus turpis imperdiet consectetur est gravida sem. malesuada maecenas vivamus consectetur donec diam sapien, in erat curae phasellus potenti, sed primis velit sem cursus. molestie ultrices tempus arcu viverra eleifend primis malesuada convallis ante accumsan, pulvinar conubia mollis at pellentesque consectetur ut dapibus sagittis integer nam, tempus orci elementum curabitur id rhoncus tempus velit elit."

centertext = "mollis vestibulum curabitur laoreet augue faucibus nullam a amet justo lorem, varius placerat magna pulvinar aptent quis porttitor metus lacus, diam etiam auctor nulla sagittis metus urna phasellus vitae."

im = Image.new('RGB', (1000, 550))
jpy = Justipy(im,
              longtext,
              tl_corner = [100, 75],		# top left corner anchor
              max_width = 800, 				# maximum horizontal size
              fontsize = 24,				# font size
              line_space = 32,				# space between lines
              paragraph_spaces = 8,			# space in beginning of paragraphs
              font = 'calibri.ttf',			# TrueType font (must be installed in your system)
              fontcolor = (255,255,255))	# RGB color of the font
jpy.drawJustifiedText()
im = jpy.getImage()

jpy = Justipy(im,
              centertext,
              tl_corner = [100, 380],
              max_width = 800,
              fontsize = 24,
              line_space = 32,
              paragraph_spaces = 0,
              font = 'calibri.ttf',
              fontcolor = (255,255,255))
jpy.drawCentralizedText()
im = jpy.getImage()

im.show()
```