var FoodProvider = Backbone.Model.extend({
  defaults: {
    expanded: false
  }
});

var FoodProviderView = Backbone.View.extend({
  initialize: function () {
    this.model = this.options.model;
    var map = this.options.map;

    var infowindow = new google.maps.InfoWindow({
        content: ich.organisation(this.model.toJSON())
    });

    var location = this.model.get('location');
    var marker = new google.maps.Marker({
        position: new google.maps.LatLng(location.x, location.y),
        map: map,
        title: this.model.get('name')
    });

    google.maps.event.addListener(marker, 'click', function() {
      $('body').trigger('closeAll');
      infowindow.open(map, marker);
    });

    $('body').on('closeAll', function() {
        infowindow.close();
    });
  }
});

var Filters = Backbone.Model.extend({
  defaults: {
    homeless: false
  },
  toQueryString: function() {
    return "?homeless=" + this.get('homeless');
  }
})

var FoodProviders = Backbone.Collection.extend({
  model: FoodProvider,

  initialize: function(models, options) {
    Backbone.Collection.prototype.initialize.call(this, models, options);
    this.filters = options.filters;
    this.filters.on('change', function() {
      this.fetch({reset: true});
    }.bind(this));
  },

  url: function() {
    return "/filter/" + this.filters.toQueryString();
  }
});

