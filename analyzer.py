
import time
import logging
import tiktoken

from google import genai
from google.genai import types
from pydantic import ValidationError

from config import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    MAX_OUTPUT_TOKENS
)

from schemas import TextAnalysis
from prompts import SYSTEM_PROMPT, build_user_prompt


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)



client = genai.Client(
    api_key=GEMINI_API_KEY,
    http_options=types.HttpOptions(
        api_version="v1beta"
    )
)


def estimate_tokens(text: str) -> int:

    try:
        encoding = tiktoken.encoding_for_model(
            "gpt-4o"
        )
    except KeyError:
        encoding = tiktoken.get_encoding(
            "cl100k_base"
        )

    return len(encoding.encode(text))


def analyze_text(text: str) -> dict:

    start_time = time.perf_counter()

    user_prompt = build_user_prompt(text)

    estimated_input_tokens = estimate_tokens(
        SYSTEM_PROMPT + user_prompt
    )

    logger.info("Starting Gemini analysis")

    try:

        response = client.models.generate_content(
            model=GEMINI_MODEL,

            contents=user_prompt,

            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,

                response_mime_type="application/json",

                response_schema=TextAnalysis,

                max_output_tokens=MAX_OUTPUT_TOKENS,

                temperature=0.2
            )
        )

        if not response.text:
            raise ValueError(
                "Gemini returned an empty response."
            )

        # Validate Gemini response
        analysis = TextAnalysis.model_validate_json(
            response.text
        )

        latency = time.perf_counter() - start_time

        # Extract token usage
        usage = response.usage_metadata

        if usage:

            input_tokens = usage.prompt_token_count or 0

            output_tokens = usage.candidates_token_count or 0

            total_tokens = usage.total_token_count or 0

        else:

            input_tokens = estimated_input_tokens

            output_tokens = 0

            total_tokens = input_tokens

        result = analysis.model_dump()

        result["usage"] = {

            "estimated_input_tokens": estimated_input_tokens,

            "actual_input_tokens": input_tokens,

            "output_tokens": output_tokens,

            "total_tokens": total_tokens,

            "latency_seconds": round(
                latency, 3
            ),

            "model": GEMINI_MODEL

        }

        logger.info(
            "Gemini analysis completed successfully"
        )

        logger.info(
            f"Total tokens: {total_tokens}"
        )

        return result

    except ValidationError:

        logger.exception(
            "Pydantic validation failed"
        )

        raise

    except Exception:

        logger.exception(
            "Gemini analysis failed"
        )

        raise
