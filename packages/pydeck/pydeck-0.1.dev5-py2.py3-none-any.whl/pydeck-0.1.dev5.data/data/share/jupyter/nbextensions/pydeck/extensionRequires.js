/* eslint-disable */
define(function() {
  'use strict';
  requirejs.config({
    "map": {
        "*": {
            "@deck.gl/jupyter-widget": "nbextensions/pydeck/index"
        }
    },
    "paths": {
        "deck.gl": "https://unpkg.com/deck.gl@~7.3.0-beta.8/dist.min",
        "mapbox-gl": "https://api.tiles.mapbox.com/mapbox-gl-js/v1.2.1/mapbox-gl",
        "h3": "https://unpkg.com/h3-js@^3.4.3/dist/h3-js.umd",
        "s2Geometry": "https://bundle.run/s2-geometry@1.2.10?name=index",
        "loaders.gl/csv": "https://unpkg.com/@loaders.gl/csv@1.2.2/dist/dist.min"
    }
});
  // Export the required load_ipython_extension function
  return {
    load_ipython_extension: function() {}
  };
});
