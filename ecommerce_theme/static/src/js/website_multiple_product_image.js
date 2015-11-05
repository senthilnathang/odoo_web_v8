
$(document).ready(function ()
	{
		
			
	 $(".product_multi_img").click(function ()
			 {

				$('.zoomWindowContainer div').css('background', 'url(' + this.src +')');
				$('.product_detail_img').attr('src',this.src);
				     													     	
			 });
	 $(".product_main_multi_img").click(function ()
			 {
				$('.zoomWindowContainer div').css('background', 'url(' + this.src +')');
				$('.product_detail_img').attr('src',this.src);	
								     													     										     	
			 });
	 $(".product-zoom-image").hover(function ()
			 {
			s=document.getElementById('zoom_01').src;
			$('.zoomWindowContainer div').css('background', 'url(' + s +')');
			$('.product_detail_img').attr('src',this.src);								     													     										     	
			 });			 
			 			 	 
    $('.js_variant_change').bind('change',function () {
       var $ul = $(this).parents('ul.js_add_cart_variants:first');
        var $parent = $ul.closest('.js_product');
        var $product_id = $parent.find('input.product_id').first();
        var $price = $parent.find(".oe_price:first .oe_currency_value");
        var $default_price = $parent.find(".oe_default_price:first .oe_currency_value");
        var variant_ids = $ul.data("attribute_value_ids");
        var values = [];
        $parent.find('input.js_variant_change:checked, select.js_variant_change').each(function () {
            values.push(+$(this).val());
        });

        $parent.find("label").removeClass("text-muted css_not_available");

        var product_id = false;
        for (var k in variant_ids) {
            if (_.isEmpty(_.difference(variant_ids[k][1], values))) {
                product_id = variant_ids[k][0];
                break;
            }
        }
        if (product_id) {
        $('.product_main_multi_img').attr("src", "/website/image/product.product/" + product_id + "/image");
        $('.product_detail_img').attr("data-zoom-image", "/website/image/product.product/" + product_id + "/image");        
        } 
    });
    
    $('ul.js_add_cart_variants', '.oe_website_sale').each(function () {
        $('input.js_variant_change, select.js_variant_change', this).trigger('change');
    });

 $('#thumb-slider').owlCarousel({
    loop:false,
    margin:10,
    responsiveClass:true,
    items:4
})  


   // alert($(".product-image").width());
  $('.magnifier-preview').css('left',$('.product-image').width()+30);


});

$(window).resize(function(){
   $('.magnifier-preview').css('left',$('.product-image').width()+30);
}); 





