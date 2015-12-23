import csv
import StringIO
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, views
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import BaseParser
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from keyedin.matcher.models import Key, Track, Box
from keyedin.matcher.serializers import (
    KeySerializer, TrackSerializer, BoxSerializer, BoxTrackSerializer
)


class CsvParser(BaseParser):
    media_type = 'text/csv'

    def parse(self, stream, media_type=None, parser_context=None):
        return stream.read()


class FileUploadView(views.APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = ()
    parser_classes = (CsvParser, )

    def put(self, request, format=None):
        csv_as_file = StringIO.StringIO(request.data)
        for i, line in enumerate(csv.reader(csv_as_file)):
            if i > 0:
                _, title, keys, bpm, _ = line
                for key in keys.split('/'):
                    key = Key.get_key_from_string(key)
                    t = Track(
                        name=title,
                        key=key,
                        bpm=bpm
                    )
                    t.save()
        return Response(status=204)


class KeyViewSet(viewsets.ModelViewSet):
    queryset = Key.objects.all()
    serializer_class = KeySerializer


class TrackViewSet(viewsets.ModelViewSet):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer

    @detail_route(methods=['get'])
    def matches(self, request, pk=None):
        track = self.get_object()
        matches = track.matches
        page = self.paginate_queryset(matches)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(matches, many=True)
        return Response(serializer.data)


class BoxTrackViewSet(viewsets.ViewSet):

    def list(self, request, boxes_pk=None):
        tracks = Track.objects.filter(boxes__id__exact=boxes_pk)
        serializer = BoxTrackSerializer(tracks, many=True, context={
            'request': request
        })
        return Response(serializer.data)

    def retrieve(self, request, pk=None, boxes_pk=None):
        tracks = Track.objects.filter(boxes__id__exact=boxes_pk)
        track = get_object_or_404(tracks, pk=pk)
        serializer = BoxTrackSerializer(track, context={
            'request': request
        })
        return Response(serializer.data)

    def get_object(self, queryset=None):
        return Track.objects.get(pk=self.kwargs.get('pk'))

    @detail_route(methods=['get'])
    def matches(self, request, pk=None, boxes_pk=None):
        track = self.get_object()
        matches = track.matches.filter(boxes__id__exact=boxes_pk)
        serializer = BoxTrackSerializer(matches, many=True, context={
            'request': request
        })
        return Response(serializer.data)


class BoxViewSet(viewsets.ModelViewSet):
    queryset = Box.objects.all()
    serializer_class = BoxSerializer
