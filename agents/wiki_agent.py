import re
import json

import utils.wiki_utils as wiki_utils
import services.genai_service as genai_service

# ------------------ AGENT RESPONSE ------------------
def agent_respond(query: str) -> str:
    try:
        full_context = ""

        # Generate the steps to get the information
        resp_step = genai_service.generate_text(wiki_utils.prompt_step(query))
        resp_step = re.search(r'```json\n(.*?)\n```', resp_step, re.DOTALL)
        
        if resp_step:
            step_data = resp_step.group(1)
            step_data = json.loads(step_data)
        else:
            return "Could not extract JSON content"

        # Process each step and extract content
        for data in step_data:
            context = wiki_utils.extract_content(data['url'], full_context)
            if full_context:
                full_context += "\n---\n" + context
            else:
                full_context = context

        # Generate the final answer based on the query
        final_answer = genai_service.generate_text(wiki_utils.prompt_result(full_context, query))
        
        return final_answer
            
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}, Response text: ")
        return "Terjadi kesalahan dalam memproses langkah-langkah URL."
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return "Terjadi kesalahan dalam memproses permintaan."
