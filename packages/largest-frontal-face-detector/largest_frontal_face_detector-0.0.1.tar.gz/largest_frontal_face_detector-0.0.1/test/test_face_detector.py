#fire up imports
import unittest
from unittest.mock import MagicMock
import os
from PIL import Image
import numpy as np
from largest_face_detector import face_detector

'''
Test class for {@link face_detector.py}
'''
class TestLargestFaceDetector(unittest.TestCase):

	def setUp(self):
		self.func = face_detector.detect_largest_face

	def test_detect_largest_face_ImageExceedsMaxHeight_RaisesNotImplementedError(self) :
		img = Image.fromarray(np.zeros([1025, 1000])).convert('RGB')
		img.save('temp.jpeg')
		with self.assertRaises(NotImplementedError) :
			self.func('temp.jpeg')
		os.remove('temp.jpeg')

	def test_detect_largest_face_ImageExceedsMaxWidth_RaisesNotImplementedError(self) :
		img = Image.fromarray(np.zeros([1000, 1025])).convert('RGB')
		img.save('temp.jpeg')
		with self.assertRaises(NotImplementedError) :
			self.func('temp.jpeg')
		os.remove('temp.jpeg')

	def test_detect_largest_face_FaceAbsentInImage_NullResponseReturned(self) :
		img = Image.fromarray(np.random.rand(3,2)).convert('RGB')
		img.save('temp.jpeg')
		cropped_image = self.func('temp.jpeg')
		self.assertIsNone(cropped_image)
		os.remove('temp.jpeg')

	def test_detect_largest_face_InvalidImagePath_RaisesRunTimeError(self) :
		with self.assertRaises(RuntimeError) :
			self.func('non_existent_file.jpeg')

	def test_detect_largest_face_ValidInput_CroppedFaceSavedSuccessfully(self) :
		file_loc = os.path.dirname(os.path.abspath(__file__)) + '/./resources/image.jpeg'
		face_detector.getOutputFilePath = MagicMock(return_value='temp_output.jpeg')
		cropped_image = self.func(file_loc)
		os.remove('temp_output.jpeg')
		self.assertFalse(None, cropped_image)
		face_detector.getOutputFilePath.assert_called_with()

if __name__ == '__main__':
    unittest.main()