import L from 'leaflet';
import leaflet_map from './leaflet-map.js';
import {FeatureLayer, featureLayer} from './featurelayer.js';

require('leaflet-legend');
require('leaflet-legend/leaflet-legend.css');
import layerBounds from './layer-bounds.js';

function map_with_geojson(map_id, options) {
    var map = leaflet_map(map_id, options);

    if (options && options.geojson) {
        map.geojson_layer = featureLayer(options.geojson).addTo(map);

        var properties = options.geojson.properties;
        if (properties && properties.legend) {
            L.control.legend({
                position: 'bottomright',
                buttonHtml: properties['legend-title'] || 'legend',
                items: properties.legend
            }).addTo(map);
        }
    }

    // Loop over each layer in the map, and call supplied callback with the featurelayers among them.
    map.eachFeatureLayer = function (callback) {
        map.eachLayer(function (layer) {
            if (!(layer instanceof FeatureLayer)) {
                // we are only interested in featureLayers, so skip everything else.
                return;
            }
            callback(layer);
        });
    };

    // Zoom to the extent of all featureLayers in the map.
    map.zoomExtent = function () {
        var bounds;
        map.eachFeatureLayer(function (layer) {
            if (bounds) {
                bounds.extend(layer.getBounds());
            } else {
                bounds = layer.getBounds();
            }
        });

        if (bounds && bounds.isValid()) {
            map.fitBounds(bounds, {maxZoom: 16});
        }
    };
    map.zoomExtent();

    // focus on the feature or the features which have key=value in their properties.
    map.focusOnFeature = function (key, value) {
        var bounds;
        map.eachFeatureLayer(function (mapLayer) {
            mapLayer.eachLayer(function (layer) {
                var properties = layer.feature.properties;
                if (key in properties && properties[key] == value) {
                    if (bounds) {
                        bounds.extend(layerBounds(layer));
                    } else {
                        bounds = layerBounds(layer);
                    }
                }
            });
        });
        if (bounds && bounds.isValid()) {
            map.fitBounds(bounds, {maxZoom: 16});
        }
    };

    map.reload = function () {
        map.invalidateSize();

        if (map.geojson_layer) {
            map.zoomExtent();
        }
    };

    map.reload();
    return map;
}

export {FeatureLayer, featureLayer, map_with_geojson};
