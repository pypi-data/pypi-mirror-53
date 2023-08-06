# -*- coding: utf-8 -*-
from collective.geo.geographer.interfaces import IGeoreferenceable
from collective.geo.geographer.interfaces import IGeoreferenced
from collective.geo.leaflet.interfaces import IMapLayer
from collective.geo.leaflet.interfaces import IGeoMap
from collective.geo.leaflet.utils import get_marker_image
from collective.geo.settings import utils
from collective.geo.settings.interfaces import IGeoFeatureStyle
from collective.geo.settings.interfaces import IGeoSettings
from zope.component import getGlobalSiteManager
from zope.schema import getFields
from zope.interface import implementer

import json


@implementer(IGeoMap)
class GeoMap(object):

    def __init__(self, context):
        self.context = context
        self.request = context.REQUEST
        self.geo_feature_style = self.geo_feature_style()
        self.geo_settings = self.geo_settings()

    @property
    def has_map(self):
        if not IGeoreferenceable.providedBy(self.context):
            return False
        else:
            return True

    def geo_feature_style(self):
        fields = [i for i in getFields(IGeoFeatureStyle)]
        manager = IGeoFeatureStyle(self.context, None)
        use_custom_styles = getattr(manager, 'use_custom_styles', False)
        if not use_custom_styles:
            manager = utils.geo_styles(self.context)
        styles = {
            'use_custom_styles': use_custom_styles
        }
        for name in fields:
            styles[name] = getattr(manager, name, None)
        styles['marker_image'] = get_marker_image(self.context,
                                                  styles['marker_image'])
        return styles

    def geo_settings(self):
        settings = {}
        fields = [i for i in getFields(IGeoSettings)]
        manager = utils.geo_settings(self.context)
        for name in fields:
            settings[name] = getattr(manager, name, None)
        return settings

    def map_center(self):
        lat = self.geo_settings.get('latitude')
        lon = self.geo_settings.get('longitude')
        if self.coordinates and self.coordinates[0] == 'Point':
            lon = self.coordinates[1][0]
            lat = self.coordinates[1][1]

        return {'longitude': str(lon), 'latitude': str(lat)}

    @property
    def coordinates(self):
        if self.has_map:
            geo_obj = IGeoreferenced(self.context)
            if getattr(geo_obj, 'coordinates', False):
                return geo_obj.type, geo_obj.coordinates
            else:
                return None, None
        return None, None

    @property
    def json_coordinates(self):
        return json.dumps(self.coordinates)

    def default_layers(self):
        registred_layers = {}
        ordered_layers = []
        baselayers = []

        gsm = getGlobalSiteManager()
        for registration in gsm.registeredSubscriptionAdapters():
            if registration.provided is IMapLayer:
                layer = registration.factory(self.context, self.request)
                registred_layers[layer.name] = layer

        default_layers = self.geo_settings.get('default_layers')
        if not default_layers:
            default_layers = (u'osm',)

        for default_layer in default_layers:
            if default_layer in registred_layers.keys():
                l = registred_layers[default_layer]
                baselayers.append({"title": l.title, "name": l.name})
                ordered_layers.append(l.index() % dict(name=l.name))

        return {
            "layers": "\n".join(ordered_layers),
            "baselayers": json.dumps(baselayers)
        }

    def has_googlemap(self):
        default_layers = self.default_layers()
        return 'google_' in default_layers['baselayers']

    def inline_style(self):
        inline_style = {
            'height': '600px',
            'width': '100%'
        }
        height = self.geo_feature_style.get('map_height')
        width = self.geo_feature_style.get('map_width')
        if height:
            inline_style['height'] = height
        if width:
            inline_style['width'] = width
        return ";".join([
            "{}: {}".format(k, v) for k, v in inline_style.items()
        ])
