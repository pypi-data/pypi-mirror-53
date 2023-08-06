Simple Django application to include LeafletJS map and display GPX file.

Not documented yet :-/


## Configuration

This is an example of custom configuration

    import os
    
    STATIC_URL = '/static'
    LEAFLET_GPX_ICONS = {
        'markerIcon': {
            'iconUrl': os.path.join(STATIC_URL, 'icons/my-custom-marker.png'),
            'iconSize': [32, 32],
            'iconAnchor': [5, 31],
        }
    }

### LEAFLET_GPX_ICONS

There are three editable icons: 

- **markerIcon**: markers points
- **startIcon**: GPX start point
- **endIcon**: GPX end point

The icon options are the same as those for creating an icon in the Leaflet-JS library.  
Here is a link to the documentation: <https://leafletjs.com/reference-1.5.0.html#icon>

