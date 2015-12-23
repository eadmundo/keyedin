import fudge
from rest_framework.test import APITestCase
from keyedin.matcher.models import Key, Track
from keyedin.matcher.views import FileUploadView

data = [
    "Collection name,File name,Key result,BPM,Energy",
    "Library,Song 1,Bm,118.01,6"
]


class KeyTests(APITestCase):

    fixtures = ['keys']

    def test_C_dominant_is_G(self):
        self.assertEqual(
            Key.objects.get(name='C', minor=False).dominant.display_name,
            'G major'
        )

    def test_Cm_dominant_is_Gm(self):
        self.assertEqual(
            Key.objects.get(name='C', minor=True).dominant.display_name,
            'G minor'
        )

    def test_Csharp_dominant_is_Gsharp(self):
        self.assertEqual(
            Key.objects.get(name='C#', minor=False).dominant.display_name,
            'G# major'
        )


class FileUploadViewTests(APITestCase):

    def setUp(self):
        self.fUV = FileUploadView()

    def test_put(self):
        # request = (fudge.Fake()
        #                 .has_attr(data='\n'.join(data))
        #            )
        # self.fUV.put(request)
        pass


class MatcherTests(APITestCase):

    fixtures = ['keys', 'test_tracks']

    def test_key_should_match_itself(self):
        pass
