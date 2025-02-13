# -*- coding; utf-8 -*-
import base64
import hashlib
import hmac
import logging
import pprint
import razorpay

import requests
from werkzeug.urls import url_join

from odoo import _, fields, models
from odoo.exceptions import ValidationError

# from odoo.addons.payment_razorpays import const

_logger = logging.getLogger(__name__)


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('razorpays', "Razorpays")], ondelete={'razorpays': 'set default'}
    )
    razorpay_key_id = fields.Char(
        string="Razorpay Key Id",
        help="The key solely used to identify the account with Razorpay.",
    )
    razorpay_key_secret = fields.Char(
        string="Razorpay Key Secret",
        required_if_provider='razorpay'
    )

    def _razorpay_make_request(self, endpoint, payload=None, method='POST'):
        """ Make a request to Razorpay API at the specified endpoint.
        Note: self.ensure_one()
        :param str endpoint: The endpoint to be reached by the request.
        :param dict payload: The payload of the request.
        :param str method: The HTTP method of the request.
        :return The JSON-formatted content of the response.
        :rtype: dict
        :raise ValidationError: If an HTTP error occurs.
        """
        # self.ensure_one()
        # client = razorpay.Client(auth=(self.razorpay_key_id, self.razorpay_key_secret))
        # data = {"amount": 500, "currency": "INR"}
        # payment = client.order.create(data=data)
        # print(payment)

        url = url_join('https://api.razorpay.com/v1/', endpoint)
        auth = (self.razorpay_key_id, self.razorpay_key_secret)
        # key = f"{self.razorpay_key_id}:{self.razorpay_key_secret}".encode("ascii")
        # value = base64.b64encode(key)
        # headers = {'Authorization': f'Basic {key}'}
        try:
            if method == 'GET':
                response = requests.get(url, params=payload, auth=auth,
                                        timeout=10)
            else:
                response = requests.post(url, json=payload, auth=auth,
                                         timeout=10)
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError:
                _logger.exception(
                    "Invalid API request at %s with data:\n%s", url,
                    pprint.pformat(payload),
                )
                raise ValidationError("Razorpay: " + _(
                    "Razorpay gave us the following information: '%s'",
                    response.json().get('error', {}).get('description')
                ))
        except (
        requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            _logger.exception("Unable to reach endpoint at %s", url)
            raise ValidationError(
                "Razorpay: " + _(
                    "Could not establish the connection to the API.")
            )
        return response.json()

    # def _razorpay_calculate_signature(self, data, is_redirect=True):
    #     """ Compute the signature for the request's data according to the Razorpay documentation.
    #
    #     See https://razorpay.com/docs/webhooks/validate-test#validate-webhooks and
    #     https://razorpay.com/docs/payments/payment-gateway/web-integration/hosted/build-integration.
    #
    #     :param dict|bytes data: The data to sign.
    #     :param bool is_redirect: Whether the data should be treated as redirect data or as coming
    #                              from a webhook notification.
    #     :return: The calculated signature.
    #     :rtype: str
    #     """
    #     if is_redirect:
    #         secret = self.razorpay_key_secret
    #         signing_string = f'{data["razorpay_order_id"]}|{data["razorpay_payment_id"]}'
    #         return hmac.new(
    #             secret.encode(), msg=signing_string.encode(),
    #             digestmod=hashlib.sha256
    #         ).hexdigest()
    #     else:  # Notification data.
    #         secret = self.razorpay_webhook_secret
    #         return hmac.new(secret.encode(), msg=data,
    #                         digestmod=hashlib.sha256).hexdigest()

    # def _get_default_payment_method_codes(self):
    #     """ Override of `payment` to return the default payment method codes. """
    #     default_codes = super()._get_default_payment_method_codes()
    #     if self.code != 'razorpays':
    #         return default_codes
    #     return const.DEFAULT_PAYMENT_METHODS_CODES
    #
    # def _get_validation_amount(self):
    #     """ Override of `payment` to return the amount for Razorpay validation operations.
    #
    #     :return: The validation amount.
    #     :rtype: float
    #     """
    #     res = super()._get_validation_amount()
    #     if self.code != 'razorpays':
    #         return res
    #
    #     return 1.0
