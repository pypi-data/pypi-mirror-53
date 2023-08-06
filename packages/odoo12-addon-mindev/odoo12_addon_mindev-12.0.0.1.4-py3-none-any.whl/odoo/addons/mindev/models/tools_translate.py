# Copyright 2011 Minorisa, S.L. <http://www.minorisa.net>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import tarfile
import io
import re
import logging
import fnmatch
import odoo
from babel.messages import extract
from os.path import join, dirname, sep
from collections import defaultdict
from odoo.tools.osutil import walksymlinks
from odoo import _
from odoo.tools import pycompat, config
from odoo.tools.translate import PoFile, encode, WEB_TRANSLATION_COMMENT

_logger = logging.getLogger(__name__)


def trans_export(lang, modules, buffer, format, cr, do_fields=True):

    def _process(format, modules, rows, buffer, lang):
        if format == 'csv':
            writer = pycompat.csv_writer(buffer, dialect='UNIX')
            # write header first
            writer.writerow((
                "module", "type", "name", "res_id",
                "src", "value", "comments"))
            for module, type, name, res_id, src, trad, comments in rows:
                comments = '\n'.join(comments)
                writer.writerow(
                    (module, type, name, res_id, src, trad, comments))

        elif format == 'po':
            writer = PoFile(buffer)
            writer.write_infos(modules)

            # we now group the translations by source.
            # That means one translation per source.
            grouped_rows = {}
            for module, type, name, res_id, src, trad, comments in rows:
                row = grouped_rows.setdefault(src, {})
                row.setdefault('modules', set()).add(module)
                if not row.get('translation') and trad != src:
                    row['translation'] = trad
                row.setdefault('tnrs', []).append((type, name, res_id))
                row.setdefault('comments', set()).update(comments)

            for src, row in sorted(grouped_rows.items()):
                if not lang:
                    # translation template, so no translation value
                    row['translation'] = ''
                elif not row.get('translation'):
                    row['translation'] = ''
                writer.write(
                    row['modules'],
                    row['tnrs'],
                    src,
                    row['translation'],
                    row['comments'])

        elif format == 'tgz':
            rows_by_module = defaultdict(list)
            for row in rows:
                module = row[0]
                rows_by_module[module].append(row)

            with tarfile.open(fileobj=buffer, mode='w|gz') as tar:
                for mod, modrows in rows_by_module.items():
                    with io.BytesIO() as buf:
                        _process('po', [mod], modrows, buf, lang)
                        buf.seek(0)

                        info = tarfile.TarInfo(
                            join(mod, 'i18n', '{basename}.{ext}'.format(
                                basename=lang or mod,
                                ext='po' if lang else 'pot',
                            )))
                        # addfile will read <size> bytes from the buffer so
                        # size *must* be set first
                        info.size = len(buf.getvalue())

                        tar.addfile(info, fileobj=buf)
        else:
            raise Exception(
                _('Unrecognized extension: must be one of .csv, .po, or .tgz '
                  '(received .%s).') % format)

    translations = trans_generate(lang, modules, cr, do_fields)
    modules = set(t[0] for t in translations)
    _process(format, modules, translations, buffer, lang)
    del translations


