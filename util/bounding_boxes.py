# Get bounding boxes from overlay
# image = 4 channel
# colour = 4 channel
# assume boxes will be the same shape
def get_bounding_boxes(image, box_colour):
    height, width = image.shape[:2]
    bounding_boxes = []
    
    last_box_height = None
    box_height = None
    box_width = None
    
    y = 0
    x = 0
    while y < height:
        x = 0
        while x < width:
            colour = image[y,x,:]
            if not (colour == box_colour).all():
                x += 1
                continue
            # if box colour, then find top and left edges
            x_start = x
            y_start = y
            
            # if box shape known, just predict
            if box_height is not None and box_width is not None:
                x_end = x_start+box_width
                y_end = y_start+box_height
                bounding_box = (x_start, y_start, x_end-1, y_end-1)
                bounding_boxes.append(bounding_box)
                last_box_height = box_height
                x = x_end+1
                continue
            
            # if finding box shape for first time
            x_end = x
            y_end = y
            _x = x_start+1
            _y = y_start+1
            # check top edge
            while _x < width:
                colour = image[y,_x,:]
                if not (colour == box_colour).all():
                    x_end = _x
                    break
                _x += 1
            # check left edge
            while _y < height:
                colour = image[_y,x,:]
                if not (colour == box_colour).all():
                    y_end = _y
                    break
                _y += 1
            # check if box or not
            box_width = x_end-x_start
            box_height = y_end-y_start
            if box_width > 1 and box_height > 1:
                bounding_box = (x_start, y_start, x_end-1, y_end-1)
                bounding_boxes.append(bounding_box)
                x = x_end
                last_box_height = box_height
            # increment normally
            x += 1
        
        if last_box_height is not None:
            y += last_box_height + 1
            last_box_height = None
        else:
            y += 1
                
    return bounding_boxes