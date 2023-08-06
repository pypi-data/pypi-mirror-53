#fire up imports
import dlib
import logging
import os
from datetime import datetime
from PIL import Image

#initialize logger and dlib detector
logging.basicConfig(filename="application.log", 
                    	format='%(asctime)s %(message)s', 
                    	filemode='w')
logger=logging.getLogger()
logger.setLevel(logging.DEBUG)
detector = dlib.get_frontal_face_detector()

#initialize static constants
MAX_WIDTH = 1024 #maximum allowed width of image
MAX_HEIGHT = 1024 #maximum allowed height of image
CROPPED_IMAGE_NAME = 'cropped_image.jpeg'
INPUT_IMAGE_SIZE_EXCEED_ERROR_MSG_FMT = 'Image size larger than {}*{} not supported'
TOTAL_FACES_DETECTED_MSG_FMT = 'Number of faces detected: {}'
NO_FACE_DETECTED_MSG = 'Face detector could not detect any face(s) in the image'
CROPPED_FACE_SAVED_MSG = 'Cropped face saved successfully at : {}'


def detect_largest_face(file_loc) :
	"""
	Gets largest cropped face from input image, also saves it
	
	Parameters
	----------
	file_loc : str
		The file location of the image

	Returns
	-------
	2-D array
		2-D numpy array representing the cropped face, or None if no face found in image

	Raises
	------
	NotImplementedError with error msg - INPUT_IMAGE_SIZE_EXCEED_ERROR_MSG_FMT
		If the image size exceeds MAX_HEIGHT (1024) * MAX_WIDTH (1024)

	Warnings
	--------
	1. NO_FACE_DETECTED_MSG warning When no face found in image

	Notes
	-----
	The function uses frontal_face_detector method of dlib library to find all cropped faces, then computes largest one amongst them

	"""

	img = dlib.load_rgb_image(file_loc)

	# raise exception if image size exceeds 1024*1024 pixels.
	if len(img) > MAX_HEIGHT or len(img[0]) > MAX_WIDTH :
		logger.error(INPUT_IMAGE_SIZE_EXCEED_ERROR_MSG_FMT.format(MAX_HEIGHT, MAX_WIDTH))
		raise NotImplementedError(INPUT_IMAGE_SIZE_EXCEED_ERROR_MSG_FMT.format(MAX_HEIGHT, MAX_WIDTH))

	#detect faces in image
	faces = detector(img, 1)
	logger.info(TOTAL_FACES_DETECTED_MSG_FMT.format(len(faces)))

	#Handle special case when no face is detected
	if len(faces) == 0 :
		logger.warning(NO_FACE_DETECTED_MSG)
		print (NO_FACE_DETECTED_MSG)
		return None

	#iterate over faces to find largest area face
	max_area, largest_face = 0, None
	for i, face in enumerate(faces) :
		face_area = (face.top() - face.bottom()) * (face.left() - face.right())
		if face_area > max_area :
			max_area = face_area
			largest_face = face

	#create cropped image and save
	cropped_image = Image.fromarray(img[largest_face.top():largest_face.bottom(), largest_face.left():largest_face.right()])
	
	cropped_image_path = getOutputFilePath()
	cropped_image.save(cropped_image_path)
	logger.info(CROPPED_FACE_SAVED_MSG.format(cropped_image_path))
	print (CROPPED_FACE_SAVED_MSG.format(cropped_image_path))
	return cropped_image

# created output file name using current timestamp
def getOutputFilePath() :
	readable_time = datetime.fromtimestamp(datetime.now().timestamp()).isoformat()
	return os.getcwd() + '/' + readable_time + '_' + CROPPED_IMAGE_NAME
	