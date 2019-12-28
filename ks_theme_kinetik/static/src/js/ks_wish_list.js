odoo.define('ks_theme_website_wishlist', function (require) {
    'use strict'
     var ks_WishList = require('website_sale_wishlist.wishlist');
     var wSaleUtils = require('website_sale.utils');
     var sAnimations = require('website.content.snippets.animation');
     sAnimations.registry.ProductWishlist.include({
              _addOrMoveWish: function (e) {
                                var $navButton = wSaleUtils.getNavBarButton('.o_wsale_my_cart');
                                if ($navButton.length==0){
                                var $navButton=$('.o_wsale_my_cart');
                                }
                                var tr = $(e.currentTarget).parents('tr');
                                var product = tr.data('product-id');
                                $('.o_wsale_my_cart').removeClass('d-none');
                                wSaleUtils.animateClone($navButton, tr, 25, 40);

                                if ($('#b2b_wish').is(':checked')) {
                                    return this._addToCart(product, tr.find('add_qty').val() || 1);
                                } else {
                                    var adding_deffered = this._addToCart(product, tr.find('add_qty').val() || 1);
                                    this._removeWish(e, adding_deffered);
                                    return adding_deffered;
                                }
                            },


              _updateWishlistView: function () {
                 $('.o_wsale_my_wish').show();
                   $('.my_wish_quantity').text(this.wishlistProductIDs.length);
                     },

                 _addNewProducts: function ($el) {
                            var self = this;
                            var productID = $el.data('product-product-id');
                            if ($el.hasClass('o_add_wishlist_dyn')) {
                                productID = $el.parent().find('.product_id').val();
                                if (!productID) { // case List View Variants
                                    productID = $el.parent().find('input:checked').first().val();
                                }
                                productID = parseInt(productID, 10);
                            }
                            var $form = $el.closest('form');
                            var templateId = $form.find('.product_template_id').val();
                            // when adding from /shop instead of the product page, need another selector
                            if (!templateId) {
                                templateId = $el.data('product-template-id');
                            }
                            $el.prop("disabled", true).addClass('disabled');
                            var productReady = this.selectOrCreateProduct(
                                $el.closest('form'),
                                productID,
                                templateId,
                                false
                            );

                            productReady.then(function (productId) {
                                productId = parseInt(productId, 10);

                                if (productId && !_.contains(self.wishlistProductIDs, productId)) {
                                    return self._rpc({
                                        route: '/shop/wishlist/add',
                                        params: {
                                            product_id: productId,
                                        },
                                    }).then(function () {
                                        var $navButton = $('.o_wsale_my_wish');
                                        self.wishlistProductIDs.push(productId);
                                        self._updateWishlistView();
                                        wSaleUtils.animateClone($navButton, $el.closest('form'), 25, 40);
                                    }).guardedCatch(function () {
                                        $el.prop("disabled", false).removeClass('disabled');
                                    });
                                }
                            }).guardedCatch(function () {
                                $el.prop("disabled", false).removeClass('disabled');
                            });
                        },

    });
});
