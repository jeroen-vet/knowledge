# Copyright 2018 Ivan Todorovich (<ivan.todorovich@gmail.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


def post_init_hook(cr, registry):  # pragma: no cover
    # Set all pre-existing pages history to approved
    cr.execute("""
        UPDATE document_page_history
        SET state='approved',
            approved_uid=create_uid,
            approved_date=create_date
        WHERE state IS NULL
    """)


def uninstall_hook(cr, registry):  # pragma: no cover
    # Remove unapproved pages
    cr.execute(
        "DELETE FROM document_page_history "
        "WHERE state != 'approved'"
    )
