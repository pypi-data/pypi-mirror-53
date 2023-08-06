# Copyright 2011 Minorisa, S.L. <http://www.minorisa.net>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from io import BytesIO
import contextlib
import os

try:
    import git
except ImportError:
    git = False

from odoo import models, fields, api, _
from ..models.tools_translate import trans_export
from odoo.exceptions import ValidationError
from odoo.modules import module as omm


class DownloadTranslations(models.TransientModel):
    _name = 'mindev.download.translation'
    _description = 'MinDev Download Translations'

    module = fields.Many2one('ir.module.module', string="Module",
                             domain=[('state', '=', 'installed')])
    languages = fields.Many2many('res.lang', string="Languages")
    i18n_path = fields.Char(string="i18n Path")
    git_repo = fields.Char(string="Git Repo")
    has_git = fields.Boolean(string="Has Git")
    do_commit = fields.Boolean(string="Do Commit & Push")
    do_fields = fields.Boolean(string="Include fields")
    state = fields.Selection(selection=[
        ('start', 'start'),
        ('end', 'end'),
    ], string="State", required=True, default='start')
    html_res = fields.Html(string="Result")

    @api.model
    def default_get(self, fields_list):
        res = super(DownloadTranslations, self).default_get(
            fields_list=fields_list)
        lang_en = self.env.ref('base.lang_en')
        lang_en_id = lang_en and lang_en.id or False
        langs = self.env["res.lang"].search([('id', '!=', lang_en_id)])
        res.update(languages=langs.ids)
        return res

    @api.onchange('module')
    def onchange_module(self):
        i18n_path = False
        has_git = False
        git_repo = False

        if self.module:
            trav = omm.get_module_path(self.module.name)
            i18n_path = os.path.join(trav, 'i18n')
            while trav != '/':
                if os.path.exists(os.path.join(trav, '.git')):
                    git_repo = trav
                    has_git = True
                    break
                trav = os.path.dirname(trav)

        self.i18n_path = i18n_path
        self.has_git = has_git
        self.git_repo = git_repo
        self.do_commit = has_git

    @api.multi
    def do_download(self):
        self.ensure_one()
        if not self.module:
            raise ValidationError(_("You must select a module!"))

        # Get again the path because this field is readonly
        # and is not updated by onchange
        i18n_path = self.i18n_path
        # project_path = omm.get_module_resource(self.module.name, 'i18n')
        if not i18n_path:
            raise ValidationError(_("Unable to create i18n path!"))

        # Check if i18n path exists; if not, create it
        if not os.path.exists(i18n_path):
            os.makedirs(i18n_path)

        i18n_files = []
        # Create .po file for each language
        for lang in self.languages:
            name = u"{}.po".format(lang.iso_code)
            i18n_file = os.path.join(i18n_path, name)
            # i18n_file = os.path.join('/home/jaume.planas/Escriptori', name)
            try:
                with contextlib.closing(BytesIO()) as buf:
                    trans_export(
                        lang.code,
                        [self.module.name], buf, 'po',
                        self._cr,
                        do_fields=self.do_fields,
                    )
                    buf.seek(0)
                    with open(i18n_file, 'wb') as output:
                        for line in buf:
                            output.write(line)
            except Exception:
                raise
            i18n_files.append(i18n_file)

        res = """
<h2>The following PO files have been created or modified</h2>
<ul>
        """
        for x in i18n_files:
            res += """
    <li>{}</li>
            """.format(x)
        res += """
</ul>
        """
        if self.do_commit and git:
            repo_name = self.git_repo
            repo = git.Repo(repo_name)
            relative_path = os.path.relpath(i18n_path, repo_name)
            files = [
                x.a_path for x in repo.index.diff(None, paths=[
                    relative_path
                ])
            ]
            xgit = repo.git
            xgit.add(files)
            git_msg = u"[TRA]][{}] PO files exported from Odoo".format(
                self.module.name)
            xgit.commit('-m', git_msg, files)
            commit = repo.head.commit
            branch = repo.head.ref.name
            hexsha = commit.hexsha
            xgit.push('origin', '{}:{}'.format(hexsha, branch))

            res += """
<h2>The following commit has been created</h2>
<pre>
            """
            res += xgit.show('--name-only', hexsha)
            res += """
</pre>
            """
        self.html_res = res
        self.state = 'end'
        return {
            'type': 'ir.actions.act_window',
            'name': 'Download Translation Results',
            'res_model': 'mindev.download.translation',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new',
        }