def trans_generate(lang, modules, cr, do_fields=True):
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    to_translate = set()

    def push_translation(module, type, name, id, source, comments=None):
        # empty and one-letter terms are ignored,
        # they probably are not meant to be
        # translated, and would be very hard to translate anyway.
        sanitized_term = (source or '').strip()
        # remove non-alphanumeric chars
        sanitized_term = re.sub(r'\W+', '', sanitized_term)
        if not sanitized_term or len(sanitized_term) <= 1:
            return

        tnx = (module, source, name, id, type, tuple(comments or ()))
        to_translate.add(tnx)

    query = 'SELECT min(name), model, res_id, module FROM ir_model_data'
    query_models = """SELECT m.id, m.model, imd.module
                      FROM ir_model AS m, ir_model_data AS imd
                      WHERE m.id = imd.res_id AND imd.model = 'ir.model'"""

    if 'all_installed' in modules:
        query += ' WHERE module IN ( ' \
                 'SELECT name FROM ir_module_module ' \
                 'WHERE state = \'installed\') '
        query_models += " AND imd.module in ( " \
                        "SELECT name FROM ir_module_module " \
                        "WHERE state = 'installed') "

    if 'all' not in modules:
        query += ' WHERE module IN %s'
        query_models += ' AND imd.module IN %s'
        query_param = (tuple(modules),)
    else:
        query += ' WHERE module != %s'
        query_models += ' AND imd.module != %s'
        query_param = ('__export__',)

    query += ' GROUP BY model, res_id, module ' \
             'ORDER BY module, model, min(name)'
    query_models += ' ORDER BY module, model'

    cr.execute(query, query_param)

    for (xml_name, model, res_id, module) in cr.fetchall():
        xml_name = "%s.%s" % (module, xml_name)

        if model not in env:
            _logger.error(u"Unable to find object %r", model)
            continue

        record = env[model].browse(res_id)
        if not record._translate:
            # explicitly disabled
            continue

        if not record.exists():
            _logger.warning(
                u"Unable to find object %r with id %d", model, res_id)
            continue

        if model == u'ir.model.fields':
            try:
                field_name = record.name
            except AttributeError as exc:
                _logger.error(u"name error in %s: %s", xml_name, str(exc))
                continue
            field_model = env.get(record.model)
            if (field_model is None or not field_model._translate or
                    field_name not in field_model._fields):
                continue
            field = field_model._fields[field_name]

            if isinstance(getattr(field, 'selection', None), (list, tuple)):
                name = "%s,%s" % (record.model, field_name)
                if field.type == 'ewan_icon_selection':
                    for dummy, val, icon in field.selection:
                        push_translation(module, 'selection', name, 0, val)
                else:
                    for dummy, val in field.selection:
                        push_translation(module, 'selection', name, 0, val)

        if do_fields:
            for field_name, field in record._fields.items():
                if field.translate:
                    name = model + "," + field_name
                    try:
                        value = record[field_name] or ''
                    except Exception:
                        continue
                    for term in set(field.get_trans_terms(value)):
                        trans_type = 'model_terms' \
                            if callable(field.translate) else 'model'
                        push_translation(module, trans_type, name, xml_name,
                                         term)

        # End of data for ir.model.data query results

    def push_constraint_msg(module, term_type, model, msg):
        if not callable(msg):
            push_translation(encode(module), term_type, encode(model), 0, msg)

    def push_local_constraints(module, model, cons_type='sql_constraints'):
        """ Climb up the class hierarchy and ignore
        inherited constraints from other modules. """
        term_type = 'sql_constraint' \
            if cons_type == 'sql_constraints' else 'constraint'
        msg_pos = 2 if cons_type == 'sql_constraints' else 1
        for cls in model.__class__.__mro__:
            if getattr(cls, '_module', None) != module:
                continue
            constraints = getattr(cls, '_local_' + cons_type, [])
            for constraint in constraints:
                push_constraint_msg(
                    module, term_type, model._name, constraint[msg_pos])

    cr.execute(query_models, query_param)

    for (x, model, module) in cr.fetchall():
        if model not in env:
            _logger.error("Unable to find object %r", model)
            continue
        Model = env[model]
        if Model._constraints:
            push_local_constraints(module, Model, 'constraints')
        if Model._sql_constraints:
            push_local_constraints(module, Model, 'sql_constraints')

    installed_modules = [
        m['name']
        for m in env['ir.module.module'].search_read([
            ('state', '=', 'installed'),
        ], fields=['name'])
    ]

    path_list = [(path, True) for path in odoo.modules.module.ad_paths]
    # Also scan these non-addon paths
    for bin_path in ['osv', 'report', 'modules', 'service', 'tools']:
        path_list.append((join(config['root_path'], bin_path), True))
    # non-recursive scan for individual files in root directory but without
    # scanning subdirectories that may contain addons
    path_list.append((config['root_path'], False))
    _logger.debug("Scanning modules at paths: %s", path_list)

    def get_module_from_path(path):
        for (mp, rec) in path_list:
            mp = join(mp, '')
            xdirname = join(dirname(path), '')
            if rec and path.startswith(mp) and xdirname != mp:
                path = path[len(mp):]
                return path.split(sep)[0]
        return 'base'
        # files that are not in a module
        # are considered as being in 'base' module

    def verified_module_filepaths(fname, path, root):
        fabsolutepath = join(root, fname)
        frelativepath = fabsolutepath[len(path):]
        display_path = "addons%s" % frelativepath
        module = get_module_from_path(fabsolutepath)
        if ('all' in modules or module in modules) \
                and module in installed_modules:
            if sep != '/':
                display_path = display_path.replace(sep, '/')
            return module, fabsolutepath, frelativepath, display_path
        return None, None, None, None

    def babel_extract_terms(
            fname, path, root, extract_method="python", trans_type='code',
            extra_comments=None, extract_keywords=None):
        if extract_keywords is None:
            extract_keywords = {'_': None}
        module, fabsolutepath, _, display_path = verified_module_filepaths(
            fname, path, root)
        extra_comments = extra_comments or []
        if not module:
            return
        src_file = open(fabsolutepath, 'rb')
        options = {}
        if extract_method == 'python':
            options['encoding'] = 'UTF-8'
        try:
            for extracted in extract.extract(
                    extract_method, src_file,
                    keywords=extract_keywords, options=options):
                # Babel 0.9.6 yields lineno, message, comments
                # Babel 1.3 yields lineno, message, comments, context
                lineno, message, comments = extracted[:3]
                push_translation(module, trans_type, display_path, lineno,
                                 encode(message), comments + extra_comments)
        except Exception:
            _logger.exception("Failed to extract terms from %s", fabsolutepath)
        finally:
            src_file.close()

    for (path, recursive) in path_list:
        _logger.debug("Scanning files of modules at %s", path)
        for root, dummy, files in walksymlinks(path):
            for fname in fnmatch.filter(files, '*.py'):
                babel_extract_terms(fname, path, root)
            # Javascript source files in the static/src/js directory,
            # rest is ignored (libs)
            if fnmatch.fnmatch(root, '*/static/src/js*'):
                for fname in fnmatch.filter(files, '*.js'):
                    babel_extract_terms(
                        fname, path, root, 'javascript',
                        extra_comments=[WEB_TRANSLATION_COMMENT],
                        extract_keywords={'_t': None, '_lt': None})
            # QWeb template files
            if fnmatch.fnmatch(root, '*/static/src/xml*'):
                for fname in fnmatch.filter(files, '*.xml'):
                    babel_extract_terms(
                        fname, path, root,
                        'odoo.tools.translate:babel_extract_qweb',
                        extra_comments=[WEB_TRANSLATION_COMMENT])
            if not recursive:
                # due to topdown, first iteration is in first level
                break

    out = []
    # translate strings marked as to be translated
    Translation = env['ir.translation']
    for module, source, name, id, type, comments in sorted(to_translate):
        trans = Translation._get_source(name, type, lang, source) \
            if lang else ""
        out.append(
            (module, type, name, id, source, encode(trans) or '', comments))
    return out
