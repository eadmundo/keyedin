from rest_framework import serializers
from rest_framework.reverse import reverse
from keyedin.matcher.models import Key, Track, Box
from parse import parse


class BoxTrackMatchesHyperlink(serializers.HyperlinkedRelatedField):

    view_name = 'box-tracks-matches'
    lookup_url_kwarg = 'boxes_pk'

    def get_url(self, obj, view_name, request, format):
        (box_pk, ) = parse('/boxes/{}/tracks/', request.path)
        url_kwargs = {
            'boxes_pk': box_pk,
            'pk': obj.pk
        }
        return reverse(
            view_name,
            kwargs=url_kwargs,
            request=request,
            format=format
        )


class BoxTrackSerializer(serializers.ModelSerializer):

    matches = BoxTrackMatchesHyperlink(
        read_only=True,
        source='*'
    )

    class Meta:
        model = Track


class BoxSerializer(serializers.ModelSerializer):

    tracks = serializers.HyperlinkedIdentityField(
        view_name='box-tracks-list',
        lookup_url_kwarg='boxes_pk'
    )

    class Meta:
        model = Box


class KeySerializer(serializers.ModelSerializer):

    class Meta:
        model = Key


class TrackSerializer(serializers.ModelSerializer):

    matches = serializers.HyperlinkedIdentityField(
        view_name='track-matches',
        read_only=True
    )

    number_of_matches = serializers.IntegerField(
        read_only=True
    )

    class Meta:
        model = Track
