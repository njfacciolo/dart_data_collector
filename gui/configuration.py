
# Outer dimensions of the dart board image under gui/images/dartboard.png
DARTBOARD_IMAGE_DIMENSIONS = (1500,1500)

# If you select a different dartboard image, you'll need to calibrate the center of the image
CENTER = (750,750)

# Diameter of each ring in pixels (of the fullsize image)
DIAMETERS = (47,112,640,707,1055,1124)

# Dimensions of the board to put on the monitor. This is critical when re-using throw data
DISPLAY_BOARD_SIZE = (900,900)

# Draw the overlay onto the existing image
DRAW_OVERLAY = False


## Alcohol Ingestion Parameters ##

# Rate at which the body absorbes the alcohol (how long until you feel the drink) in hours
ABSORPTION_RATE = 0.125

# Rate at which the body processes the drink (1 per hour)
METABOLIC_RATE = 1.0