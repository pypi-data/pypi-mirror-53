import L from 'leaflet';

function layerBounds(layer) {
    if (layer.getBounds) {
        return layer.getBounds();
    } else {
        return L.latLngBounds(layer.getLatLng(), layer.getLatLng());
    }
}

export default layerBounds;
