from __future__ import annotations

import unittest

from app.test3_manifest import build_test3_manifest


class TestManifest(unittest.TestCase):
    def test_test3_manifest_is_structured(self) -> None:
        manifest, report = build_test3_manifest()
        self.assertEqual(len(manifest["slides"]), 10)
        self.assertGreaterEqual(report["editableTextObjects"], 100)
        self.assertGreaterEqual(report["nativeShapeObjects"], 40)
        self.assertEqual(report["nativeChartObjects"], 2)
        for slide in manifest["slides"]:
            self.assertTrue(any(item["type"] == "text" for item in slide["items"]))
            self.assertFalse(
                len(slide["items"]) == 1 and slide["items"][0]["type"] == "image",
                "A slide must not be a single full-page image",
            )

    def test_all_items_stay_near_slide_bounds(self) -> None:
        manifest, _ = build_test3_manifest()
        width = manifest["layout"]["width"]
        height = manifest["layout"]["height"]
        for slide_number, slide in enumerate(manifest["slides"], start=1):
            for item in slide["items"]:
                self.assertGreaterEqual(item["x"], -0.01, slide_number)
                self.assertGreaterEqual(item["y"], -0.01, slide_number)
                self.assertLessEqual(item["x"] + item["w"], width + 0.02, slide_number)
                self.assertLessEqual(item["y"] + item["h"], height + 0.02, slide_number)


if __name__ == "__main__":
    unittest.main()

