#!/usr/bin/env python
import os
import os.path
import sys
import django
from glob import glob
from django.conf import settings
from django.test.utils import get_runner

def cleanMedia():
    mediaDir = settings.MEDIA_ROOT
    imgDir = os.path.join(mediaDir, "images")
    origImgDir = os.path.join(mediaDir, "original_images")
    for path in glob(os.path.join(imgDir, "*")) + glob(os.path.join(origImgDir, "*")):
        try:
            os.remove(path)
        except:
            print("Error deleting", path)

def run():
    verbosity = 1
    if "-v" in sys.argv or "--verbose" in sys.argv:
        verbosity = 2
    os.environ['DJANGO_SETTINGS_MODULE'] = 'ls.joyous.tests.settings'
    django.setup()
    cleanMedia()
    TestRunner = get_runner(settings)
    test_runner = TestRunner(top_level="ls/joyous",
                             verbosity=verbosity,
                             keepdb=False)
    labels = ["ls.joyous.tests."+arg for arg in sys.argv[1:]
              if not arg.startswith("-")]
    if not labels:
        labels = ["ls.joyous.tests"]
    failures = test_runner.run_tests(labels)
    return failures

def coverage():
    from coverage import Coverage
    cover = Coverage()
    cover.start()
    failures = run()
    cover.stop()
    cover.save()
    cover.html_report()
    return failures

if __name__ == "__main__":
    if "--coverage" in sys.argv:
        failures = coverage()
    else:
        failures = run()
    sys.exit(bool(failures))
