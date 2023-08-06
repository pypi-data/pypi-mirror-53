# -*- coding: UTF-8 -*-
# Copyright 2018-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from lino.api import dd, rt, _


def objects():

    ContentType = rt.models.contenttypes.ContentType
    ExcerptType = rt.models.excerpts.ExcerptType

    yield ExcerptType(
        build_method='appypdf',
        #template='Default.odt',
        body_template='final_report.body.html',
        certifying=True, primary=True,
        content_type=ContentType.objects.get_for_model(
            rt.models.avanti.Client),
        **dd.str2kw('name', _("Final certificate")))

    # yield ExcerptType(
    #     build_method='appypdf',
    #     # template='Certificate.odt',
    #     body_template='certificate.body.html',
    #     backward_compat=True,
    #     content_type=ContentType.objects.get_for_model(
    #         rt.models.courses.Enrolment),
    #     **dd.str2kw('name', _("Certificate")))
