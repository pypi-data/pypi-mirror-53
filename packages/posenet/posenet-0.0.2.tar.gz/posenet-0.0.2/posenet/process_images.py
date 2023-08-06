import tensorflow as tf
import cv2
import time
import argparse
import os
import numpy as np
import posenet

##
# Process dir of images and save npy vectors of each
##

def process_images(*args):
  args = args[0] if args else {}
  args['model'] = args.get('model', 101)
  args['scale_factor'] = args.get('scale_factor', 1.0)
  args['notxt'] = args.get('notxt', False)
  args['noimg'] = args.get('noimg', False)
  args['image_dir'] = args.get('image_dir', './images')
  args['output_dir'] = args.get('output_dir', './output')

  with tf.Session() as sess:
    model_cfg, model_outputs = posenet.load_model(args['model'], sess)
    output_stride = model_cfg['output_stride']

    if args['output_dir']:
      if not os.path.exists(args['output_dir']):
        os.makedirs(args['output_dir'])

    filenames = [
      f.path for f in os.scandir(args['image_dir']) if f.is_file() and f.path.endswith(('.png', '.jpg'))]

    start = time.time()
    for f in filenames:
      input_image, draw_image, output_scale = posenet.utils.read_imgfile(
        f, scale_factor=args['scale_factor'], output_stride=output_stride)

      heatmaps_result, offsets_result, displacement_fwd_result, displacement_bwd_result = sess.run(
        model_outputs,
        feed_dict={'image:0': input_image}
      )

      pose_scores, keypoint_scores, keypoint_coords = posenet.decode_multiple_poses(
        heatmaps_result.squeeze(axis=0),
        offsets_result.squeeze(axis=0),
        displacement_fwd_result.squeeze(axis=0),
        displacement_bwd_result.squeeze(axis=0),
        output_stride=output_stride,
        max_pose_detections=10,
        min_pose_score=0.25)

      print(input_image, pose_scores, keypoint_coords)

      keypoint_coords *= output_scale

      if args['output_dir'] and not args['noimg']:
        draw_image = posenet.utils.draw_skel_and_kp(
          draw_image, pose_scores, keypoint_scores, keypoint_coords,
          min_pose_score=0.25, min_part_score=0.25)

        cv2.imwrite(os.path.join(args['output_dir'], os.path.relpath(f, args['image_dir'])), draw_image)

      data = []
      if not args['notxt']:
        print()
        print('Results for image: %s' % f)
        for pi in range(len(pose_scores)):
          pose_data = []
          if pose_scores[pi] == 0.:
            break
          print('Pose #%d, score = %f' % (pi, pose_scores[pi]))

          for ki, (s, c) in enumerate(zip(keypoint_scores[pi, :], keypoint_coords[pi, :, :])):
            print('Keypoint %s, score = %f, coord = %s' % (posenet.constants.PART_NAMES[ki], s, c))

            # pull out the data to store on disk
            pose_data.append([ki, s, c])
          data.append(np.array(pose_data))

        # each array has shape [n_bodies, n_verts, n_dims]
        # the values in the last index have values:
        # [keypoint index, confidence, coord array]
        np.save(os.path.join(args['output_dir'], os.path.basename(f)), np.array(data))

    print('Average FPS:', len(filenames) / (time.time() - start))
