from math import dist, sqrt

# Older Python version
# def dist(a, b):
#   x1, y1 = a
#   x2, y2 = b
#   return sqrt((x1-x2)**2 + (y2-y1)**2)

def rect_distance(box1, box2):
    x1, y1, x1b, y1b = box1
    x2, y2, x2b, y2b = box2
    b = box2
    left = x2b < x1
    right = x1b < x2
    bottom = y2b < y1
    top = y1b < y2
    if top and left:
        return dist((x1, y1b), (x2b, y2))
    elif left and bottom:
        return dist((x1, y1), (x2b, y2b))
    elif bottom and right:
        return dist((x1b, y1), (x2, y2b))
    elif right and top:
        return dist((x1b, y1b), (x2, y2))
    elif left:
        return x1 - x2b
    elif right:
        return x2 - x1b
    elif bottom:
        return y1 - y2b
    elif top:
        return y2 - y1b
    else:             # rectangles intersect
        return 0

def point_distance_to_rect(point, rect):
    x1, y1 = point
    x2, y2, x2b, y2b = rect
    dx = max(min(x2, x2b) - x1, 0, x1 - max(x2, x2b))
    dy = max(min(y2, y2b) - y1, 0, y1 - max(y2, y2b))
    return sqrt(dx*dx + dy*dy)

def combine_box(box1, box2):
    x1, y1, x2, y2 = box1
    xb1, yb1, xb2, yb2 = box2
    return (min(x1, xb1), min(y1, yb1), max(x2, xb2), max(y2, yb2))

def combine_boxes(boxes, threshold=20):

    def merge(boxes, result, threshold):
        if len(boxes) == 0:
            return result
        else:
            box = boxes[0]
            for index, stored_box in enumerate(result):
                if rect_distance(box, stored_box) <= threshold:
                    result[index] = combine_box(box, stored_box)
                    print('combined', result[index])
                    return merge(boxes[1:], result, threshold)
            result.append(tuple(box))
            print('box', box)
            print('result', result)
        return merge(boxes[1:], result, threshold)

    def need_merge(boxes, threshold=20):
        for i in range(0, len(boxes)):
            for j in range(0, len(boxes)):
                if i != j:
                    if rect_distance(boxes[i], boxes[j]) <= threshold:
                        return True
        return False
    boxes = merge(boxes, [], threshold)

    while need_merge(boxes, threshold):
        boxes = merge(boxes, [], threshold)
    return boxes

def add_padding(boxes, padding=5):
    new_boxes = []
    for box in boxes:
        x, y, x2, y2 = box
        new_box = (max(0, x-padding), max(0, y-padding), x2+padding, y2+padding)
        new_boxes.append(new_box)
    return new_boxes