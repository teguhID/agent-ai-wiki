import re
import json

import utils.wiki_utils as wiki_utils

# ------------------ AGENT RESPONSE ------------------

def agent_respond(query: str, session_id: str, chain_with_history) -> str:
    full_context = ""
    
    resp_step = chain_with_history.invoke(
        {"input": wiki_utils.prompt_step(query)},
        config={"configurable": {"session_id": session_id}}
    )

    resp_step = re.search(r'```json\n(.*?)\n```', resp_step.content, re.DOTALL)
    if resp_step:
        step_data = resp_step.group(1)
        step_data = json.loads(step_data)
    else:
        return "Could not extract JSON content"

    # Process each step and extract content
    for data in step_data:
        context = wiki_utils.extract_content(data['url'], session_id, chain_with_history)
        if full_context:
            full_context += "\n---\n" + context
        else:
            full_context = context

    # Generate the final answer based on the query
    final_answer = chain_with_history.invoke(
        {"input": wiki_utils.prompt_result(full_context, query)},
        config={"configurable": {"session_id": session_id}}
    )

    return final_answer.content

