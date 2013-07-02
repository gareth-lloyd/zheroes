var MAP_UTIL = function() {
  var SHADOW = new google.maps.MarkerImage("http://chart.apis.google.com/chart?chst=d_map_pin_shadow",
      new google.maps.Size(40, 37),
      new google.maps.Point(0, 0),
      new google.maps.Point(12, 35));

  var makeMarkerImage = function(colour) {
    var url = "http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|" + colour;
    return new google.maps.MarkerImage(url,
        new google.maps.Size(21, 34),
        new google.maps.Point(0,0),
        new google.maps.Point(10, 34));
  }
  var RED = "FE7569";
  var GREEN = "75FE69";
  return {
    red: makeMarkerImage(RED),
    green: makeMarkerImage(GREEN),
    shadow: SHADOW
  }
}();

var FoodProvider = Backbone.Model.extend({
  defaults: {
    expanded: false
  },

  hasRequirements: function() {
    return this.get('requirements').length > 0;
  }
});

var FiltersView = Backbone.View.extend({
  events: {
    "click #homeless-yes": "homeless",
    "click #homeless-no": "notHomeless",
    "click #gender-man": "genderMan",
    "click #gender-woman": "genderWoman",
    "blur #age": "ageSet",
  },
  homeless: function() {
    this.model.set('homeless', true);
  },
  notHomeless: function() {
    this.model.set('homeless', false);
  },
  genderMan: function() {
    this.model.set('gender', 'male');
  },
  genderWoman: function() {
    this.model.set('gender', 'female');
  },
  ageSet: function() {
    this.model.set('age', $('#age').val());
  }
});

var FoodProviderView = Backbone.View.extend({
  initialize: function () {
    this.model = this.options.model;
    var map = this.options.map;

    this.infowindow = new google.maps.InfoWindow({
        content: ich.organisation(this.model.toJSON())
    });

    var location = this.model.get('location');
    this.marker = new google.maps.Marker({
        position: new google.maps.LatLng(location.x, location.y),
        map: map,
        icon: this.model.hasRequirements() ? MAP_UTIL.red : MAP_UTIL.green,
        shadow: MAP_UTIL.shadow,
        animation: google.maps.Animation.DROP,
        title: this.model.get('name')
    });

    google.maps.event.addListener(this.marker, 'click', function() {
      $('body').trigger('closeAll');
      this.infowindow.open(map, this.marker);
    }.bind(this));

    $('body').on('closeAll', function() {
        this.infowindow.close();
    }.bind(this));
    this.model.on('remove', this.remove, this);
    this.model.on('destroy', this.destroy, this);
  },

  remove: function() {
    this.marker.setMap(null);
    this.infowindow.setMap(null);
  }
});

var Filters = Backbone.Model.extend({
  defaults: {
    homeless: null,
    age: null,
    gender: null
  },
  toQueryString: function() {
    return $.param(this.toJSON());
  }
})

var FoodProviders = Backbone.Collection.extend({
  model: FoodProvider,

  initialize: function(models, options) {
    Backbone.Collection.prototype.initialize.call(this, models, options);
    this.filters = options.filters;
    this.filters.on('change', function() {
      this.fetch();
    }, this);
  },

  url: function() {
    return "/filter/?" + this.filters.toQueryString();
  }
});

