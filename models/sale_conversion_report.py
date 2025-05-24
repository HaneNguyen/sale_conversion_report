from odoo import models, fields, tools

class SaleConversionReport(models.Model):
    _name = 'sale.conversion.report'
    _description = 'Sale Quote to Order Conversion Report'
    _auto = False
    _order = 'period desc'

    period = fields.Char(string='Period (YYYY-MM)', readonly=True)
    user_id = fields.Many2one('res.users', string='Salesperson', readonly=True)
    partner_id = fields.Many2one('res.partner', string='Customer', readonly=True)
    partner_state_id = fields.Many2one('res.country.state', string='Customer State', readonly=True)
    total_quotations = fields.Integer(string='Total Quotations', readonly=True)
    total_orders = fields.Integer(string='Total Orders', readonly=True)
    conversion_rate = fields.Float(string='Conversion Rate (%)', readonly=True)

    def init(self):
        tools.drop_view_if_exists(self.env.cr, 'sale_conversion_report')
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW sale_conversion_report AS (
                SELECT
                    row_number() OVER () AS id,
                    to_char(so.date_order, 'YYYY-MM') AS period,
                    so.user_id,
                    so.partner_id,
                    rp.state_id AS partner_state_id,
                    COUNT(DISTINCT CASE WHEN so.state != 'cancel' THEN so.id END) AS total_quotations,  -- tất cả báo giá & đơn hàng không hủy
                    COUNT(DISTINCT CASE WHEN so.state IN ('sale', 'done') THEN so.id END) AS total_orders,
                    CASE
                        WHEN COUNT(DISTINCT CASE WHEN so.state != 'cancel' THEN so.id END) = 0 THEN 0
                        ELSE ROUND(
                            COUNT(DISTINCT CASE WHEN so.state IN ('sale', 'done') THEN so.id END)::numeric * 100 /
                            COUNT(DISTINCT CASE WHEN so.state != 'cancel' THEN so.id END)::numeric,
                            2
                        )
                    END AS conversion_rate
                FROM sale_order so
                LEFT JOIN res_partner rp ON rp.id = so.partner_id
                GROUP BY to_char(so.date_order, 'YYYY-MM'), so.user_id, so.partner_id, rp.state_id
            )
        """)
