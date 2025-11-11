from openai import OpenAI
from django.conf import settings
from core.models import Article, ArticleSummary


class SummaryService:
    client: OpenAI

    def __init__(self) -> None:
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def generate_summary(self, article: Article) -> ArticleSummary:
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a helpful assistant that summarizes "
                            "technology news articles. Provide concise, "
                            "informative summaries in 2-3 sentences."
                        )
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Please summarize this article:\n\n"
                            f"Title: {article.title}\n"
                            f"Content: {article.content}"
                        )
                    }
                ],
                max_tokens=150,
                temperature=0.7
            )

            summary_text = response.choices[0].message.content.strip()

            summary = ArticleSummary.objects.create(
                article=article,
                summary_text=summary_text
            )

            return summary

        except Exception as e:
            raise Exception(f"Failed to generate summary: {str(e)}")

    def get_or_create_summary(self, article: Article) -> ArticleSummary:
        try:
            return article.summary
        except ArticleSummary.DoesNotExist:
            return self.generate_summary(article)
