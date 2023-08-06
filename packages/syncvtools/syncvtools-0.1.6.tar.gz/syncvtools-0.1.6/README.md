# Synapse Computer Vision Tools
More details are provided in Notion page. 

## Requirements
- Python 3.5+
- OpenCV
- Pillow
- LXML
- For TF Records - TensorFlow

## Installation
Using PIP

    pip3 import syncvtools

### Visualize predictions from prod

```
from syncvtools.utils.draw_detections import DrawDetections
from syncvtools.utils.parsers import ProdDetections, TFRecords, TFObjDetAPIDetections

prod_dets = ProdDetections.parse_prod_detections(img_dir='IMAGE_DIRECTORY', predictions_dir='DETECTIONS_FILE_DIR')
drawer = DrawDetections(bbox_line_height=1, threshold=0.5)
for pro_det in prod_dets:
    vis_img = drawer.draw_imageleveldetections(img_dets=prod_dets[pro_det])
    cv2.imshow("predictions", vis_img)
    cv2.waitKey(0)
```


### Visualize predictions from TF training
```
from syncvtools.utils.draw_detections import DrawDetections
from syncvtools.utils.parsers import ProdDetections, TFRecords, TFObjDetAPIDetections

tf_inf = TFObjDetAPIDetections.parse_detections(detection_file='detections_and_losses.json')
tf_gts = TFRecords.parse(tfrecord_src='val.tfrecord')
#adding image info to predictions/gt
tf_inf += tf_gts
if label_map is not None:
    tf_inf.process_labelmap('path_to_label_map.pbtxt')

drawer = DrawDetections(bbox_line_height=1, threshold=0.5)


for pro_det in tf_inf:
    if not tf_inf[pro_det].detections and not tf_inf[pro_det].ground_truth:
        continue #no gt/detections here
    vis_img = drawer.draw_imageleveldetections(img_dets=tf_inf[pro_det])
    cv2.imshow("predictions/gt from TF inference", vis_img)
    cv2.waitKey(0)
```

# utils

```
from syncvtools.utils import file_tools as ft

ft.get_file_list_by_ext(dir='input_path', ext=('jpg','png'))
```

Returns a list of string with full path to files with `ext` extension.

