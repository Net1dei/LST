import torch
from torchvision import ops
 
# Bounding box coordinates.
ground_truth_bbox = torch.tensor([[0, 0, 10, 10]], dtype=torch.float)
prediction_bbox = torch.tensor([[0, 0, 5, 5]], dtype=torch.float)
 
# Get iou.
iou = ops.box_iou(ground_truth_bbox, prediction_bbox)
print('IOU : ', iou.numpy()[0][0])

