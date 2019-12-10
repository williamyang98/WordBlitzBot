def load_bounding_boxes(filepath):
    bounding_boxes = {
        'characters': [],
        'values': [],
        'bonuses': []
    }

    current_boxes = None

    begin_header = "#begin "
    end_footer = "#end"

    with open(filepath, "r") as file:
        for line in file.readlines():
            if line.startswith(begin_header):
                read_mode = line[len(begin_header):]
                read_mode = read_mode.lower().strip()
                if read_mode in bounding_boxes:
                    current_boxes = bounding_boxes[read_mode]
                continue
        
            if line.startswith(end_footer):
                current_boxes = None
                continue
                
            if current_boxes is not None:
                bounding_box = map(int, line.strip().split(' '))
                bounding_box = tuple(bounding_box)
                current_boxes.append(bounding_box)
    
    return bounding_boxes
                
