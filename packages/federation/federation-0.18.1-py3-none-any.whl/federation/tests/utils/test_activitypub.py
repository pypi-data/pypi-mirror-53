import json
from unittest.mock import patch, Mock

from federation.entities.activitypub.entities import ActivitypubFollow, ActivitypubPost
from federation.tests.fixtures.payloads import (
    ACTIVITYPUB_FOLLOW, ACTIVITYPUB_POST, ACTIVITYPUB_POST_OBJECT, ACTIVITYPUB_POST_OBJECT_IMAGES)
from federation.utils.activitypub import retrieve_and_parse_document, retrieve_and_parse_profile


class TestRetrieveAndParseDocument:
    @patch("federation.utils.activitypub.fetch_document", autospec=True, return_value=(None, None, None))
    def test_calls_fetch_document(self, mock_fetch):
        retrieve_and_parse_document("https://example.com/foobar")
        mock_fetch.assert_called_once_with(
            "https://example.com/foobar", extra_headers={'accept': 'application/activity+json'},
        )

    @patch("federation.utils.activitypub.fetch_document", autospec=True, return_value=(
        json.dumps(ACTIVITYPUB_FOLLOW), None, None),
    )
    @patch.object(ActivitypubFollow, "post_receive")
    def test_returns_entity_for_valid_document__follow(self, mock_post_receive, mock_fetch):
        entity = retrieve_and_parse_document("https://example.com/foobar")
        assert isinstance(entity, ActivitypubFollow)

    @patch("federation.utils.activitypub.fetch_document", autospec=True, return_value=(
            json.dumps(ACTIVITYPUB_POST_OBJECT), None, None),
    )
    def test_returns_entity_for_valid_document__post__without_activity(self, mock_fetch):
        entity = retrieve_and_parse_document("https://example.com/foobar")
        assert isinstance(entity, ActivitypubPost)

    @patch("federation.utils.activitypub.fetch_document", autospec=True, return_value=(
            json.dumps(ACTIVITYPUB_POST_OBJECT_IMAGES), None, None),
    )
    def test_returns_entity_for_valid_document__post__without_activity__with_images(self, mock_fetch):
        entity = retrieve_and_parse_document("https://example.com/foobar")
        assert isinstance(entity, ActivitypubPost)
        assert len(entity._children) == 1
        assert entity._children[0].url == "https://files.mastodon.social/media_attachments/files/017/792/237/original" \
                                          "/foobar.jpg"

    @patch("federation.utils.activitypub.fetch_document", autospec=True, return_value=(
        json.dumps(ACTIVITYPUB_POST), None, None),
    )
    def test_returns_entity_for_valid_document__post__wrapped_in_activity(self, mock_fetch):
        entity = retrieve_and_parse_document("https://example.com/foobar")
        assert isinstance(entity, ActivitypubPost)

    @patch("federation.utils.activitypub.fetch_document", autospec=True, return_value=('{"foo": "bar"}', None, None))
    def test_returns_none_for_invalid_document(self, mock_fetch):
        entity = retrieve_and_parse_document("https://example.com/foobar")
        assert entity is None


class TestRetrieveAndParseProfile:
    @patch("federation.utils.activitypub.retrieve_and_parse_document", autospec=True)
    def test_calls_retrieve_and_parse_document(self, mock_retrieve):
        retrieve_and_parse_profile("https://example.com/profile")
        mock_retrieve.assert_called_once_with("https://example.com/profile")

    @patch("federation.utils.activitypub.fetch_document", autospec=True, return_value=('{"foo": "bar"}', None, None))
    def test_returns_none_on_invalid_document(self, mock_fetch):
        profile = retrieve_and_parse_profile("https://example.com/profile")
        assert profile is None

    @patch("federation.utils.activitypub.retrieve_and_parse_document", autospec=True)
    def test_calls_profile_validate(self, mock_retrieve):
        mock_profile = Mock()
        mock_retrieve.return_value = mock_profile
        retrieve_and_parse_profile("https://example.com/profile")
        assert mock_profile.validate.called
