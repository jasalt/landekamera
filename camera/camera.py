from sh import identify

# fswebcam, 
# Check deps

def image_is_dark(image):
    deviation = str(identify('-format', ' \"%[standard-deviation]\"', image))
    deviation = float(deviation[1:-1])  # strip quotes, convert to float
    min_deviation = 700

    if deviation < min_deviation:
        print("Image too dark. Deviation: %s, Limit: %s." % (deviation, min_deviation))
        return True

    print("Image not too dark. Deviation: %s, Limit: %s." % (deviation, min_deviation))
    return False
        
image_is_dark("out.jpg")
# if dark.. wait long?
