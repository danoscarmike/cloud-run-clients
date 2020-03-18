from connectors.google_apis import *


class TestGoogleApis:
    def test_list_apis(self):
        assert list_apis() is not None
