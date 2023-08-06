/**
 * Some utilities
 */
class Utils {
    get_duration_string(duration) {
        let s = '';

        if (duration >= _DAY_IN_MILLIS) {
            s += Math.floor(duration / _DAY_IN_MILLIS) + ' jours';
        }

        if (duration >= _HOUR_IN_MILLIS) {
            s += Math.floor(duration / _HOUR_IN_MILLIS) + 'h';
            duration = duration % _HOUR_IN_MILLIS
        }

        let mins = Math.floor(duration / _MINUTE_IN_MILLIS);
        duration = duration % _MINUTE_IN_MILLIS;
        if (mins < 10) s+= '0';
        s += mins + 'm';

        let secs = Math.floor(duration / _SECOND_IN_MILLIS);
        if (secs < 10) s += '0';
        s += secs + 's';

        return s;
    }

    /**
     * Return a string to debug bounds
     */
    getBoundsStr(bounds) {
        let str = "NE: (" + bounds._northEast.lat.toFixed(6) + " - " + bounds._northEast.lng.toFixed(6) + ") , ";
        str += "SW: (" + bounds._southWest.lat.toFixed(6) + " - " + bounds._southWest.lng.toFixed(6) + ")";
        return str;
    }
}
let utils = new Utils();

/**
 * A custom Map
 */
class LeaftletGpxMap {
    constructor(map_id, map_options={}) {
        this.map_id = map_id;
        this.map_options = map_options;
        this.element = document.getElementById(map_id);
        this.container = document.getElementById(map_id + '-container');

        this.is_loaded = false;
        this.map = null;
        this.popup = null;
        this.icons = {};
        this.markers = [];

        this.min_lat = null;
        this.max_lat = null;
        this.min_lng = null;
        this.max_lng = null;

        if (map_options.hasOwnProperty('icons')) {
            for (let icon_name of Object.keys(map_options['icons'])) {
                let icon_data = map_options['icons'][icon_name];

                if (icon_name == 'startIcon' || icon_name == 'endIcon' || icon_name == 'markerIcon')
                    this.icons[icon_name] = L.icon(icon_data);
                else
                    this.icons[icon_name] = this._create_icon(icon_data);
            }
        }
    }

    /**
     * Create a custom icon
     */
    _create_icon(data) {

        if (!data.hasOwnProperty('className'))
            data.className = 'map-icon-container';

        if (!data.hasOwnProperty('html')) {
            let div = document.createElement('div'),
                img = document.createElement('img');

            if (data.hasOwnProperty('iconUrl'))
                img.src = data.iconUrl;

            img.className = 'map-icon';

            div.appendChild(img);
            data.html = div.innerHTML;
        }

        let icon = L.divIcon(data);

        if (!data.hasOwnProperty('iconSize'))
            icon.options.iconSize = null;

        return icon;
    }

    /**
     * Load the map
     */
    load() {
        this.map = L.map(this.element).setView([48.583, 7.75], 13);
        this.map.on('click', this.handle_map_click, this);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: 'Map data &copy; <a href="http://www.osm.org">OpenStreetMap</a>'
        }).addTo(this.map);

        let bounds = this.map.getBounds();
        this.min_lat = bounds._southWest.lat;
        this.max_lat = bounds._northEast.lat;
        this.min_lng = bounds._northEast.lng;
        this.max_lng = bounds._southWest.lng;

        this.is_loaded = true;
    }

    /**
     * Load the given GPX on the map
     */
    load_gpx(gpx_url=null) {
        if (!this.is_loaded) this.load();

        // Get GPX source from container if not provided
        if (gpx_url === null)
            gpx_url = this.container.getAttribute('data-gpx-source');

        // Create marker options
        let marker_options = {};
        if (this.icons.hasOwnProperty('startIcon'))
            marker_options.startIcon = this.icons['startIcon'];
        if ('endIcon' in this.icons)
            marker_options['endIcon'] = this.icons['endIcon'];
        if ('markerIcon' in this.icons)
            marker_options['wptIcons'] = {
                '': this.icons['markerIcon']
            };

        let _c = (c) => this.container.getElementsByClassName(c)[0];

        new L.GPX(gpx_url, {
            async: true,
            marker_options: marker_options,
            max_point_interval: 60000,
        }).on('loaded', e => {
            let gpx = e.target;
            this.map.fitBounds(gpx.getBounds());

            _c('title').textContent = gpx.get_name();
            _c('start').textContent = gpx.get_start_time().toLocaleString();
            _c('distance').textContent = gpx.m_to_km(gpx.get_distance()).toFixed(2);
            _c('duration').textContent = utils.get_duration_string(gpx.get_moving_time());
            _c('elevation-gain').textContent = gpx.get_elevation_gain().toFixed(0);
            _c('elevation-loss').textContent = gpx.get_elevation_loss().toFixed(0);
            _c('elevation-net').textContent  = (gpx.get_elevation_gain() - gpx.get_elevation_loss()).toFixed(0);

            let speed = gpx.get_moving_speed();
            if (speed > 10)
                _c('average-speed').textContent = speed.toFixed(0);
            else
                _c('average-speed').textContent = speed.toFixed(2);

            let stop_time = gpx.get_total_time() - gpx.get_moving_time();
            _c('stop-duration').textContent = utils.get_duration_string(gpx.get_total_time() - gpx.get_moving_time());
      }).addTo(this.map);
    }

    /**
     * Calculate and fit map bounds that fit with given lat and lng
     */
    calculate_new_bounds(lat, lng) {
        let bounds = this.map.getBounds();
        if (bounds.contains([lat, lng])) return;

        let changed = false;
        if (this.min_lat == null || this.min_lat > lat) {
            this.min_lat = lat;
            changed = true;
        }
        if (this.max_lat == null || this.max_lat < lat) {
            this.max_lat = lat;
            changed = true;
        }
        if (this.min_lng == null || this.min_lng > lng) {
            this.min_lng = lng;
            changed = true;
        }
        if (this.max_lng == null || this.max_lng < lng) {
            this.max_lng = lng;
            changed = true;
        }

        if (!changed) return;

        let topRightBounds = L.latLng(this.max_lat, this.max_lng),
            bottomLeftBounds = L.latLng(this.min_lat, this.min_lng),
            newBounds = L.latLngBounds(topRightBounds, bottomLeftBounds);

        this.map.fitBounds(newBounds);
    }

    /**
     * Return a correct icon from an unknown source
     */
    getIcon(icon) {
        return this.icons[icon];
    }

    /**
     * Add a marker
     */
    add_marker(lat, lng, marker_options={}) {

        // Get the correct icon
        if (marker_options.hasOwnProperty('icon'))
            marker_options['icon'] = this.getIcon(marker_options['icon']);

        let latlng = L.latLng(lat, lng);
        let marker = L.marker(latlng, marker_options).addTo(this.map);
        this.markers.push(marker);

        this.calculate_new_bounds(lat, lng);
    }

    /**
     * Display a popup a given position with given content
     */
    show_popup(lat, lng, content) {
        if (this.popup === null)
            this.popup = L.popup();

        this.popup.setLatLng([lat, lng])
            .setContent(content)
            .openOn(this.map);
    }

    /**
     * Handle click on map
     */
    handle_map_click(event) {
        try {
            let content = "Latitude: <b>" + event.latlng.lat.toFixed(6) + "</b><br>Longitude: <b>" + event.latlng.lng.toFixed(6) + "</b>"
            this.show_popup(event.latlng.lat, event.latlng.lng, content);
        } catch (e) {
            console.error(e);
        }
    }
}
