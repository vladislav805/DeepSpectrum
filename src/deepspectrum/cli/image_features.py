import cv2
import numpy as np
import click
import logging
from os import environ
from os.path import basename
from .configuration import Configuration, GENERAL_OPTIONS, EXTRACTION_OPTIONS, LABEL_OPTIONS, WRITER_OPTIONS
from ..backend.plotting import PlotTuple
from ..tools.feature_writer import get_writer
from .utils import add_options

environ['GLOG_minloglevel'] = '2'
environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

log = logging.getLogger(__name__)

DESCRIPTION_IMAGE_FEATURES = 'Extract CNN-descriptors from images.'


def image_reader(files, size=500):
    for image in files:
        img = cv2.imread(image, cv2.IMREAD_COLOR)
        img = cv2.resize(img, dsize=(size, size))
        img = img[:, :, :3]
        yield PlotTuple(name=basename(image),
                        timestamp=None,
                        plot=np.array(img))


@click.command(help=DESCRIPTION_IMAGE_FEATURES)
@add_options(GENERAL_OPTIONS)
@add_options(EXTRACTION_OPTIONS)
@add_options(LABEL_OPTIONS)
@add_options(WRITER_OPTIONS[:-2])
def image_features(**kwargs):
    configuration = Configuration(plotting=False,
                                  file_types=['jpg', 'png'],
                                  **kwargs)
    plots = image_reader(configuration.files)
    log.info('Loading model and weights...')
    extractor = configuration.extractor(images=plots,
                                        **configuration.extraction_args)

    log.info('Extracting features from images...')
    writer = get_writer(**configuration.writer_args)
    writer.write_features(configuration.files, extractor)

    log.info('Done extracting features.')