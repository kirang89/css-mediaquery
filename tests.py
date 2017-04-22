#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cssmq import match, parse
import unittest


class MediaQueryParserAndMatcherTest(unittest.TestCase):

    def test_screen(self):
        self.assertEquals(parse('screen'), [{
            "inverse": False,
            "type": 'screen',
            "expressions": []
        }])

    def test_not_screen(self):
        self.assertEquals(parse('not screen'), [{
            "inverse": True,
            "type": 'screen',
            "expressions": []
        }])

    def test_retina_media_query_list(self):
        query = 'only screen and (-webkit-min-device-pixel-ratio: 2),\n' + \
                'only screen and (min--moz-device-pixel-ratio: 2),\n' + \
                'only screen and (-o-min-device-pixel-ratio: 2/1),\n' + \
                'only screen and (min-device-pixel-ratio: 2),\n' + \
                'only screen and (min-resolution: 192dpi),\n' + \
                'only screen and (min-resolution: 2dppx)'

        parsed = parse(query)
        self.assertTrue(isinstance(parsed, list))
        self.assertEquals(len(parsed), 6)
        self.assertEquals(parsed[0]["expressions"][0]["feature"],
                          "-webkit-min-device-pixel-ratio")
        self.assertEquals(parsed[1]["expressions"][0]["modifier"],
                          "min")

    def test_media_query_invalid(self):
        queries = ["some crap", "48em", "screen and crap",
                   "screen and (48em)", "screen and (foo:)", "()",
                   "(foo) (bar)", "(foo:) and (bar)"]

        for query in queries:
            try:
                parse(query)
            except Exception as e:
                msg = "Invalid CSS media query: {}".format(query)
                self.assertEquals(e.message, msg)
            else:
                self.assertTrue(False)

    def test_orientation_match(self):
        self.assertTrue(match("(orientation: portrait)", {
            "orientation": "portrait"
        }))

        self.assertFalse(match("(orientation: landscape)", {
            "orientation": "portrait"
        }))

    def test_scan_match(self):
        self.assertTrue(match("(scan: progressive)", {
            "scan": "progressive"
        }))

        self.assertFalse(match("(scan: progressive)", {
            "scan": "interlace"
        }))

    def test_width_match(self):
        self.assertTrue(match("(width: 800px)", {"width": "800"}))
        self.assertFalse(match("(width: 800px)", {"width": "810"}))

    def test_width_range_match(self):
        self.assertTrue(match("(min-width: 48em)", {"width": "80em"}))
        self.assertFalse(match("(min-width: 48em)", {"width": "20em"}))
        self.assertFalse(match("(min-width: 48em)", {"resolution": "72"}))

    def test_different_unit_match(self):
        self.assertTrue(match("(min-width: 500px)", {"width": "48em"}))
        self.assertTrue(match("(min-width: 500px)", {"width": "48rem"}))
        self.assertTrue(match("(max-height: 1000px)", {"height": "20cm"}))
        self.assertFalse(match("(max-height: 1000px)", {"height": "850pt"}))
        self.assertTrue(match("(max-height: 1000px)", {"height": "60pc"}))

    def test_resolution_match(self):
        self.assertTrue(match("(resolution: 50dpi)", {"resolution": "50"}))
        self.assertTrue(match('(min-resolution: 50dpi)', {"resolution": "72"}))
        self.assertFalse(match('(min-resolution: 72dpi)', {"width": "300"}))
        self.assertFalse(match('(min-resolution: 72dpi)', {"width": "75dpcm"}))
        self.assertTrue(match("(resolution: 192dpi)", {"resolution": "2dppx"}))

    def test_aspect_ratio_match(self):
        self.assertTrue(match('(min-aspect-ratio: 4/3)',
                              {'aspect-ratio': '16 / 9'}))
        self.assertFalse(match('(max-aspect-ratio: 4/3)',
                               {'aspect-ratio': '16/9'}))
        self.assertFalse(match('(max-aspect-ratio: 72dpi)', {"width": "300"}))
        self.assertFalse(match('(min-aspect-ratio: 2560/1440)',
                               {'aspect-ratio': 4 / 3}))

    def test_not_query_match(self):
        self.assertFalse(match('not screen and (color)',
                               {"type": 'screen', "color": "1"}))
        self.assertTrue(match('not screen and (color), screen and (min-height: 48em)',
                              {"type": 'screen', "height": "1000"}))
        self.assertTrue(match('not screen and (color), screen and (min-height: 48em)',
                              {"type": 'screen', "height": "1000"}))

    def test_type_match(self):
        self.assertTrue(match('screen', {'type': 'screen'}))
        self.assertFalse(match('screen and (color:1)',
                               {'type': 'tv', 'color': '1'}))
        self.assertFalse(match('(min-width: 500px)', {'type': 'screen'}))

    def test_not_match(self):
        self.assertTrue(match('not screen and (color), screen and (min-height: 48em)',
                              {'type': 'screen', 'height': '1000'}))
        self.assertFalse(match('not all and (min-width: 48em)',
                               {'type': 'all', 'width': '1000'}))

    def test_media_query_combinations(self):
        self.assertTrue(match('screen and (min-width: 767px)',
                              {'type': 'screen', 'width': '980'}))
        self.assertTrue(match('screen and (min-width: 767px) and (max-width: 979px)',
                              {'type': 'screen', 'width': '800'}))
        self.assertTrue(match('screen and (color)',
                              {'type': 'screen', 'color': '1'}))
        self.assertTrue(match('screen and (min-width: 767px), screen and (color)',
                              {'type': 'screen', 'color': '1'}))
        self.assertFalse(match('screen and (max-width: 1200px), handheld and (monochrome)',
                               {'type': 'screen', 'monochrome': '0'}))


if __name__ == '__main__':
    unittest.main()
