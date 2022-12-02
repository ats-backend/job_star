from rest_framework.parsers import JSONParser, MultiPartParser


class CustomJSONParser(JSONParser):

    def parse(self, stream, media_type=None, parser_context=None):
        data = super(CustomJSONParser, self).parse(
            stream,
            media_type=None,
            parser_context=None
        )
        print(data)
        return data


class CustomMultiPartParser(MultiPartParser):

    def parse(self, stream, media_type=None, parser_context=None):
        return super(CustomMultiPartParser, self).parse(
            stream,
            media_type=None,
            parser_context=None
        )