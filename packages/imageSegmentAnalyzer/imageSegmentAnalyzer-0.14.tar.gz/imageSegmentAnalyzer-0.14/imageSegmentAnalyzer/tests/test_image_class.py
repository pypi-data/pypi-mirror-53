from unittest import TestCase
import numpy as np
import matplotlib.pyplot as plt
from imageSegmentAnalyzer.image import Image
import rawpy


class TestImage(TestCase):
    def setUp(self):
        self.img = rawpy.imread("TestImg2.NEF")
        self.I = Image(image=self.img, name="Test")

    def test_init_image(self):
        self.assertIsInstance(I, Image)

    def test_process_image(self):
        self.I.process_image()
        self.assertIsInstance(self.I.processed_image, np.ndarray)

    def test_select_points(self):
        self.I.select_points(name="test1")
        print(self.I.sections["test1"])

    def test_select_points(self):
        self.I.select_points(name="column1A", shape="rectangle", rows=8, columns=33)
        self.I.select_points(name="column2A", shape="rectangle", rows=8, columns=33)
        self.I.show()
        plt.show()

    def test_segment_images(self):
        self.I.select_points(name="column1A", shape="rectangle", rows=8, columns=33)
        self.I.select_points(name="column2A", shape="rectangle", rows=8, columns=33)
        self.I.show()
        plt.show()
        seg = self.I.get_segmented()
        k = seg.values()
        print(seg)
        plt.imshow(seg['column1Aa0'])
        plt.show()

    def test_getValues_images(self):
        self.I.select_points(name="column1A", shape="rectangle", rows=33, columns=8)
        self.I.show()
        plt.show()
        self.I.get_values()