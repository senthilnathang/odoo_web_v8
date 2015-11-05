openerp.kingfisher = function(openerp) {
    var _t = openerp.web._t;

    openerp.web.list.Binary.include({
        placeholder: "/web/static/src/img/placeholder.png",
        _format: function (row_data, options) {
            var value = row_data[this.id].value;
            var download_url;
            if (value && value.substr(0, 10).indexOf(' ') == -1) {
                download_url = "data:image/png;base64," + value;
            } else {
                download_url = this.placeholder;
            } 
 			model=options.model
 			if (model=='product.images')
	            return _.template("<img width='50' height='50' src='<%-href%>'/>", {
	                href: download_url,
	            });
        var text = _t("Download");
        var value = row_data[this.id].value;
        if (!value) {
            return options.value_if_empty || '';
        }

        var download_url;
        if (value.substr(0, 10).indexOf(' ') == -1) {
            download_url = "data:application/octet-stream;base64," + value;
        } else {
            download_url = openerp.session.url('/web/binary/saveas', {model: options.model, field: this.id, id: options.id});
            if (this.filename) {
                download_url += '&filename_field=' + this.filename;
            }
        }
        if (this.filename && row_data[this.filename]) {
            text = _.str.sprintf(_t("Download \"%s\""), openerp.web.format_value(
                    row_data[this.filename].value, {type: 'char'}));
        }
        return _.template('<a href="<%-href%>"><%-text%></a> (<%-size%>)', {
            text: text,
            href: download_url,
            size: openerp.web.binary_to_binsize(value),
        });
        
        }

    });
}
