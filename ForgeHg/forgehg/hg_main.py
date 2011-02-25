#-*- python -*-
import logging

# Non-stdlib imports
import pkg_resources
from pylons import c, g

from ming.utils import LazyProperty
from ming.orm.ormsession import ThreadLocalORMSession

# Pyforge-specific imports
from allura.lib import helpers as h
from allura import model as M
from allura.controllers.repository import RepoRootController, RefsController, CommitsController
from allura.controllers.repository import MergeRequestsController
from allura.lib.repository import RepositoryApp

# Local imports
from . import model as HM
from . import version
from .controllers import BranchBrowser

log = logging.getLogger(__name__)

class ForgeHgApp(RepositoryApp):
    '''This is the Git app for PyForge'''
    __version__ = version.__version__
    tool_label='Mercurial'
    ordinal=3
    forkable=True
    default_branch_name='ref/default'

    def __init__(self, project, config):
        super(ForgeHgApp, self).__init__(project, config)
        self.root = RepoRootController()
        self.root.ref = RefsController(BranchBrowser)
        self.root.ci = CommitsController()
        setattr(self.root, 'merge-requests', MergeRequestsController())

    @LazyProperty
    def repo(self):
        return HM.Repository.query.get(app_config_id=self.config._id)

    def install(self, project):
        '''Create repo object for this tool'''
        super(ForgeHgApp, self).install(project)
        repo = HM.Repository(
            name=self.config.options.mount_point,
            tool='hg',
            status='initing')
        ThreadLocalORMSession.flush_all()
        cloned_from_project_id = self.config.options.get('cloned_from_project_id')
        cloned_from_repo_id = self.config.options.get('cloned_from_repo_id')
        if cloned_from_project_id is not None:
            with h.push_config(c, project=M.Project.query.get(_id=cloned_from_project_id)):
                cloned_from = HM.Repository.query.get(_id=cloned_from_repo_id)
                msg = dict(
                    cloned_from_path=cloned_from.full_fs_path,
                    cloned_from_name=cloned_from.app.config.script_name(),
                    cloned_from_url=cloned_from.app.url)
            g.publish('audit', 'repo.clone', msg)
        else:
            g.publish('audit', 'repo.init',
                      dict(repo_name=repo.name, repo_path=repo.fs_path))

