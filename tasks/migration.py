import os
from torndb import Connection
from tornado.options import options

from tasks import mltshp_task


@mltshp_task()
def migrate_for_user(user_id=0, **kwargs):
    """
    This task will update the post table setting any post containing the shared file
    to deleted = 0
    """
    db = Connection(options.database_host, options.database_name, options.database_user, options.database_password)

    db.execute("""UPDATE accesstoken SET deleted=0 WHERE deleted=2 AND user_id=%s""", user_id)
    db.execute("""UPDATE app SET deleted=0 WHERE deleted=2 AND user_id=%s""", user_id)
    db.execute("""UPDATE comment SET deleted=0 WHERE deleted=2 AND user_id=%s""", user_id)
    db.execute("""UPDATE comment_like SET deleted=0 WHERE deleted=2 AND user_id=%s""", user_id)
    db.execute("""UPDATE externalservice SET deleted=0 WHERE deleted=2 AND user_id=%s""", user_id)
    db.execute("""UPDATE favorite SET deleted=0 WHERE deleted=2 AND user_id=%s""", user_id)
    db.execute("""UPDATE invitation_request SET deleted=0 WHERE deleted=2 AND user_id=%s""", user_id)
    db.execute("""UPDATE notification SET deleted=0 WHERE deleted=2 AND receiver_id=%s""", user_id)
    db.execute("""UPDATE post SET deleted=0 WHERE deleted=2 AND user_id=%s""", user_id)
    db.execute("""UPDATE shake SET deleted=0 WHERE deleted=2 AND user_id=%s""", user_id)
    db.execute("""UPDATE shake_manager SET deleted=0 WHERE deleted=2 AND user_id=%s""", user_id)
    db.execute("""UPDATE shakesharedfile SET deleted=0 WHERE deleted=2 AND shake_id IN (SELECT DISTINCT id FROM shake WHERE deleted=0 AND user_id=%s)""", user_id)
    db.execute("""UPDATE sharedfile SET deleted=0 WHERE deleted=2 AND user_id=%s""", user_id)
    db.execute("""UPDATE subscription SET deleted=0 WHERE deleted=2 AND user_id=%s""", user_id)
    db.execute("""UPDATE tagged_file SET deleted=0 WHERE deleted=2 AND sharedfile_id IN (SELECT DISTINCT id FROM sharedfile WHERE user_id=%s)""", user_id)
    # this should already be done by the web app, but we may running this
    # via a script
    db.execute("""UPDATE user SET deleted=0 WHERE deleted=2 and id=%s""", user_id)
    db.execute("""UPDATE migration_state SET is_migrated=1 WHERE user_id=%s""", user_id)

    db.close()
