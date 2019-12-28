# # -*- coding: utf-8 -*-
from odoo import models, fields, api
from lxml import etree



class Ks_IrUiView(models.Model):
    _inherit = "ir.ui.view"
    #
    # LAZYLOAD_DEFAULT_SRC = 'data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw=='
    #
    # @api.model
    # def render_template(self, template, values=None, engine='ir.qweb'):
    #     res = super(Ks_IrUiView, self).render_template(template, values, engine)
    #     html = etree.HTML(res)
    #     imgs = html.xpath('//main//img[@src][not(hasclass("lazyload-disable"))]') + html.xpath('//footer//img[@src][not(hasclass("lazyload-disable"))]')
    #     for img in imgs:
    #         src = img.attrib['src']
    #         img.attrib['src'] = self.LAZYLOAD_DEFAULT_SRC
    #         img.attrib['data-src'] = src
    #     res = etree.tostring(html, method='html')
    #     return res

    # @api.multi
    def toggle(self):
        """ Switches between enabled and disabled statuses
        """

        def deactivate_views(current_view, views):
            for hv in views:
                if current_view.key != hv.key and hv.active:
                    hv.write({'active': False})

        for view in self:
            # Activating current view and deactive other view of footer,heade,fonts etc...
            if 'ks_theme_kinetik.custom_footer_layout' in view.key:

                footer_views = view.search([('key', 'like', 'custom_footer_layout'), ('active', '=', True),
                                            ('website_id', '=', self.env['website'].get_current_website().id)])
                deactivate_views(view, footer_views)

            elif 'ks_theme_kinetik.custom_snippet_width_1' in view.key:
                width_views = view.search([('key', 'like', 'custom_snippet_width'), ('active', '=', True),
                                           ('website_id', '=', self.env['website'].get_current_website().id)])
                deactivate_views(view, width_views)
            elif 'ks_theme_kinetik.custom_header_offer_price' in view.key:
                offer_header_views = view.search([('key', 'like', 'custom_header_offer_price'), ('active', '=', True),
                                                  ('website_id', '=', self.env['website'].get_current_website().id)])
                deactivate_views(view, offer_header_views)
            elif 'ks_theme_kinetik.custom_header_layout' in view.key:
                header_views = view.search(
                    [('key', 'like', 'custom_header_layout'), ('active', '=', True),
                     ('website_id', '=', self.env['website'].get_current_website().id)])
                deactivate_views(view, header_views)
            elif 'ks_theme_kinetik.custom_font_layout' in view.key:
                font_views = view.search(
                    [('key', 'like', 'custom_font_layout'),('active', '=', True),
                     ('website_id', '=', self.env['website'].get_current_website().id)])
                deactivate_views(view, font_views)
            elif 'ks_theme_kinetik.ks_button_style_layout' in view.key:
                button_views = view.search(
                    [('key', 'like', 'ks_button_style_layout'), ('active', '=', True),
                     ('website_id', '=', self.env['website'].get_current_website().id)])
                deactivate_views(view, button_views)

            # rewriting on view and it works
            state = not view.active
            try:
                view.write({'active':state})
            except Exception:
                view.write({'active': not view.active})

    # It is patched because getting some error in case of rtl
    @api.model
    def apply_view_inheritance(self, source, source_id, model, root_id=None):
        """ Apply all the (directly and indirectly) inheriting views.

        :param source: a parent architecture to modify (with parent modifications already applied)
        :param source_id: the database view_id of the parent view
        :param model: the original model for which we create a view (not
            necessarily the same as the source's model); only the inheriting
            views with that specific model will be applied.
        :return: a modified source where all the modifying architecture are applied
        """
        if root_id is None:
            root_id = source_id
        sql_inherit = self.get_inheriting_views_arch(source_id, model)
        for (specs, view_id) in sql_inherit:
            if specs:
                specs_tree = etree.fromstring(specs.encode('utf-8'))
            else:
                spec = self.env['ir.ui.view'].browse(view_id).arch_db
                specs_tree = etree.fromstring(spec.encode('utf-8'))
            if self._context.get('inherit_branding'):
                self.inherit_branding(specs_tree, view_id, root_id)
            source = self.apply_inheritance_specs(source, specs_tree, view_id)
            source = self.apply_view_inheritance(source, view_id, model, root_id=root_id)

        return source
