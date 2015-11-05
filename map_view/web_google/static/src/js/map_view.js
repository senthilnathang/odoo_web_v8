/*---------------------------------------------------------
 * OpenERP web_gantt
 *---------------------------------------------------------*/
openerp.web_google = function (instance) {

    var QWeb = instance.web.qweb;
        _t = instance.web._t,
        _lt = instance.web._lt;

    function google_ensure_jsapi_loaded() {
        if (typeof(instance.google_jsapi_loaded) !== "undefined") {
            // please wait until the first call finishes:
            return instance.google_jsapi_loaded;
        }

        instance.google_jsapi_loaded = $.Deferred();
        window.ginit = function() {
            instance.google_jsapi_loaded.resolve();
        };
        console.log('Loading Google jsapi.');
        $.getScript('//www.google.com/jsapi' +
                    '?sensor=false&async=true&callback=ginit');
        return instance.google_jsapi_loaded;
    }

    function google_ensure_module_loaded(module, version, options) {
        if (typeof(instance.google_modules) === "undefined") {
            instance.google_modules = {};
        }
        if (typeof(instance.google_modules[module]) !== "undefined") {
            // please wait until the first call finishes
            return instance.google_modules[module];
        }
        instance.google_modules[module] = $.Deferred();
        google_ensure_jsapi_loaded().then(function() {
            console.log('Loading Google module: ' + module);
            $.extend(options, {
                callback: function() {
                    instance.google_modules[module].resolve();
                }
            });
            google.load(module, version, options);
        });
        return instance.google_modules[module];
    }

    // GET JQUERY UI MAP

    // XXXvlab: should implement a full lib of dynamic js loading.
    function ensure_jquery_ui_map_loaded() {
        if (typeof(instance.jquery_ui_map_loaded) !== "undefined") {
            // please wait until the first call finishes:
            return instance.jquery_ui_map_loaded;
        }

        instance.jquery_ui_map_loaded = $.Deferred();
        console.log('Loading jquery.ui.map.js');
        $.getScript('/web_google_map/static/lib/js/jquery.ui.map.js',
                    function() {
                        instance.jquery_ui_map_loaded.resolve();
                    });
        return instance.jquery_ui_map_loaded;
    }
    /**
     * Adds a marker to existing google map by location object.
     */
    function _add_marker_by_location($gmap, location, options) {
        options = options || {};
        var gpos = new google.maps.LatLng(location.lat, location.lng);
        $.extend(options, {
            position: gpos
        });
        $gmap.gmap('addBounds', gpos);
        return $gmap.gmap('addMarker', options);
    }

    /**
     * Adds a marker to existing google map by place (a single string address)
     * This includes geocoding the address.
     */
    function _add_marker_by_place ($gmap, place, options) {
        var def = $.Deferred();
        geocode_place(place).then(function (location) {
            marker = _add_marker_by_location($gmap, location, options);
            def.resolve(marker);
        });
        return def.promise();
    }
    /**
     * Returns a float from an unspecified typed value.
     */
    function getFixedValue(value) {
        try {
            value = value.toString();
            if (value === "")
                return 0;
            return parseFloat(value.replace(",", "."));
        } catch(e) {
            console.log(e);
        }
    }

instance.web.views.add('map', 'instance.web_google.MapView');

instance.web_google.MapView = instance.web.View.extend({
    display_name: _lt('Map'),
    template: "MapView",
    view_type: "map",
    map: 'openerp.web_google.map.MapView',
    
    
    init: function() {
        var self = this;
        this._super.apply(this, arguments);
        var icon = '';

    },
                                                            // LOAD MAP VIEW 
    view_loading: function() {
        this.edit_mode = !this.get('effective_readonly');
        this.$canvas = this.$el.find("#map2");
        $("div#pick").addClass("none");
        this.$canvas[0].offsetWidth = 0;
        this.draw_map();
        var self = this;
        this.lines = new instance.web.Model('crm.lead');
        $( ".close" ).click(function() {
            $("div.showact").hide();
        });
        this.waypoints = [];

                        // Demo in_progress Clickkkk

        this.$el.find('#in_progress').on('click', function () {
            $('.btn.btn-primary.active').removeClass('active');
            $('.btn.btn-default.active').removeClass('active');
            $("#pick").addClass("none","1000");
            $('#in_progress').addClass("active");
            icon = 'http://maps.google.com/mapfiles/ms/icons/green-dot.png';
            var defs = [];
            self.waypoints = [];
            self.lines.call('search', [[['type','=','opportunity']]])
            .then(function(results){
                _.each(results, function(val, index){
                    defs.push(new instance.web.Model('crm.lead').call('read', [[val], ['city', 'country_id',]], {})
                        .then(function(result){
                            self.waypoints.push(result[0]);
                        }));
                });
                $.when.apply($, defs).then(function(){
                    self.get_ltlg(self.waypoints);
                });
            });
        });

                     // LEads OPEN

        this.$el.find('#leads').on('click', function () {
            $('.btn.btn-primary.active').removeClass('active');
            $('.btn.btn-default.active').removeClass('active');
            $('#leads').addClass("active");
            $("#pick").addClass("none","1000");
            icon = 'http://maps.google.com/mapfiles/ms/icons/red-dot.png';
            var defs = [];
            self.waypoints = [];
            self.lines.call('search', [[['type','=','lead']]])
            .then(function(results){
                _.each(results, function(val, index){
                    defs.push(new instance.web.Model('crm.lead').call('read', [[val], ['city', 'country_id', 'company_id']], {})
                        .then(function(result){
                            self.waypoints.push(result[0]);
                        }));
                });
                $.when.apply($, defs).then(function(){
                    self.get_ltlg(self.waypoints);
                });
            });
        });


        this.appo = new instance.web.Model('calendar.event');

                        // APPOINMENTS OPEN

        this.$el.find('#appoinments').on('click', function () {
            $('.btn.btn-primary.active').removeClass('active');
            $('.btn.btn-default.active').removeClass('active');
            $('#appoinments').addClass("active");
            $("#pick").addClass("none","1000");
            icon = 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png';
            var defs = [];
            self.waypoints = [];
            self.appo.call('search', [[]])
            .then(function(results){
                _.each(results, function(val, index){
                    defs.push(new instance.web.Model('calendar.event').call('read', [[val], ['city', 'country_id']], {})
                        .then(function(result){
                            self.waypoints.push(result[0]);
                        }));
                });
                $.when.apply($, defs).then(function(){
                    self.get_ltlg(self.waypoints);
                });
            });
        });


        this.customer = new instance.web.Model('res.partner');

                    // CUSTOMERS OPEN

        this.$el.on('click', '#customers', function () {
            $('.btn.btn-primary.active').removeClass('active');
            $('.btn.btn-default.active').removeClass('active');
            $('#customers').addClass("active");
            $("#pick").addClass("none","1000");
            var defs = [];
            icon = 'http://maps.google.com/mapfiles/ms/icons/purple-dot.png';
            self.waypoints = [];
            self.customer.call('search', [[['customer','=', 'TRUE']]])
            .then(function(results){
                _.each(results, function(val, index){
                    defs.push(new instance.web.Model('res.partner').call('read', [[val], ['city', 'state_id','country_id']], {})
                        .then(function(result){
                            self.waypoints.push(result[0]);
                        }));
                });
                $.when.apply($, defs).then(function(){
                    self.get_ltlg(self.waypoints);
                });
            });
        });


                                    //   FILTERS   // 

                                    // TODAY FILTER FOR LEAD , OPPORTUNITIES , DEMO IN PROGRESS , AND CUSTOMERS. //

        this.$el.on('click','#today', function(){
            $('.btn.btn-primary.active').removeClass('active');
            today = new Date();
            var dateString = today.format("Y-m-d");
            $("#pick").addClass("none","1000");
            if( $('.btn.btn-default.active').length !== 0 ){
                $('#today').addClass("active");
                if ($('.btn.btn-default.active')[0].id == "leads"){
                    var defs = [];
                    icon = 'http://maps.google.com/mapfiles/ms/icons/red-dot.png';
                    self.waypoints = [];
                    new instance.web.Model('crm.lead').call('search', [[['type','=','lead']]])
                    .then(function(results){
                        _.each(results, function(val, index){
                            defs.push(new instance.web.Model('crm.lead').call('read', [[val], ['city', 'state_id','country_id','create_date']], {})
                                .then(function(result){
                                    if(result[0].create_date.split(' ')[0] == dateString){
                                        self.waypoints.push(result[0]);
                                    }
                                }));
                        });
                        $.when.apply($, defs).then(function(){
                            self.get_ltlg(self.waypoints);
                        });
                    });
                }else if ($('.btn.btn-default.active')[0].id == "appoinments") {
                    var defs = [];
                    icon = 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png';
                    self.waypoints = [];
                    new instance.web.Model('calendar.event').call('search', [[]])
                    .then(function(results){
                        _.each(results, function(val, index){
                            defs.push(new instance.web.Model('calendar.event').call('read', [[val], ['city', 'state_id','country_id','create_date']], {})
                                .then(function(result){
                                    if(result[0].create_date.split(' ')[0] == dateString){
                                        self.waypoints.push(result[0]);
                                    }
                                }));
                        });
                        $.when.apply($, defs).then(function(){
                            self.get_ltlg(self.waypoints);
                        });
                    });
                }else if ($('.btn.btn-default.active')[0].id == "in_progress"){
                    var defs = [];
                    icon = 'http://maps.google.com/mapfiles/ms/icons/green-dot.png';
                    self.waypoints = [];
                    new instance.web.Model('crm.lead').call('search', [[['type','=','opportunity']]])
                    .then(function(results){
                        _.each(results, function(val, index){
                            defs.push(new instance.web.Model('crm.lead').call('read', [[val], ['city', 'state_id','country_id','create_date']], {})
                                .then(function(result){
                                    if(result[0].create_date.split(' ')[0] == dateString){
                                        self.waypoints.push(result[0]);
                                    }
                                }));
                        });
                        $.when.apply($, defs).then(function(){
                            self.get_ltlg(self.waypoints);
                        });
                    });
                }else if ($('.btn.btn-default.active')[0].id == "customers"){
                    this.customer = new instance.web.Model('res.partner');
                    var defs = [];
                    icon = 'http://maps.google.com/mapfiles/ms/icons/purple-dot.png';
                    self.waypoints = [];
                    new instance.web.Model('res.partner').call('search', [[['customer','=','TRUE']]])
                    .then(function(results){
                        _.each(results, function(val, index){
                            defs.push(new instance.web.Model('res.partner').call('read', [[val], ['city', 'state_id','country_id','create_date']], {})
                                .then(function(result){
                                    if(result[0].create_date.split(' ')[0] == dateString){
                                        self.waypoints.push(result[0]);
                                    }
                                }));
                        });
                        $.when.apply($, defs).then(function(){
                            self.get_ltlg(self.waypoints);
                        });
                    });
                }else{
                    console.log('please select the category...');
                }
            }else{
                $('#show_winn').show();
                $('#show_win').show();
            }

        });


                                //   FILTERS   // 

                                // YESTERDAY FILTER FOR LEAD , OPPORTUNITIES , DEMO IN PROGRESS , AND CUSTOMERS. //



        this.$el.on('click','#yesterday', function(){
            $('.btn.btn-primary.active').removeClass('active');
            $("#pick").addClass("none","1000");
            today = new Date();
            
            today.setDate(today.getDate() - 1);
            var dateString = today.format("Y-m-d");

            if( $('.btn.btn-default.active').length !== 0 ){
                $('#yesterday').addClass("active");
                if ($('.btn.btn-default.active')[0].id == "leads"){
                    var defs = [];
                    icon = 'http://maps.google.com/mapfiles/ms/icons/red-dot.png';
                    self.waypoints = [];
                    new instance.web.Model('crm.lead').call('search', [[['type','=','lead']]])
                    .then(function(results){
                        _.each(results, function(val, index){
                            defs.push(new instance.web.Model('crm.lead').call('read', [[val], ['city', 'state_id','country_id','create_date']], {})
                                .then(function(result){
                                    if(result[0].create_date.split(' ')[0] == dateString){
                                        self.waypoints.push(result[0]);
                                    }
                                }));
                        });
                        $.when.apply($, defs).then(function(){
                            self.get_ltlg(self.waypoints);
                        });
                    });
                }else if ($('.btn.btn-default.active')[0].id == "appoinments") {
                    var defs = [];
                    icon = 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png';
                    self.waypoints = [];
                    new instance.web.Model('calendar.event').call('search', [[]])
                    .then(function(results){
                        _.each(results, function(val, index){
                            defs.push(new instance.web.Model('calendar.event').call('read', [[val], ['city', 'state_id','country_id','create_date']], {})
                                .then(function(result){
                                    if(result[0].create_date.split(' ')[0] == dateString){
                                        self.waypoints.push(result[0]);
                                    }
                                }));
                        });
                        $.when.apply($, defs).then(function(){
                            self.get_ltlg(self.waypoints);
                        });
                    });
                }else if ($('.btn.btn-default.active')[0].id == "in_progress"){
                    var defs = [];
                    icon = 'http://maps.google.com/mapfiles/ms/icons/green-dot.png';
                    self.waypoints = [];
                    new instance.web.Model('crm.lead').call('search', [[['type','=','opportunity']]])
                    .then(function(results){
                        _.each(results, function(val, index){
                            defs.push(new instance.web.Model('crm.lead').call('read', [[val], ['city', 'state_id','country_id','create_date']], {})
                                .then(function(result){
                                    if(result[0].create_date.split(' ')[0] == dateString){
                                        self.waypoints.push(result[0]);
                                    }
                                }));
                        });
                        $.when.apply($, defs).then(function(){
                            self.get_ltlg(self.waypoints);
                        });
                    });
                }else if ($('.btn.btn-default.active')[0].id == "customers"){
                    this.customer = new instance.web.Model('res.partner');
                    var defs = [];
                    icon = 'http://maps.google.com/mapfiles/ms/icons/purple-dot.png';
                    self.waypoints = [];
                    new instance.web.Model('res.partner').call('search', [[['customer','=','TRUE']]])
                    .then(function(results){
                        _.each(results, function(val, index){
                            defs.push(new instance.web.Model('res.partner').call('read', [[val], ['city', 'state_id','country_id','create_date']], {})
                                .then(function(result){
                                    if(result[0].create_date.split(' ')[0] == dateString){
                                        self.waypoints.push(result[0]);
                                    }
                                }));
                        });
                        $.when.apply($, defs).then(function(){
                            self.get_ltlg(self.waypoints);
                        });
                    });
                }else{
                    console.log('please select the category...');
                }
            }else{
                $('#show_winn').show();
                $('#show_win').show();
            }
        });

                        //   FILTERS   // 

                        // PREVIOUS WEEK FILTER FOR LEAD , OPPORTUNITIES , DEMO IN PROGRESS , AND CUSTOMERS. //




        this.$el.on('click','#preweek', function(){
            $('.btn.btn-primary.active').removeClass('active');
            $("#pick").addClass("none","1000");
            var beforeOneWeek = new Date(new Date().getTime() - 60 * 60 * 24 * 7 * 1000)
            var beforeOneWeek2 = new Date(beforeOneWeek);
            day = beforeOneWeek.getDay()
            diffToMonday = beforeOneWeek.getDate() - day + (day === 0 ? -6 : 1)
            lastMonday = new Date(beforeOneWeek.setDate(diffToMonday))
            lastSunday = new Date(beforeOneWeek2.setDate(diffToMonday + 6));
            
            startDate = lastMonday.format("Y-m-d");
            endDate = lastSunday.format("Y-m-d");

            if( $('.btn.btn-default.active').length !== 0 ){
                $('#preweek').addClass("active");
                if ($('.btn.btn-default.active')[0].id == "leads"){
                    var defs = [];
                    icon = 'http://maps.google.com/mapfiles/ms/icons/red-dot.png';
                    self.waypoints = [];
                    new instance.web.Model('crm.lead').call('search', [[['type','=','lead']]])
                    .then(function(results){
                        _.each(results, function(val, index){
                            defs.push(new instance.web.Model('crm.lead').call('read', [[val], ['city', 'state_id','country_id','create_date']], {})
                                .then(function(result){
                                    if(result[0].create_date.split(' ')[0] >= startDate && result[0].create_date.split(' ')[0] <= endDate){
                                        self.waypoints.push(result[0]);
                                    }
                                }));
                        });
                        $.when.apply($, defs).then(function(){
                            self.get_ltlg(self.waypoints);
                        });
                    });
                }else if ($('.btn.btn-default.active')[0].id == "appoinments") {
                    var defs = [];
                    icon = 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png';
                    self.waypoints = [];
                    new instance.web.Model('calendar.event').call('search', [[]])
                    .then(function(results){
                        _.each(results, function(val, index){
                            defs.push(new instance.web.Model('calendar.event').call('read', [[val], ['city', 'state_id','country_id','create_date']], {})
                                .then(function(result){
                                    if(result[0].create_date.split(' ')[0] >= startDate && result[0].create_date.split(' ')[0] <= endDate){
                                        self.waypoints.push(result[0]);
                                    }
                                }));
                        });
                        $.when.apply($, defs).then(function(){
                            self.get_ltlg(self.waypoints);
                        });
                    });
                }else if ($('.btn.btn-default.active')[0].id == "in_progress"){
                    var defs = [];
                    icon = 'http://maps.google.com/mapfiles/ms/icons/green-dot.png';
                    self.waypoints = [];
                    new instance.web.Model('crm.lead').call('search', [[['type','=','opportunity']]])
                    .then(function(results){
                        _.each(results, function(val, index){
                            defs.push(new instance.web.Model('crm.lead').call('read', [[val], ['city', 'state_id','country_id','create_date']], {})
                                .then(function(result){
                                    if(result[0].create_date.split(' ')[0] >= startDate && result[0].create_date.split(' ')[0] <= endDate){
                                        self.waypoints.push(result[0]);
                                    }
                                }));
                        });
                        $.when.apply($, defs).then(function(){
                            self.get_ltlg(self.waypoints);
                        });
                    });
                }else if ($('.btn.btn-default.active')[0].id == "customers"){
                    this.customer = new instance.web.Model('res.partner');
                    var defs = [];
                    icon = 'http://maps.google.com/mapfiles/ms/icons/purple-dot.png';
                    self.waypoints = [];
                    new instance.web.Model('res.partner').call('search', [[['customer','=','TRUE']]])
                    .then(function(results){
                        _.each(results, function(val, index){
                            defs.push(new instance.web.Model('res.partner').call('read', [[val], ['city', 'state_id','country_id','create_date']], {})
                                .then(function(result){
                                    if(result[0].create_date.split(' ')[0] >= startDate && result[0].create_date.split(' ')[0] <= endDate){
                                        self.waypoints.push(result[0]);
                                    }
                                }));
                        });
                        $.when.apply($, defs).then(function(){
                            self.get_ltlg(self.waypoints);
                        });
                    });
                }else{
                    console.log('please select the category...');
                }
            }else{
                $('#show_winn').show();
                $('#show_win').show();
            }
        });


                        //   FILTERS   // 

                        // PREVIOUS MONTH FILTER FOR LEAD , OPPORTUNITIES , DEMO IN PROGRESS , AND CUSTOMERS. //

        this.$el.on('click','#premonth', function(){
            $('.btn.btn-primary.active').removeClass('active');
            $("#pick").addClass("none","1000");
            var date = new Date();
            var firstDay = new Date(date.getFullYear(), date.getMonth()-1, 1);
            var lastDay = new Date(date.getFullYear(), date.getMonth(), 0);
            startDate = firstDay.format("Y-m-d");
            endDate = lastDay.format("Y-m-d");

            if( $('.btn.btn-default.active').length !== 0 ){
                $('#premonth').addClass("active");
                if ($('.btn.btn-default.active')[0].id == "leads"){
                    var defs = [];
                    icon = 'http://maps.google.com/mapfiles/ms/icons/red-dot.png';
                    self.waypoints = [];
                    new instance.web.Model('crm.lead').call('search', [[['type','=','lead']]])
                    .then(function(results){
                        _.each(results, function(val, index){
                            defs.push(new instance.web.Model('crm.lead').call('read', [[val], ['city', 'state_id','country_id','create_date']], {})
                                .then(function(result){
                                    if(result[0].create_date.split(' ')[0] >= startDate && result[0].create_date.split(' ')[0] <= endDate){
                                        self.waypoints.push(result[0]);
                                    }
                                }));
                        });
                        $.when.apply($, defs).then(function(){
                            self.get_ltlg(self.waypoints);
                        });
                    });
                }else if ($('.btn.btn-default.active')[0].id == "appoinments") {
                    var defs = [];
                    icon = 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png';
                    self.waypoints = [];
                    new instance.web.Model('calendar.event').call('search', [[]])
                    .then(function(results){
                        _.each(results, function(val, index){
                            defs.push(new instance.web.Model('calendar.event').call('read', [[val], ['city', 'state_id','country_id','create_date']], {})
                                .then(function(result){
                                    if(result[0].create_date.split(' ')[0] >= startDate && result[0].create_date.split(' ')[0] <= endDate){
                                        self.waypoints.push(result[0]);
                                    }
                                }));
                        });
                        $.when.apply($, defs).then(function(){
                            self.get_ltlg(self.waypoints);
                        });
                    });
                }else if ($('.btn.btn-default.active')[0].id == "in_progress"){
                    var defs = [];
                    icon = 'http://maps.google.com/mapfiles/ms/icons/green-dot.png';
                    self.waypoints = [];
                    new instance.web.Model('crm.lead').call('search', [[['type','=','opportunity']]])
                    .then(function(results){
                        _.each(results, function(val, index){
                            defs.push(new instance.web.Model('crm.lead').call('read', [[val], ['city', 'state_id','country_id','create_date']], {})
                                .then(function(result){
                                    if(result[0].create_date.split(' ')[0] >= startDate && result[0].create_date.split(' ')[0] <= endDate){
                                        self.waypoints.push(result[0]);
                                    }
                                }));
                        });
                        $.when.apply($, defs).then(function(){
                            self.get_ltlg(self.waypoints);
                        });
                    });
                }else if ($('.btn.btn-default.active')[0].id == "customers"){
                    this.customer = new instance.web.Model('res.partner');
                    var defs = [];
                    icon = 'http://maps.google.com/mapfiles/ms/icons/purple-dot.png';
                    self.waypoints = [];
                    new instance.web.Model('res.partner').call('search', [[['customer','=','TRUE']]])
                    .then(function(results){
                        _.each(results, function(val, index){
                            defs.push(new instance.web.Model('res.partner').call('read', [[val], ['city', 'state_id','country_id','create_date']], {})
                                .then(function(result){
                                    if(result[0].create_date.split(' ')[0] >= startDate && result[0].create_date.split(' ')[0] <= endDate){
                                        self.waypoints.push(result[0]);
                                    }
                                }));
                        });
                        $.when.apply($, defs).then(function(){
                            self.get_ltlg(self.waypoints);
                        });
                    });
                }else{
                    console.log('please select the category...');
                }
            }else{
                $('#show_winn').show();
                $('#show_win').show();
            }

        });


                        //   FILTERS   // 

                        // LAST 3 MONTH FILTER FOR LEAD , OPPORTUNITIES , DEMO IN PROGRESS , AND CUSTOMERS. //



        this.$el.on('click','#last3month', function(){
            $('.btn.btn-primary.active').removeClass('active');
            $("#pick").addClass("none","1000");
            
            var date = new Date();
            var firstDay = new Date(date.getFullYear(), date.getMonth()-3, 1);
            var lastDay = new Date(date.getFullYear(), date.getMonth(), 0);
            startDate = firstDay.format("Y-m-d");
            endDate = lastDay.format("Y-m-d");

            if( $('.btn.btn-default.active').length !== 0 ){
                $('#last3month').addClass("active");
                if ($('.btn.btn-default.active')[0].id == "leads"){
                    var defs = [];
                    icon = 'http://maps.google.com/mapfiles/ms/icons/red-dot.png';
                    self.waypoints = [];
                    new instance.web.Model('crm.lead').call('search', [[['type','=','lead']]])
                    .then(function(results){
                        _.each(results, function(val, index){
                            defs.push(new instance.web.Model('crm.lead').call('read', [[val], ['city', 'state_id','country_id','create_date']], {})
                                .then(function(result){
                                    if(result[0].create_date.split(' ')[0] >= startDate && result[0].create_date.split(' ')[0] <= endDate){
                                        self.waypoints.push(result[0]);
                                    }
                                }));
                        });
                        $.when.apply($, defs).then(function(){
                            self.get_ltlg(self.waypoints);
                        });
                    });
                }else if ($('.btn.btn-default.active')[0].id == "appoinments") {
                    var defs = [];
                    icon = 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png';
                    self.waypoints = [];
                    new instance.web.Model('calendar.event').call('search', [[]])
                    .then(function(results){
                        _.each(results, function(val, index){
                            defs.push(new instance.web.Model('calendar.event').call('read', [[val], ['city', 'state_id','country_id','create_date']], {})
                                .then(function(result){
                                    if(result[0].create_date.split(' ')[0] >= startDate && result[0].create_date.split(' ')[0] <= endDate){
                                        self.waypoints.push(result[0]);
                                    }
                                }));
                        });
                        $.when.apply($, defs).then(function(){
                            self.get_ltlg(self.waypoints);
                        });
                    });
                }else if ($('.btn.btn-default.active')[0].id == "in_progress"){
                    var defs = [];
                    icon = 'http://maps.google.com/mapfiles/ms/icons/green-dot.png';
                    self.waypoints = [];
                    new instance.web.Model('crm.lead').call('search', [[['type','=','opportunity']]])
                    .then(function(results){
                        _.each(results, function(val, index){
                            defs.push(new instance.web.Model('crm.lead').call('read', [[val], ['city', 'state_id','country_id','create_date']], {})
                                .then(function(result){
                                    if(result[0].create_date.split(' ')[0] >= startDate && result[0].create_date.split(' ')[0] <= endDate){
                                        self.waypoints.push(result[0]);
                                    }
                                }));
                        });
                        $.when.apply($, defs).then(function(){
                            self.get_ltlg(self.waypoints);
                        });
                    });
                }else if ($('.btn.btn-default.active')[0].id == "customers"){
                    this.customer = new instance.web.Model('res.partner');
                    var defs = [];
                    icon = 'http://maps.google.com/mapfiles/ms/icons/purple-dot.png';
                    self.waypoints = [];
                    new instance.web.Model('res.partner').call('search', [[['customer','=','TRUE']]])
                    .then(function(results){
                        _.each(results, function(val, index){
                            defs.push(new instance.web.Model('res.partner').call('read', [[val], ['city', 'state_id','country_id','create_date']], {})
                                .then(function(result){
                                    if(result[0].create_date.split(' ')[0] >= startDate && result[0].create_date.split(' ')[0] <= endDate){
                                        self.waypoints.push(result[0]);
                                    }
                                }));
                        });
                        $.when.apply($, defs).then(function(){
                            self.get_ltlg(self.waypoints);
                        });
                    });
                }else{
                    console.log('please select the category...');
                }
            }else{
                $('#show_winn').show();
                $('#show_win').show();
            }
        });


                //   FILTERS   // 

                // LAST 6 MONTH FILTER FOR LEAD , OPPORTUNITIES , DEMO IN PROGRESS , AND CUSTOMERS. //


        this.$el.on('click','#last6month', function(){
            $('.btn.btn-primary.active').removeClass('active');
            $("#pick").addClass("none","1000");

            var date = new Date();
            var firstDay = new Date(date.getFullYear(), date.getMonth()-6, 1);
            var lastDay = new Date(date.getFullYear(), date.getMonth(), 0);
            startDate = firstDay.format("Y-m-d");
            endDate = lastDay.format("Y-m-d");

            if( $('.btn.btn-default.active').length !== 0 ){
                $('#last6month').addClass("active");
                if ($('.btn.btn-default.active')[0].id == "leads"){
                    var defs = [];
                    icon = 'http://maps.google.com/mapfiles/ms/icons/red-dot.png';
                    self.waypoints = [];
                    new instance.web.Model('crm.lead').call('search', [[['type','=','lead']]])
                    .then(function(results){
                        _.each(results, function(val, index){
                            defs.push(new instance.web.Model('crm.lead').call('read', [[val], ['city', 'state_id','country_id','create_date']], {})
                                .then(function(result){
                                    if(result[0].create_date.split(' ')[0] >= startDate && result[0].create_date.split(' ')[0] <= endDate){
                                        self.waypoints.push(result[0]);
                                    }
                                }));
                        });
                        $.when.apply($, defs).then(function(){
                            self.get_ltlg(self.waypoints);
                        });
                    });
                }else if ($('.btn.btn-default.active')[0].id == "appoinments") {
                    var defs = [];
                    icon = 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png';
                    self.waypoints = [];
                    new instance.web.Model('calendar.event').call('search', [[]])
                    .then(function(results){
                        _.each(results, function(val, index){
                            defs.push(new instance.web.Model('calendar.event').call('read', [[val], ['city', 'state_id','country_id','create_date']], {})
                                .then(function(result){
                                    if(result[0].create_date.split(' ')[0] >= startDate && result[0].create_date.split(' ')[0] <= endDate){
                                        self.waypoints.push(result[0]);
                                    }
                                }));
                        });
                        $.when.apply($, defs).then(function(){
                            self.get_ltlg(self.waypoints);
                        });
                    });
                }else if ($('.btn.btn-default.active')[0].id == "in_progress"){
                    var defs = [];
                    icon = 'http://maps.google.com/mapfiles/ms/icons/green-dot.png';
                    self.waypoints = [];
                    new instance.web.Model('crm.lead').call('search', [[['type','=','opportunity']]])
                    .then(function(results){
                        _.each(results, function(val, index){
                            defs.push(new instance.web.Model('crm.lead').call('read', [[val], ['city', 'state_id','country_id','create_date']], {})
                                .then(function(result){
                                    if(result[0].create_date.split(' ')[0] >= startDate && result[0].create_date.split(' ')[0] <= endDate){
                                        self.waypoints.push(result[0]);
                                    }
                                }));
                        });
                        $.when.apply($, defs).then(function(){
                            self.get_ltlg(self.waypoints);
                        });
                    });
                }else if ($('.btn.btn-default.active')[0].id == "customers"){
                    this.customer = new instance.web.Model('res.partner');
                    var defs = [];
                    icon = 'http://maps.google.com/mapfiles/ms/icons/purple-dot.png';
                    self.waypoints = [];
                    new instance.web.Model('res.partner').call('search', [[['customer','=','TRUE']]])
                    .then(function(results){
                        _.each(results, function(val, index){
                            defs.push(new instance.web.Model('res.partner').call('read', [[val], ['city', 'state_id','country_id','create_date']], {})
                                .then(function(result){
                                    if(result[0].create_date.split(' ')[0] >= startDate && result[0].create_date.split(' ')[0] <= endDate){
                                        self.waypoints.push(result[0]);
                                    }
                                }));
                        });
                        $.when.apply($, defs).then(function(){
                            self.get_ltlg(self.waypoints);
                        });
                    });
                }else{
                    console.log('please select the category...');
                }
            }else{
                $('#show_winn').show();
                $('#show_win').show();
            }
        });

                        //   FILTERS   // 

                        // LAST YEAR FILTER FOR LEAD , OPPORTUNITIES , DEMO IN PROGRESS , AND CUSTOMERS. //


        this.$el.on('click','#lastyear', function(){
            $('.btn.btn-primary.active').removeClass('active');
            $("#pick").addClass("none","1000");
            
            var date = new Date();
            var firstDay = new Date(date.getFullYear()-1, date.getMonth(), 1);
            var lastDay = date;
            startDate = firstDay.format("Y-m-d");
            endDate = lastDay.format("Y-m-d");

            if( $('.btn.btn-default.active').length !== 0 ){
                $('#lastyear').addClass("active");
                if ($('.btn.btn-default.active')[0].id == "leads"){
                    var defs = [];
                    icon = 'http://maps.google.com/mapfiles/ms/icons/red-dot.png';
                    self.waypoints = [];
                    new instance.web.Model('crm.lead').call('search', [[['type','=','lead']]])
                    .then(function(results){
                        _.each(results, function(val, index){
                            defs.push(new instance.web.Model('crm.lead').call('read', [[val], ['city', 'state_id','country_id','create_date']], {})
                                .then(function(result){
                                    if(result[0].create_date.split(' ')[0] >= startDate && result[0].create_date.split(' ')[0] <= endDate){
                                        self.waypoints.push(result[0]);
                                    }
                                }));
                        });
                        $.when.apply($, defs).then(function(){
                            self.get_ltlg(self.waypoints);
                        });
                    });
                }else if ($('.btn.btn-default.active')[0].id == "appoinments") {
                    var defs = [];
                    icon = 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png';
                    self.waypoints = [];
                    new instance.web.Model('calendar.event').call('search', [[]])
                    .then(function(results){
                        _.each(results, function(val, index){
                            defs.push(new instance.web.Model('calendar.event').call('read', [[val], ['city', 'state_id','country_id','create_date']], {})
                                .then(function(result){
                                    if(result[0].create_date.split(' ')[0] >= startDate && result[0].create_date.split(' ')[0] <= endDate){
                                        self.waypoints.push(result[0]);
                                    }
                                }));
                        });
                        $.when.apply($, defs).then(function(){
                            self.get_ltlg(self.waypoints);
                        });
                    });
                }else if ($('.btn.btn-default.active')[0].id == "in_progress"){
                    var defs = [];
                    icon = 'http://maps.google.com/mapfiles/ms/icons/green-dot.png';
                    self.waypoints = [];
                    new instance.web.Model('crm.lead').call('search', [[['type','=','opportunity']]])
                    .then(function(results){
                        _.each(results, function(val, index){
                            defs.push(new instance.web.Model('crm.lead').call('read', [[val], ['city', 'state_id','country_id','create_date']], {})
                                .then(function(result){
                                    if(result[0].create_date.split(' ')[0] >= startDate && result[0].create_date.split(' ')[0] <= endDate){
                                        self.waypoints.push(result[0]);
                                    }
                                }));
                        });
                        $.when.apply($, defs).then(function(){
                            self.get_ltlg(self.waypoints);
                        });
                    });
                }else if ($('.btn.btn-default.active')[0].id == "customers"){
                    this.customer = new instance.web.Model('res.partner');
                    var defs = [];
                    icon = 'http://maps.google.com/mapfiles/ms/icons/purple-dot.png';
                    self.waypoints = [];
                    new instance.web.Model('res.partner').call('search', [[['customer','=','TRUE']]])
                    .then(function(results){
                        _.each(results, function(val, index){
                            defs.push(new instance.web.Model('res.partner').call('read', [[val], ['city', 'state_id','country_id','create_date']], {})
                                .then(function(result){
                                    if(result[0].create_date.split(' ')[0] >= startDate && result[0].create_date.split(' ')[0] <= endDate){
                                        self.waypoints.push(result[0]);
                                    }
                                }));
                        });
                        $.when.apply($, defs).then(function(){
                            self.get_ltlg(self.waypoints);
                        });
                    });
                }else{
                    console.log('please select the category...');
                }
            }else{
                $('#show_winn').show();
                $('#show_win').show();
            }
        });


                        //   FILTERS   // 

                        // CUSTOM FILTER FOR LEAD , OPPORTUNITIES , DEMO IN PROGRESS , AND CUSTOMERS. //


        this.$el.on('click','#filter_date', function(){
            $('.btn.btn-primary.active').removeClass('active');
            
            var startDate = $('#from_date')[0].value;
            var endDate = $('#to_date')[0].value;
            
            if( $('.btn.btn-default.active').length !== 0 ){
                if ($('.btn.btn-default.active')[0].id == "leads"){
                    var defs = [];
                    icon = 'http://maps.google.com/mapfiles/ms/icons/red-dot.png';
                    self.waypoints = [];
                    new instance.web.Model('crm.lead').call('search', [[['type','=','lead']]])
                    .then(function(results){
                        _.each(results, function(val, index){
                            defs.push(new instance.web.Model('crm.lead').call('read', [[val], ['city', 'state_id','country_id','create_date']], {})
                                .then(function(result){
                                    if(result[0].create_date.split(' ')[0] >= startDate && result[0].create_date.split(' ')[0] <= endDate){
                                        self.waypoints.push(result[0]);
                                    }
                                }));
                        });
                        $.when.apply($, defs).then(function(){
                            self.get_ltlg(self.waypoints);
                        });
                    });
                }else if ($('.btn.btn-default.active')[0].id == "appoinments") {
                    var defs = [];
                    icon = 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png';
                    self.waypoints = [];
                    new instance.web.Model('calendar.event').call('search', [[]])
                    .then(function(results){
                        _.each(results, function(val, index){
                            defs.push(new instance.web.Model('calendar.event').call('read', [[val], ['city', 'state_id','country_id','create_date']], {})
                                .then(function(result){
                                    if(result[0].create_date.split(' ')[0] >= startDate && result[0].create_date.split(' ')[0] <= endDate){
                                        self.waypoints.push(result[0]);
                                    }
                                }));
                        });
                        $.when.apply($, defs).then(function(){
                            self.get_ltlg(self.waypoints);
                        });
                    });
                }else if ($('.btn.btn-default.active')[0].id == "in_progress"){
                    var defs = [];
                    icon = 'http://maps.google.com/mapfiles/ms/icons/green-dot.png';
                    self.waypoints = [];
                    new instance.web.Model('crm.lead').call('search', [[['type','=','opportunity']]])
                    .then(function(results){
                        _.each(results, function(val, index){
                            defs.push(new instance.web.Model('crm.lead').call('read', [[val], ['city', 'state_id','country_id','create_date']], {})
                                .then(function(result){
                                    if(result[0].create_date.split(' ')[0] >= startDate && result[0].create_date.split(' ')[0] <= endDate){
                                        self.waypoints.push(result[0]);
                                    }
                                }));
                        });
                        $.when.apply($, defs).then(function(){
                            self.get_ltlg(self.waypoints);
                        });
                    });
                }else if ($('.btn.btn-default.active')[0].id == "customers"){
                    this.customer = new instance.web.Model('res.partner');
                    var defs = [];
                    icon = 'http://maps.google.com/mapfiles/ms/icons/purple-dot.png';
                    self.waypoints = [];
                    new instance.web.Model('res.partner').call('search', [[['customer','=','TRUE']]])
                    .then(function(results){
                        _.each(results, function(val, index){
                            defs.push(new instance.web.Model('res.partner').call('read', [[val], ['city', 'state_id','country_id','create_date']], {})
                                .then(function(result){
                                    if(result[0].create_date.split(' ')[0] >= startDate && result[0].create_date.split(' ')[0] <= endDate){
                                        self.waypoints.push(result[0]);
                                    }
                                }));
                        });
                        $.when.apply($, defs).then(function(){
                            self.get_ltlg(self.waypoints);
                        });
                    });
                }else{
                    console.log('please select the category...');
                }
            }else{
                $('#show_winn').show();
                $('#show_win').show();
            }
            //$("#pick").addClass("none","1000");
        });

        this.$el.on('click','#advance', function(){
            $('.btn.btn-primary.active').removeClass('active');
            $("#pick").removeClass("none", "1000", "easeOutBounce");
            $('#advance').addClass("active");
        });
    },

    

    get_location: function() {
        var self = this;
        this.company = new instance.web.Model('res.company');
        var defs = [];
        icon = 'http://maps.google.com/mapfiles/ms/icons/yellow-dot.png';
        self.waypoints = [];
        this.company.call('search', [[]])
        .then(function(results){
            _.each(results, function(val, index){
                defs.push(new instance.web.Model('res.company').call('read', [[val], ['city', 'state_id','country_id']], {})
                    .then(function(result){
                        self.waypoints.push(result[0]);
                    }));
            });
            $.when.apply($, defs).then(function(){
                self.get_ltlg(self.waypoints);
            });
        });
    },

    google_ensure_map_loaded: function() {
        return google_ensure_module_loaded("maps", "3", {
            // Thanks: http://stackoverflow.com/questions/5296115/can-you-load-google-maps-api-v3-via-google-ajax-api-loader
            other_params: "sensor=false",
            async: 'true'});
    },

    draw_map: function () {
        var self = this;
        this.google_ensure_map_loaded().then(function() {

            var OPTIONS = {
                zoom: 16,
                mapTypeId: google.maps.MapTypeId.ROADMAP
            };
            try {
                var location = self.get_location();
            } catch (e) {
                console.log(e);
            }
        });
    },

    get_ltlg: function(res){
        var self = this;
        this.google_ensure_map_loaded().then(function() {
            this.country = new google.maps.LatLng(50, 0);
            var mapOptions = {
                    zoom:2,
                    center: this.country,
                    mapTypeId: google.maps.MapTypeId.ROADMAP
                };
            this.$canvas = self.$el.find("#map2");
            
            var map = new google.maps.Map(self.$canvas[0], mapOptions);
            map.setOptions({ minZoom: 2, maxZoom: 20 });
            var geocoder =  new google.maps.Geocoder();
            var infowindow = new google.maps.InfoWindow();
            var marker, i;
            for (var i=0;i<res.length;i++){
                if (res[i].city) {
                    geocoder.geocode({ 'address': res[i].city}, function(results, status) {
                        if (status == google.maps.GeocoderStatus.OK) {
                            var ltlg = results[0].geometry.location.lat() + " , " +results[0].geometry.location.lng();
                        }
                        if (ltlg){
                            var location = [ltlg];
                            for (i = 0; i < location.length; i++) {
                                var loc = location[0].split(",") ;
                                var point = new google.maps.LatLng(loc[0],loc[1]);
                                marker = new google.maps.Marker({
                                    position: point,
                                    icon: icon,
                                    map: map
                                });
                                //map.setCenter(point);
                                google.maps.event.addListener(marker, 'click', (function(marker, i) {
                                    return function() {
                                        infowindow.setContent(results[0].address_components[0].short_name  + "," + results[0].address_components[2].long_name);
                                        infowindow.open(map, marker);
                                    }
                                })(marker, i));
                            }
                        }
                    });
                } 
            }
        });
    },

});
    
    // instance.web_google.MapView = instance.web.View.extend({
    //     'map': 'openerp.web_google.map.MapView',
    // });
};
