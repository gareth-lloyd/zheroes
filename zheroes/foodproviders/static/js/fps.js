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
  var RED = "E14747";
  var GREEN = "90C47E";
  var ORANGE = "D58646";
  return {
    red: makeMarkerImage(RED),
    green: makeMarkerImage(GREEN),
    orange: makeMarkerImage(ORANGE),
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
    "change #age": "ageSet",
    "change #daySelector": "daySelected",
    "change #timeSelector": "timeSelected",
    "change #foodSelector": "foodTypeSelected",
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
  },
  daySelected: function() {
    this.model.set('day', $('#daySelector').val());
  },
  timeSelected: function() {
    this.model.set('time', $('#timeSelector').val());
  },
  foodTypeSelected: function() {
    this.model.set('food', $('#foodSelector').val());
  }
});

var FoodProviderView = Backbone.View.extend({
  initialize: function () {
    this.model = this.options.model;
    var map = this.options.map;
    this.filters = this.options.filters;

    this.infowindow = new google.maps.InfoWindow({
        content: ich.organisation(this.model.toJSON())
    });

    var location = this.model.get('location');
    this.marker = new google.maps.Marker({
      position: new google.maps.LatLng(location.x, location.y),
      map: map,
      icon: this.getIcon(),
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

    this.filters.on('change', this.refreshMarker, this);
    this.model.on('remove', this.remove, this);
    this.model.on('destroy', this.destroy, this);
  },

  getIcon: function() {
    if (this.model.get('referral_required')) {
      return MAP_UTIL.orange;
    } else if (this.filters.hasAdditionalRequirements(this.model)) {
      return MAP_UTIL.red;
    } else {
      return MAP_UTIL.green;
    }
  },

  refreshMarker: function() {
    this.marker.setIcon(this.getIcon());
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
  },
  hasAdditionalRequirements: function (foodProvider) {
    // return true if the foodProvider has additional requirements
    // that may or may not be satisfied.
    var age = parseInt(this.get('age'));
    var homeless = this.get('homeless');
    additional = foodProvider.get('requirements').filter(function(req) {
      // for each requirement, return false if satisfied so that it
      // is not included in the additional list.
      if (req == "Homeless") {
        return !(homeless === true);
      }
      if (age && req == "Over 16") {
        return age < 16;
      }
      if (age && req == "Under 25") {
        return age > 25;
      }
      if (age && req == "Over 25") {
        return age <= 25;
      }
      if (age && req == "Over 60") {
        return age < 60;
      }
      return true;
    });
    return additional.length > 0;
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

