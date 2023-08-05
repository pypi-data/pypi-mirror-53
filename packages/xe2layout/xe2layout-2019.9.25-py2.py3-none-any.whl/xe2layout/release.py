#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
# @copyright Copyright (C) Guichet Entreprises - All Rights Reserved
# 	All Rights Reserved.
# 	Unauthorized copying of this file, via any medium is strictly prohibited
# 	Dissemination of this information or reproduction of this material
# 	is strictly forbidden unless prior written permission is obtained
# 	from Guichet Entreprises.
###############################################################################

###############################################################################
# Template generation for xenon2
###############################################################################

import os
import os.path
import logging
import codecs
import urllib.request
import shutil
from zipfile import ZipFile
import yaml
import gitlab
import pymdtools.common as common
import pymdtools.mdcommon

# -----------------------------------------------------------------------------
def get(destination_folder, name, version=None):
    logging.info("Get the xenon2 release %s %s", name, version)
    project_id = '14250502'
    server = 'https://gitlab.com/'
    conf_filename = 'template_conf.yml'

    destination_folder = common.check_create_folder(destination_folder)
    conf_filename = os.path.join(destination_folder, conf_filename)

    if version is None:
        project = gitlab.Gitlab(server).projects.get(project_id)
        release_tag = [release.tag_name for release in project.releases.list()]
        release_tag.sort()
        version = release_tag[-1]
        logging.info("The latest release is %s", version)

    if os.path.isfile(conf_filename):
        with codecs.open(conf_filename, "r", "utf-8") as ymlfile:
            conf = yaml.load(ymlfile, Loader=yaml.FullLoader)
        current_version = conf['version']
        logging.info('Current_version is %s', current_version)
        if current_version == version:
            logging.info('Already have it')
            return destination_folder

    logging.info('Go for a download')
    project = gitlab.Gitlab(server).projects.get(project_id)
    description_md = project.releases.get(version).description
    links = pymdtools.mdcommon.search_link_in_md_text(description_md)

    url = None
    for link in links:
        if link['name'].startswith(name):
            url = link['url']
    if url is None:
        logging.warning('Cannont find the version %s of %s', version, name)
        raise Exception('Cannont find the version %s of %s' % (version, name))
    url = project.web_url + url

    if os.path.isdir(destination_folder):
        logging.info('Clean folder %s', destination_folder)
        shutil.rmtree(destination_folder)
        common.check_create_folder(destination_folder)

    dest_filename = os.path.join(
        destination_folder, name + "-" + release_tag[-1] + ".zip")
    logging.info('Download %s --> %s', url, dest_filename)
    urllib.request.urlretrieve(url, dest_filename)

    logging.info('Extract %s', dest_filename)
    with ZipFile(dest_filename, 'r') as zip_obj:
        zip_obj.extractall(destination_folder)

    return destination_folder
