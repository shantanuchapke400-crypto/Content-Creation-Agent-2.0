from core.services.ai_service import ai_service
from core.services.research_service import research_service


class ContentService:
    """Main CreatorOS content generation service."""

    def generate_blog(
        self,
        topic: str,
        tone: str,
        research: str | None = None,
    ) -> str:
        if research is None:
            research = research_service.search(topic)

        prompt = f"""
You are an expert blog writer.

Write a detailed, SEO-friendly blog article.

Topic:
{topic}

Tone:
{tone}

Requirements:
- Catchy title
- Introduction
- Clear headings
- Detailed explanation
- Bullet points where useful
- Professional formatting
- Conclusion
- Human-like writing
- Do not mention AI

Reference Information:
{research}
"""

        return ai_service.generate(prompt)

    def generate_linkedin_post(
        self,
        topic: str,
        tone: str,
        research: str | None = None,
    ) -> str:
        if research is None:
            research = research_service.search(topic)

        prompt = f"""
You are an expert LinkedIn content creator.

Write a professional and engaging LinkedIn post.

Topic:
{topic}

Writing Tone:
{tone}

Requirements:
- Start with a powerful hook.
- Explain the topic simply.
- Share key insights or lessons.
- Keep paragraphs short and readable.
- Add a call-to-action.
- Include 5-10 relevant hashtags.
- Do not mention AI.

Reference Information:
{research}
"""

        return ai_service.generate(prompt)

    def generate_youtube_script(
        self,
        topic: str,
        tone: str,
        research: str | None = None,
    ) -> str:
        if research is None:
            research = research_service.search(topic)

        prompt = f"""
You are a creative short-form video scriptwriter.

Create an engaging YouTube Shorts / Instagram Reels script.

Topic:
{topic}

Tone:
{tone}

Requirements:
- Strong hook
- Conversational tone
- 200-250 words
- Easy to understand
- End with a strong CTA
- Do not mention AI

Information:
{research}
"""

        return ai_service.generate(prompt)

    def generate_instagram_caption(
        self,
        topic: str,
        tone: str,
    ) -> str:
        prompt = f"""
You are an expert Instagram content creator.

Write an engaging Instagram caption.

Topic:
{topic}

Tone:
{tone}

Requirements:
- Start with an attention-grabbing opening.
- Keep the writing natural and engaging.
- Use short paragraphs.
- Include a clear call-to-action.
- Include relevant hashtags.
- Do not mention AI.
"""

        return ai_service.generate(prompt)

    def generate_twitter_thread(
        self,
        topic: str,
        tone: str,
    ) -> str:
        prompt = f"""
You are an expert Twitter/X content creator.

Write an engaging Twitter/X thread.

Topic:
{topic}

Tone:
{tone}

Requirements:
- Start with a strong hook.
- Break the idea into concise posts.
- Make every post useful.
- Keep the language natural and readable.
- End with a strong conclusion or CTA.
- Do not mention AI.
"""

        return ai_service.generate(prompt)

    def generate_newsletter(
        self,
        topic: str,
        tone: str,
    ) -> str:
        prompt = f"""
You are an expert newsletter writer.

Write a high-quality newsletter.

Topic:
{topic}

Tone:
{tone}

Requirements:
- Create a compelling subject/title.
- Write an engaging introduction.
- Explain the topic clearly.
- Use useful sections and headings.
- End with a clear CTA.
- Do not mention AI.
"""

        return ai_service.generate(prompt)

    def generate_email(
        self,
        topic: str,
        tone: str,
    ) -> str:
        prompt = f"""
You are an expert professional email writer.

Write a polished email.

Topic:
{topic}

Tone:
{tone}

Requirements:
- Create an appropriate subject line.
- Write a clear opening.
- Communicate the main message concisely.
- Include a natural closing.
- Do not mention AI.
"""

        return ai_service.generate(prompt)

    def rewrite_content(
        self,
        input_content: str,
        tone: str,
    ) -> str:
        prompt = f"""
You are an expert content editor.

Rewrite the following content.

Tone:
{tone}

Original content:
{input_content}

Requirements:
- Preserve the original meaning.
- Improve clarity and readability.
- Improve structure and flow.
- Remove unnecessary repetition.
- Do not mention AI.
"""

        return ai_service.generate(prompt)

    def summarize_content(
        self,
        input_content: str,
        tone: str,
    ) -> str:
        prompt = f"""
You are an expert summarization assistant.

Summarize the following content.

Tone:
{tone}

Content:
{input_content}

Requirements:
- Preserve the key ideas.
- Remove unnecessary details.
- Make the summary concise.
- Keep important facts and context.
- Do not mention AI.
"""

        return ai_service.generate(prompt)

    def expand_content(
        self,
        input_content: str,
        tone: str,
    ) -> str:
        prompt = f"""
You are an expert content writer.

Expand the following content.

Tone:
{tone}

Original content:
{input_content}

Requirements:
- Preserve the original idea.
- Add useful detail and context.
- Improve structure.
- Avoid unnecessary repetition.
- Do not mention AI.
"""

        return ai_service.generate(prompt)

    def humanize_content(
        self,
        input_content: str,
        tone: str,
    ) -> str:
        prompt = f"""
You are an expert human editor.

Humanize the following content.

Tone:
{tone}

Content:
{input_content}

Requirements:
- Make the writing natural and conversational.
- Remove robotic or repetitive phrasing.
- Preserve the original meaning.
- Improve readability and flow.
- Do not mention AI.
"""

        return ai_service.generate(prompt)

    def generate_seo_title(
        self,
        topic: str,
        tone: str,
    ) -> str:
        prompt = f"""
You are an SEO content specialist.

Generate an SEO-friendly title.

Topic:
{topic}

Tone:
{tone}

Requirements:
- Make the title compelling.
- Clearly communicate the topic.
- Keep it concise.
- Optimize naturally for search intent.
- Do not use misleading clickbait.
"""

        return ai_service.generate(prompt)

    def generate_meta_description(
        self,
        topic: str,
        tone: str,
    ) -> str:
        prompt = f"""
You are an SEO specialist.

Write an SEO meta description.

Topic:
{topic}

Tone:
{tone}

Requirements:
- Clearly summarize the topic.
- Make it compelling.
- Encourage clicks.
- Keep it concise.
- Avoid keyword stuffing.
"""

        return ai_service.generate(prompt)


content_service = ContentService()