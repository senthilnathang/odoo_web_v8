
// Owl slider
$(document).ready(function(){


$('.oe_website_sale').each(function () {
    var oe_website_sale = this;


$(oe_website_sale).on("change", ".oe_cart input.js_quantity", function () {
		setTimeout("location.reload();", 1000);
});

$(oe_website_sale).on('click', 'a.js_add_cart_json_new', function (ev) {
        ev.preventDefault();
        var $link = $(ev.currentTarget);
        var $input = $link.parent().parent().find("input");        
        var value = parseInt(0, 10);
        var line_id = parseInt($input.data('line-id'),10);
        if (isNaN(value)) value = 0;
        openerp.jsonRpc("/shop/cart/update_json", 'call', {
            'line_id': line_id,
            'product_id': parseInt($input.data('product-id'),10),
            'set_qty': value})
	.then(function (data) {
                if (!data.quantity) {
                    location.reload();
                    return;
                }
	});
    });
});



  $('.owl-carousel').owlCarousel({
    loop:true,
    margin:30,
    responsiveClass:true,
    responsive:{
        0:{
            items:1,
            nav:false,
            dots:true
        },
        480:{
            items:2,
            nav:false,
            dots:true
        },
        768:{
            items:3,
            nav:false,
            dots:true
        },
        1000:{
            items:4,
            nav:true,
            loop:false,
            dots:false
        }
    }
})
// Mobile menu 
  $(".menu-toggle").click(function () {
         $('body').toggleClass( "menu-show" );
      });


// Cat
  $('.sub-cat-1').click(
    function(e) {
        e.preventDefault(); // prevent the default action
        e.stopPropagation(); // stop the click from bubbling
        $(this).parent().toggleClass('selected');
});


  $('.sub-cat-2').click(
    function(e) {
        e.preventDefault(); // prevent the default action
        e.stopPropagation(); // stop the click from bubbling
        $(this).parent().toggleClass('selected');
});

$('#products_grid_before .nav li.active').parent().parent().addClass('selected');
$('#products_grid_before .nav li.active').parent().parent().parent().parent().addClass('selected');

});

// header fix
$(window).scroll(function(){
    if ($(window).scrollTop() >= 110) {
       $('.nav-top').addClass('navbar-fixed-top');
    }
    else {
       $('.nav-top').removeClass('navbar-fixed-top');
    }
});


/*function equalHeight(group) {
	var tallest = 0;
	group.each(function() {
		var thisHeight = $(this).height();
		if(thisHeight > tallest) {
			tallest = thisHeight;
		}
	});
	group.height(tallest);
}

$(document).ready(function() {
	equalHeight($(".product .title"));
	equalHeight($(".product-img"));
});

$(window).resize(function() {
    equalHeight($(".product .title"));
    equalHeight($(".product-img"));
});*/


$(window).load(function(){
 function resetHeight() {
        var maxHeight = 0;
        jQuery(".product .title").height("auto").each(function () {
            maxHeight = $(this).height() > maxHeight ? $(this).height() : maxHeight;
        }).height(maxHeight);
    }
    resetHeight();
    jQuery(window).resize(function () {
        resetHeight();
    });

    function resetHeight1() {
        var maxHeight = 0;
        jQuery(".product-img").height("auto").each(function () {
            maxHeight = $(this).height() > maxHeight ? $(this).height() : maxHeight;
        }).height(maxHeight);
    }
    resetHeight1();
    jQuery(window).resize(function () {
          resetHeight();
        resetHeight1();
    });

    });


/*Added By BC 03-07-2015*/

$(document).ready(function() {
    $("<span class='mob_sub'><span data-icon-name='plus'></span></span>").insertBefore(".mega-menu");

    $('.mob_sub').click(
        function(e) {
            e.preventDefault(); // prevent the default action
            e.stopPropagation(); // stop the click from bubbling
            $(this).parent().toggleClass('selected');
            $(this).toggleClass('mob_sub_open');
        });

});


