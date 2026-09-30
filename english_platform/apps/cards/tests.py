from unittest.mock import MagicMock, patch

from django.test import RequestFactory, SimpleTestCase

from apps.cards.views import FlashcardView
from apps.dictionary.presenters import CuratedDictionaryEntry


class FlashcardViewTests(SimpleTestCase):
    def setUp(self) -> None:
        self.factory: RequestFactory = RequestFactory()

    @patch("apps.cards.views.render")
    @patch("apps.cards.views.get_object_or_404")
    @patch("apps.cards.views.UserWord.objects")
    def test_flashcard_view_provides_curated_entry(
        self,
        mock_userword_objects: MagicMock,
        mock_get_object: MagicMock,
        mock_render: MagicMock,
    ) -> None:
        mock_learning_qs = MagicMock()
        mock_learning_qs.exists.return_value = True
        mock_learning_qs.values_list.return_value = [10]
        mock_userword_objects.filter.return_value.select_related.return_value.order_by.return_value = (
            mock_learning_qs
        )

        mock_user = MagicMock()
        mock_user.is_authenticated = True

        mock_word = MagicMock()
        mock_word.word = "characteristic of"
        mock_word.full_translation = {
            "english": "characteristic of",
            "entry_type": "construction",
            "pattern": "[feature] + be characteristic of + [group]",
            "uses": [{"ru": "быть свойственным", "examples": []}],
        }

        mock_user_word = MagicMock()
        mock_user_word.pk = 10
        mock_user_word.word = mock_word
        mock_get_object.return_value = mock_user_word

        mock_render.return_value = MagicMock()

        view = FlashcardView()
        request = self.factory.get("/cards/10/")
        request.user = mock_user

        view.get(request, pk=10)

        mock_render.assert_called_once()
        context = mock_render.call_args[0][2]
        self.assertIn("entry", context)
        self.assertIsInstance(context["entry"], CuratedDictionaryEntry)
        self.assertEqual(context["entry"].english, "characteristic of")
        self.assertEqual(
            context["entry"].pattern, "[feature] + be characteristic of + [group]"
        )
