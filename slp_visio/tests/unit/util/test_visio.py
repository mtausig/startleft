from unittest.mock import MagicMock

from pytest import mark
from vsdx import VisioFile

from slp_visio.slp_visio.util.visio import get_shape_text, get_master_shape_text, normalize_label, \
    normalize_unique_id, get_unique_id_text
from slp_visio.tests.resources import test_resource_paths


class TestVisioUtils:

    def test_visio_complex_stencil_text(self):
        with VisioFile(test_resource_paths.visio_complex_stencil_text) as vis:
            shape = vis.pages[0].child_shapes[0]
        assert get_shape_text(shape) == "Custom AWS Step Functions workflow name"
        assert get_master_shape_text(shape) == "AWS Step Functions workflow"

    def test_get_shape_text_by_text_attribute(self):
        shape = MagicMock(text=' This is the text ')
        result = get_shape_text(shape)
        assert result == "This is the text"

    def test_get_shape_text_by_child_shapes_text(self):
        shape = MagicMock(
            text='',
            child_shapes=[
                MagicMock(text='This is'),
                MagicMock(text='\n'),
                MagicMock(text='the child text')
            ]
        )
        result = normalize_label(get_shape_text(shape))
        assert result == "This is the child text"

    def test_get_shape_text_by_master_shape_text_attribute(self):
        shape = MagicMock(
            text='',
            child_shapes=None,
            master_shape=MagicMock(text=' This is the master shape text ')
        )
        result = get_shape_text(shape)
        assert result == "This is the master shape text"

    def test_get_shape_text_by_master_shape_child_shapes_text(self):
        shape = MagicMock(
            text='',
            child_shapes=None,
            master_shape=MagicMock(
                text='',
                child_shapes=[
                    MagicMock(text='This is'),
                    MagicMock(text='\n'),
                    MagicMock(text='the master shape child text')
                ]
            )
        )
        result = normalize_label(get_shape_text(shape))
        assert result == "This is the master shape child text"

    def test_get_shape_text_without_master_shape(self):
        shape = MagicMock(
            text='',
            child_shapes=None,
            master_shape=None
        )
        result = get_shape_text(shape)
        assert result == ''

    def test_get_master_shape_text_without_text(self):
        shape = MagicMock(
            master_shape=MagicMock(
                text='',
                child_shapes=None
            )
        )
        result = get_master_shape_text(shape)
        assert result == ''

    def test_get_master_shape_text_by_text_attribute(self):
        shape = MagicMock(
            master_shape=MagicMock(
                text='This is the master text ',
                child_shapes=None
            )
        )
        result = get_master_shape_text(shape)
        assert result == 'This is the master text'

    def test_get_master_shape_text_by_child_shapes_text(self):
        shape = MagicMock(
            master_shape=MagicMock(
                text='',
                child_shapes=[
                    MagicMock(text='This is'),
                    MagicMock(text='\n'),
                    MagicMock(text='the master shape child text')
                ]
            )
        )
        result = normalize_label(get_master_shape_text(shape))
        assert result == "This is the master shape child text"

    @mark.parametrize('source_label',
                      ['\nTest label\n',
                       ' Test\n  \nlabel ',
                       '\n Test \n\n \n label \n',
                       ' \nTest\nlabel\n ',
                       '   Test   label   ',
                       u'Test \u00A0\u00A0 \u00A0 label',
                       u'\u00A0Test label\u00A0'])
    def test_normalize_label(self, source_label):
        assert normalize_label(source_label) == 'Test label'

    def test_get_unique_id_text_present(self):
        shape = MagicMock(
            master_page=MagicMock(
                master_unique_id='{1234-abcd}')
        )
        result = get_unique_id_text(shape)
        assert result == "1234-abcd"

    def test_get_unique_id_text_without_master_page(self):
        shape = MagicMock(
            master_page=None
        )
        result = get_unique_id_text(shape)
        assert result == ""

    def test_get_unique_id_text_without_master_unique_id(self):
        shape = MagicMock(
            master_page=MagicMock(
                master_unique_id=None)
        )
        result = get_unique_id_text(shape)
        assert result == ""

    @mark.parametrize('unique_id',
                      ['1234-abcd',
                       '{1234-abcd}'])
    def test_normalize_unique_id(self, unique_id):
        assert normalize_unique_id(unique_id) == '1234-abcd'
