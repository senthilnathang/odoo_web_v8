jQuery(function($){
		
    $('#zoom_01').elevateZoom();
    $('.product_multi_img,.product_main_multi_img').on('click', function(){
	    // Remove old instance od EZ
	    $('.zoomContainer').remove();
	    $('#zoom_01').removeData('elevateZoom');
	    // Update source for images
	    $('#zoom_01').attr('src', this.src);
	    $('#zoom_01').data('zoom-image', this.src);
	    // Reinitialize EZ	
		var website = openerp.website;
	    openerp.jsonRpc('/product/zoom_type', 'call', {}).then(function (type) 
					{	
					if (type)
	    			{	$('#zoom_01').elevateZoom({constrainType:"height", constrainSize:274, zoomType: "lens", containLensZoom: true, cursor: 'pointer'});
	    			}	
					else
	    				$('#zoom_01').elevateZoom();					
					   
				 });
    
	});
    $('.product-zoom-image').on('hover', function(){
    	// Remove old instance od EZ
		s=document.getElementById('zoom_01').src;    
	    $('.zoomContainer').remove();
	    $('#zoom_01').removeData('elevateZoom');
	    // Update source for images
	    $('#zoom_01').attr('src', s);
	    $('#zoom_01').data('zoom-image', s);
	    // Reinitialize EZ
		var website = openerp.website;	    
	    openerp.jsonRpc('/product/zoom_type', 'call', {}).then(function (type) 
					{	
					if (type)
	    			{	$('#zoom_01').elevateZoom({constrainType:"height", constrainSize:274, zoomType: "lens", containLensZoom: true, cursor: 'pointer'});
	    			}
					else
	    				$('#zoom_01').elevateZoom();					
					   
				 });	    
	});

});