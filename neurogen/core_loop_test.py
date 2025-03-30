#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core_loop_test.py

Full recursive ignition test — routes input through all 10 modules with validation.
"""

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("CoreLoopTest")

from neurogen.feedback_core import process_feedback
from neurogen.contradiction_resolver import check_for_conflicts
from neurogen.mutation_engine import mutate_if_needed
from neurogen.belief_integrity_net import validate_belief
from neurogen.knowledge_graph_engine import KG
from neurogen.semantic_query_engine import query_memory
from neurogen.recursive_context_synth import build_context
from neurogen.meta_prioritization_kernel import get_next_priority
from neurogen.memory_digest import distill_logs
from neurogen.symbolic_reasoning import infer_causal_chain

def core_loop(state):
    log = []

    try:
        # 1. Feedback: Process agent output.
        feedback = process_feedback(agent_name="TestAgent", outcome=state.get("output"))
        if not isinstance(feedback, dict):
            return fail("Feedback core did not return proper dict", log)
        log.append("Feedback processed. Mutation flag: " + str(feedback.get("mutation_required", False)))
    except Exception as e:
        return fail("Feedback core exception: " + str(e), log)

    try:
        # 2. Contradiction: Check belief consistency.
        contradictions = check_for_conflicts(state.get("belief", ""))
        if contradictions:
            log.append("Contradictions: " + str(contradictions))
            return fail("Contradiction resolver blocked.", log)
        log.append("No contradictions found.")
    except Exception as e:
        return fail("Contradiction resolver exception: " + str(e), log)

    try:
        # 3. Mutation: Attempt to mutate state based on feedback.
        mutated = mutate_if_needed(state)
        if not mutated.get("mutated", False):
            return fail("Mutation engine found no mutation.", log)
        log.append("Mutation executed.")
    except Exception as e:
        return fail("Mutation engine exception: " + str(e), log)

    try:
        # 4. Belief Validation: Ensure the new belief is sound.
        belief = mutated.get("new_belief", "")
        if not validate_belief(belief):
            return fail("Belief rejected.", log)
        log.append("Belief validated: " + belief)
    except Exception as e:
        return fail("Belief validation exception: " + str(e), log)

    try:
        # 5. Knowledge Graph: Log belief into the symbolic graph.
        KG.add_belief(belief, context="test", tags=["test"])
        log.append("Belief added to KG.")
    except Exception as e:
        return fail("KG exception: " + str(e), log)

    try:
        # 6. Semantic Query: Retrieve relevant memory entries.
        memory = [
            "Leads convert better after third contact.",
            "Follow-ups increase close rate.",
            "Personalization boosts response."
        ]
        results = query_memory(state.get("query", ""), memory)
        if not results:
            return fail("Semantic query failed.", log)
        log.append("Memory query results: " + str(results))
    except Exception as e:
        return fail("Semantic query exception: " + str(e), log)

    try:
        # 7. Recursive Context: Synthesize prompt context from memory.
        context = build_context(state.get("query", ""), memory)
        log.append("Context: " + context)
    except Exception as e:
        return fail("Context synth exception: " + str(e), log)

    try:
        # 8. Planner: Determine the next high-priority task.
        task = get_next_priority()
        log.append("Next task: " + task)
    except Exception as e:
        return fail("Planner exception: " + str(e), log)

    try:
        # 9. Digest Memory: Compress the output logs into a digest.
        digest = distill_logs([state.get("output")])
        log.append("Digest: " + digest)
    except Exception as e:
        return fail("Digest exception: " + str(e), log)

    try:
        # 10. Symbolic Reasoning: Infer causal chains from process.
        chain = infer_causal_chain(["Outreach -> Call -> Deal"])
        log.append("Symbolic reasoning chain: " + str(chain))
    except Exception as e:
        return fail("Symbolic reasoning exception: " + str(e), log)

    return success(log)

def fail(reason, log):
    logger.error("CORE LOOP FAILURE: %s", reason)
    for line in log:
        logger.error(" - %s", line)
    return {"success": False, "log": log}

def success(log):
    logger.info("CORE LOOP PASSED")
    for line in log:
        logger.info(" - %s", line)
    return {"success": True, "log": log}

if __name__ == "__main__":
    test_state = {
        "output": "Engagement was low due to poor personalization.",
        "belief": "All clients should be sent the same message.",
        "query": "How to increase lead response rate?"
    }
    core_loop(test_state)
