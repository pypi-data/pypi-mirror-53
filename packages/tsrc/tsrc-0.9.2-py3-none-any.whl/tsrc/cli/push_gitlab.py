""" Entry point for tsrc push """


import argparse
import itertools
import textwrap
from typing import cast, Any, List, Optional, Set  # noqa

from gitlab import Gitlab
from gitlab.v4.objects import Group, User, Project, ProjectMergeRequest  # noqa
from gitlab.exceptions import GitlabGetError
import cli_ui as ui

import tsrc
from tsrc.cli.push import RepositoryInfo


WIP_PREFIX = "WIP: "


class UserNotFound(tsrc.Error):
    def __init__(self, username: str) -> None:
        self.username = username
        super().__init__("No user found with this username : %s" % self.username)


class TooManyUsers(tsrc.Error):
    def __init__(self, max_users: int) -> None:
        self.max_users = max_users
        super().__init__("More than %s users found" % self.max_users)


class AmbiguousUser(tsrc.Error):
    def __init__(self, query: str) -> None:
        self.query = query
        super().__init__("Found more that one user matching query: %s" % self.query)


class NoGitLabToken(tsrc.Error):
    def __init__(self) -> None:
        message = textwrap.dedent(
            """\
            Could not find GitLab token in tsrc config file
            Please check  https://tankerhq.github.io/tsrc/ref/formats/#tsrcyml_format
            for details\
            """
        )
        super().__init__(message)


class FeatureNotAvailable(tsrc.Error):
    def __init__(self, feature: str) -> None:
        self.name = feature
        message = (
            "The '%s' feature is not available on your GitLab installation" % self.name
        )
        super().__init__(message)


def get_token() -> str:
    config = tsrc.parse_tsrc_config()
    try:
        res = config["auth"]["gitlab"]["token"]
        return cast(str, res)
    except KeyError:
        raise NoGitLabToken() from None


def wipify(title: str) -> str:
    if not title.startswith(WIP_PREFIX):
        return WIP_PREFIX + title
    else:
        return title


def unwipify(title: str) -> str:
    if title.startswith(WIP_PREFIX):
        return title[len(WIP_PREFIX) :]
    else:
        return title


class PushAction(tsrc.cli.push.PushAction):
    def __init__(
        self,
        repository_info: RepositoryInfo,
        args: argparse.Namespace,
        gitlab_api: Optional[Gitlab] = None,
    ) -> None:
        super().__init__(repository_info, args)
        self.gitlab_api = gitlab_api
        self.group = None  # type: Optional[Group]
        self.project = None  # type: Optional[Project]
        self.review_candidates = []  # type: List[User]

    def _get_group(self, group_name: str) -> Optional[Group]:
        assert self.gitlab_api
        try:
            return self.gitlab_api.groups.get(group_name)
        except GitlabGetError as e:
            if e.response_code == 404:
                return None
            else:
                raise

    def check_gitlab_feature(self, name: str) -> None:
        assert self.gitlab_api
        # Note: don't worry, the http request is cached under the hood by
        # the python-gitlab library. This should be fine
        features = self.gitlab_api.features.list()
        names = [x.name for x in features]
        if name not in names:
            raise FeatureNotAvailable(name)

    def setup_service(self) -> None:
        if not self.gitlab_api:
            token = get_token()
            self.gitlab_api = Gitlab(
                self.repository_info.repository_login_url, private_token=token
            )

        assert self.project_name
        self.project = self.gitlab_api.projects.get(self.project_name)
        group_name = self.project_name.split("/")[0]
        self.group = self._get_group(group_name)

    def handle_assignee(self) -> User:
        assert self.requested_assignee
        return self.get_reviewer_by_username(self.requested_assignee)

    def handle_reviewers(self) -> List[User]:
        self.check_gitlab_feature("multiple_merge_request_assignees")
        res = list()
        for requested_username in self.args.reviewers:
            username = requested_username.strip()
            approver = self.get_reviewer_by_username(username)
            res.append(approver)
        return res

    def get_reviewer_by_username(self, username: str) -> User:
        assert self.project
        in_project = self.get_users_matching(self.project.members, username)
        if self.group:
            in_group = self.get_users_matching(self.group.members, username)
        else:
            in_group = list()
        candidates = list()
        seen = set()  # type: Set[int]
        for user in itertools.chain(in_project, in_group):
            if user.id in seen:
                continue
            candidates.append(user)
            seen.add(user.id)
        if not candidates:
            raise UserNotFound(username)
        if len(candidates) > 1:
            raise AmbiguousUser(username)
        return candidates[0]

    def get_users_matching(self, members: Any, query: str) -> List[User]:
        res = members.list(active=True, query=query, per_page=100, as_list=False)
        if res.next_page:
            raise TooManyUsers(100)
        return cast(List[User], res)

    def post_push(self) -> None:
        merge_request = self.ensure_merge_request()
        assert self.gitlab_api
        if self.args.close:
            ui.info_2("Closing merge request #%s" % merge_request.iid)
            merge_request.state_event = "close"
            merge_request.save()
            return

        assignee = None
        if self.requested_assignee:
            assignee = self.handle_assignee()
            if assignee:
                ui.info_2("Assigning to", assignee.username)

        title = self.handle_title(merge_request)
        merge_request.title = title
        merge_request.remove_source_branch = True
        if self.requested_target_branch:
            merge_request.target_branch = self.requested_target_branch
        if assignee:
            merge_request.assignee_id = assignee.id

        if self.args.reviewers:
            approvers = self.handle_reviewers()
            if approvers:
                ui.info_2(
                    "Requesting approvals from", ", ".join(x.name for x in approvers)
                )
                merge_request.approvals.set_approvers([x.id for x in approvers])

        merge_request.save()

        if self.args.accept:
            merge_request.merge(merge_when_pipeline_succeeds=True)

        ui.info(ui.green, "::", ui.reset, "See merge request at", merge_request.web_url)

    def handle_title(self, merge_request: ProjectMergeRequest) -> str:
        # If explicitely set, use it
        if self.requested_title:
            return self.requested_title
        else:
            # Else change the title if we need to
            title = merge_request.title  # type: str
            if self.args.ready:
                return unwipify(title)
            if self.args.wip:
                return wipify(title)
            return title

    def find_merge_request(self) -> Optional[ProjectMergeRequest]:
        assert self.remote_branch
        assert self.project
        res = self.project.mergerequests.list(
            state="opened", source_branch=self.remote_branch, all=True
        )
        if len(res) >= 2:
            raise tsrc.Error(
                "Found more than one opened merge request with the same branch"
            )
        if not res:
            return None
        return res[0]

    def create_merge_request(self) -> ProjectMergeRequest:
        assert self.project
        if self.requested_target_branch:
            target_branch = self.requested_target_branch
        else:
            target_branch = self.project.default_branch
        assert self.remote_branch
        return self.project.mergerequests.create(
            {
                "source_branch": self.remote_branch,
                "target_branch": target_branch,
                "title": self.remote_branch,
            }
        )

    def ensure_merge_request(self) -> ProjectMergeRequest:
        merge_request = self.find_merge_request()
        if merge_request:
            ui.info_2("Found existing merge request: !%s" % merge_request.iid)
            return merge_request
        else:
            return self.create_merge_request()
