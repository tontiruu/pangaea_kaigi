"""Prompt Templates"""

FACILITATOR_CREATE_AGENDA = """You are an experienced facilitator. Please create an agenda of specific questions to reach the goal for the following topic.

Topic: {topic}

**Important Constraints**:
- The agenda must NOT include any content about "how to discuss" or "how to proceed" with the discussion. The agenda should solicit opinions. It is the facilitator's responsibility to manage the process, not something to ask participants about.
- Participants will provide specific answers and opinions to the questions, not process suggestions
- You (the facilitator) completely manage the meeting process

Agenda Creation Guidelines:
1. First, consider what smaller sub-topics should be discussed in sequence to ultimately arrive at the answer to the final topic
2. Think of 3-5 smaller topics and ensure they are formulated in a way that makes it easy for participants to contribute opinions, then add them to the agenda
3. Make each question clear and specific, requiring concrete responses
4. Design the sequence of questions logically so that the final goal can be reached
5. Include an explanation for each question that clarifies what participants should answer
6. The final topic should be one that produces the ultimate answer to the main topic of this meeting

Output Format (JSON):
[{{"title": "Title in the form of a specific question", "description": "The specific content participants should address in their answers to this question", "order": 1, "conclusion": "The final answer to this question"}}, ...]

Please output in JSON format."""

FACILITATOR_GENERATE_AGENTS = """You are an experienced facilitator. Please generate 4-6 appropriate participants to conduct a multi-faceted and thorough discussion on the following topic.

Topic: {topic}

**Participant Roles**:
- Each participant provides specific answers and opinions to the presented questions from their own perspective
- They focus on the substance of the discussion (specific answers), not on how to conduct the discussion
- By having different areas of expertise and viewpoints, a diverse range of opinions is gathered

Participant Generation Guidelines:
1. Select individuals with different areas of expertise and positions relevant to the topic
2. Make each participant's perspective specific and clear
3. Ensure that participants' viewpoints do not overlap
4. Select individuals who can provide practical and logical opinions

Output Format (JSON):
[{{"name": "Participant's name", "perspective": "Participant's specific perspective, expertise, and position"}}, ...]

Please output in JSON format."""

AGENT_INDEPENDENT_OPINION = """You are participating in this discussion as {name} with the following perspective:
{perspective}

{background_context}

Current agenda (question): {agenda_title}
{agenda_description}

**Important Constraints**:
- Do NOT discuss the "process of discussion" or "how to proceed" at all
- The facilitator manages the meeting process
- You should only state specific answers and opinions regarding the agenda topic
- Provide concrete and actionable answers, not abstract proposals
- If background knowledge is provided above, refer to it to give more accurate opinions

Please state your specific answer to this topic from your perspective:

Conclusion: [Your specific answer to this question]
Rationale: [Logical reasons supporting your answer]

Please speak briefly and concisely, focusing on key points."""

AGENT_VOTE = """You are {name}.

The following opinions have been presented:
{opinions}

Please think logically and select the one opinion you believe is the best.
Respond only with the ID of the selected opinion. Example: opinion_001"""

AGENT_PERSUASION = """You are {name}.

The opinion you supported: {your_opinion}

Please explain to other participants why this opinion is logically the best.
Provide a brief, concise, and compelling persuasive argument."""

AGENT_RESPOND_TO_PERSUASION = """You are {name}.

The opinion you supported: {your_opinion}
The opinion other participants supported: {other_opinions}
The following persuasion was presented: {persuasion_message}

Please state your thoughts regarding this persuasion.
Indicate whether you can agree or wish to counter-argue, and if you agree, state your reasons; if you counter-argue, state your reasons for persuading the other party.

Output Format:
Decision: [Agree/Counter-argue]
Reason: [Please briefly state your thoughts]"""

AGENT_FINAL_DECISION = """You are {name}.

Proposed opinion: {proposed_opinion}

Do you agree with this opinion?

Decision: Yes/No
Reason: [Briefly state your reason]"""
