from test import test_app
from test import test_const
from test import test_document
from test import test_errorlog
from test import test_proxy
from test import test_push_doc
from test import test_search


test_app.test_create()
test_app.test_get_all()
test_app.test_get_all_page()
test_app.test_status()
test_app.test_delete()


test_const.test_const_def()
test_const.test_const_del()
test_const.test_const_del2()


test_document.test_app_create()
test_document.test_add()
test_document.test_adds()
test_document.test_get()
test_document.test_update()
test_document.test_after_update_get()
test_document.test_delete()
test_document.test_deletes()
test_document.test_app_delete()


test_errorlog.test_errlog()
test_errorlog.test_errlog_post()
test_errorlog.test_errlog_raise()
test_errorlog.test_errlog_raise2()


test_proxy.test_errlog()
test_proxy.test_errlog_post()


test_push_doc.test_push_add()
test_push_doc.test_push_add2()
test_push_doc.test_push_update()
test_push_doc.test_push_update2()
test_push_doc.test_deletes()


test_search.test_search()
test_search.test_scroll()
test_search.test_suggest()
test_search.test_rebuild()
