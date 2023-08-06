# Copyright 2011 Minorisa, S.L. <http://www.minorisa.net>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import os
import logging
from odoo import models, api

_logger = logging.getLogger(__name__)


class WizardDeleteAttachments(models.TransientModel):
    _name = "mindev.wizard.delete.attachments"
    _description = "MinDev Wizard Delete Attachments"

    @api.multi
    def action_delete(self):
        self.ensure_one()

        iaobj = self.env["ir.attachment"]

        attachments = iaobj.search([
            ('store_fname', '!=', False)
        ])

        _logger.info("Checking %s attachments" % len(attachments))

        for attachment in attachments:

            full_path = iaobj._full_path(attachment.store_fname)
            _logger.debug(
                "Checking %s" % full_path)

            if not os.path.exists(full_path):
                _logger.debug("Deleting %s" % full_path)
                attachment.unlink()
