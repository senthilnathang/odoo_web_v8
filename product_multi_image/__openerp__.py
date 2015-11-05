{
    'name': 'Product Multi-Image',
    'category': 'Website',
    'version': '1.0',
    'author': 'Luke Branch and Cristian Sebastian Rocha',
    'depends': ['product', 'sale', ],
    'data': [
        'views/product_images.xml',
       # 'views/website_product_image_carousel.xml',
        #'views/theme.xml',
        'security/ir.model.access.csv',
    ],
    'application': True,
}
