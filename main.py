import autogen

llm_config = {
    "timeout": 600,
    "cache_seed": 44,  # change the seed for different trials
    "config_list": autogen.config_list_from_json(
        "OAI_CONFIG_LIST",
        filter_dict={
            "model": ["gpt-4-32k"]
            },
    ),
    "temperature": 0,
}

# create an AssistantAgent instance named "assistant"
python_assistant = autogen.AssistantAgent(
    name="PythonAssistant",
    system_message="You're an expert back-end Python developer. Here are our technology preferences: Please use the FastAPI framework to serve the front-end and any required tables. Please also use Alembic and SQLAlchemy to create any database tables needed.",
    llm_config={
    "timeout": 600,
    "cache_seed": 44,  # change the seed for different trials
    "config_list": autogen.config_list_from_json(
            "OAI_CONFIG_LIST",
            filter_dict={
                "model": ["gpt-4"]
                },
        ),
        "temperature": 0,
    },
    is_termination_msg=lambda x: True if "TERMINATE" in x.get("content") else False,
)

# create an AssistantAgent instance named "assistant"
front_end_assistant = autogen.AssistantAgent(
    name="FrontEndDeveloperAssistant",
    system_message="You are an expert HTML, CSS, and JavaScript engineer. You'll be given a task by the user to produce a front-end. Please provide all HTML, CSS, and JavaScript. First, think step-by-step and make a plan for your work, then write the code, all in one message. Reply with 'TERMINATE' to ask the user for feedback.",
    llm_config={
    "timeout": 600,
    "cache_seed": 44,  # change the seed for different trials
    "config_list": autogen.config_list_from_json(
            "OAI_CONFIG_LIST",
            filter_dict={
                "model": ["gpt-4"]
                },
        ),
        "temperature": 0,
    },
    is_termination_msg=lambda x: True if "TERMINATE" in x.get("content") else False,
)

front_end_critic = autogen.AssistantAgent(
    name="FrontEndDeveloperCritic",
    system_message="You are a critic of the Front-end agent. Please review the work of the front-end agent and give feedback on the quality of the output. Ensure templates, animations, and other materials are complex enough to be compelling, and provide good next steps for a second iteration of the html & css.",
    llm_config={
    "timeout": 600,
    "cache_seed": 44,  # change the seed for different trials
    "config_list": autogen.config_list_from_json(
            "OAI_CONFIG_LIST",
            filter_dict={
                "model": ["gpt-4"]
                },
        ),
        "temperature": 0,
    },
    is_termination_msg=lambda x: True if "TERMINATE" in x.get("content") else False,
)

image_assistant = autogen.AssistantAgent(
    name="ImageAssistant",
    llm_config={
        "timeout": 1200,
        "config_list": autogen.config_list_from_json(
            "OAI_CONFIG_LIST",
            filter_dict={
                "model": ["gpt-4"]
                },
        ),
        "temperature": 1,
    },
    system_message="You are an image assistant. Please write a compelling prompt to create an image using DALL-E. Reply with 'TERMINATE' to stop the conversation.",
    
    is_termination_msg=lambda x: True if "TERMINATE" in x.get("content") else False,
)

# create a UserProxyAgent instance named "user_proxy"
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="TERMINATE",
    is_termination_msg=lambda x: True if "TERMINATE" in x.get("content") else False,
    max_consecutive_auto_reply=10,
    code_execution_config={
        "work_dir": "agent_code",
        "use_docker": False,
    },
)


# chat_results = user_proxy.initiate_chats(
#     [
#         {
#             "recipient": front_end_assistant,
#             "message": "Can you craft a compelling blog post template with a engaging SVG animation, suitable for use on a template website. Please provide all HTML, CSS, and JavaScript.",
#             "clear_history": True,
#             "silent": False,
#             "summary_method": "reflection_with_llm",
#         },
#         {
#             "recipient": python_assistant,
#             "message": " serve posts, tags, authors, and any other related tables. ",
#             "summary_method": "reflection_with_llm",
#         },
#         {
#             "recipient": image_assistant,
#             "message": "Please create any images that might be helpful as placeholders for the blog post template, or as background images.",
#         },
#     ]
# )

# for i, chat_res in enumerate(chat_results):
#     print(f"*****{i}th chat*******:")
#     print(chat_res.summary)
#     print("Human input in the middle:", chat_res.human_input)
#     print("Conversation cost: ", chat_res.cost)
#     print("\n\n")
    
    
groupchat = autogen.GroupChat(
    agents=[front_end_assistant, front_end_critic], messages=["Can you craft a compelling blog post template with a engaging SVG animation, suitable for use on a template website, and and api that will serve posts, tags, authors, and any other related tables"], max_round=12, speaker_selection_method="round_robin"
)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

# Start chatting with boss_aid as this is the user proxy agent.
user_proxy.initiate_chat(
    manager,
    n_results=3,
)

print(groupchat.chat_messages_for_summary())

groupchat = autogen.GroupChat(
    agents=[python_assistant], messages=["Can you craft an api that will serve posts, tags, authors, and any other related tables for a basic blogging platform"], max_round=12, speaker_selection_method="round_robin"
)