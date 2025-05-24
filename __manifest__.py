{
    'name': 'Sale Conversion Report',
    'version': '1.0',
    'summary': 'Report sale quotation to order conversion rate',
    'description': 'Thống kê tỉ lệ chuyển đổi từ báo giá sang đơn hàng theo tháng',
    'author': 'Nhóm 2',
    'category': 'Sales',
    'depends': ['sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_conversion_report_views.xml',
        'views/sale_conversion_report_action.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': False,
}
