{
    'name': 'Payment Razorpays',
    'version': '17.0.1.0.0',
    'description': 'Razorpay Payment Gateway',
    'category': 'Sales/Payment Razorpays',
    'summary': 'Make Transactions through Razorpay Payment Gateway',
    'installable': True,
    'application': True,
    'depends': [
        'payment',
        'sale_management',
        ],
    'data': [
        'views/payment_razorpay_templates.xml',
        'data/payment_method_data.xml',
        'data/payment_provider_data.xml',
        'views/payment_provider_views.xml',
    ],
    # 'assets': {
    #     'web.assets_frontend': [
    #         'payment_razorpays/static/src/js/payment_form.js',
    #     ],
    # }
}