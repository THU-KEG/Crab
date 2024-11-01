Combination_1 = '''{instruction}\n{additional}'''
Combination_2 = '''{instruction} {additional}'''
Combination_3 = '''Please follow the instructions below to generate your response. Additionally, make sure to adhere to the specific constraints mentioned.

Instructions: {instruction}

Additional Constraints: {additional}'''

Combination_4 = ''' Please carefully read and follow the instructions below, along with the additional restrictions provided, to generate your response.

Instructions: {instruction}

Additional Restrictions: {additional}'''

Combination_5 = '''Please ensure you read and follow the detailed instructions and additional constraints provided below to accurately address the query.

- **Instructions**: {instruction}
- **Additional Constraints**: {additional}

Your compliance with these guidelines is essential for a valid response.'''


Combination_6 = '''To generate your response, please adhere to the following:
1. **Instructions**: {instruction}
2. **Additional Constraints**: {additional}

It's important to follow these guidelines closely to ensure your response is appropriate.'''


Combination_7 = '''We invite you to respond by carefully considering the instructions and constraints outlined below. Your thoughtful adherence to these guidelines will greatly enhance the quality of your response.

- **Instructions**: {instruction}
- **Additional Constraints**: {additional}

Thank you for your attention to detail!'''

Combination_8 = '''Hey there! We'd love for you to take a crack at this by following the steps and rules below:
- Here's what you need to do: {instruction}
- Just a couple of things to keep in mind: {additional}

Can't wait to see what you come up with!'''


Combination = [
    (Combination_1, ""),
    (Combination_2, ""),
    (Combination_3, "    "),
    (Combination_4, "    "),
    (Combination_5, "    "),
    (Combination_6, "    "),
    (Combination_7, "    "),
    (Combination_8, "    "),
]

Connectors = [
    " ",
    "{item}",
    "{index}. {item}",
    "- {item}",
    "# {item}",
    "* {item}",
    "> {item}"
]

Base_Combination = [
    (Combination_1, ""),
]

Base_Connectors = [
    "{item}",
]

History_In = '''Please read the text below carefully, but do not generate a response based on it. Please follow the **Instruction Part** to generate the response.
# ============== Text Part: Do not generate responses in this section ==================== #
You are an AI assistant. User will you give you a task. Your goal is to complete the task as faithfully as you can. While performing the task think step-by-step and justify your steps.

Next question: name the right bank and the left bank tributaries of ganga?

The response should begin with a sentence that sets the context for the task, such as 'In order to provide the names of the right and left bank tributaries of the Ganga river, which is the largest and most sacred river in India, I will refer to geographical resources and texts about the Indian river system.'
The list of tributaries should use numbers (1., 2., 3., etc.) followed by the name of the river, and a brief description of its origin and confluence with the Ganga river, separated by a colon (:).
Employ the use of descriptive phrases to paint a vivid picture of the geographical features, and utilize transitional phrases to connect the different steps and ideas in the response.

# ============== Instruction Part ============= #
**Do not generate a token following the above text.**
Please merge the sentences in above **Text Part** into a cohesive paragraph, using conjunctions as needed for clarity and flow. 
Do not modify the original content beyond merging. 
'''

History_Output = '''Here is the merged paragraph:

You are an AI assistant, and your goal is to faithfully complete tasks given by users, meticulously thinking through and justifying each step. Please list the names of the right and left bank tributaries of the Ganga river, the largest and most sacred river in India, referring to geographical resources and texts about the Indian river system. The tributaries should be sequentially numbered (1., 2., 3., etc.), with each number followed by the river's name and a brief description of its origin and confluence with the Ganga, separated by a colon (:). Use descriptive phrases to vividly depict the geographical features and transitional phrases to seamlessly connect the different steps and ideas in the response.'''


Generate_Paraphrase = '''Please read the text below carefully, but do not generate a response based on it. Please follow the **Instruction Part** to generate the response.
# ============== Text Part: Do not generate responses in this section ====================#
'{text}'

# ============== Instruction Part =============#
**Do not generate a token following the above text.**
Please merge the sentences in above **Text Part** into a cohesive paragraph, using conjunctions as needed for clarity and flow. 
Do not modify the original content beyond merging. 
'''

# History_In = '''Please merge the sentences in the provided content into a cohesive paragraph, using conjunctions as needed for clarity and flow. 
# Do not modify the original content beyond merging. 
# Please respond directly and do not include any headings or prefixes in your response. '''

# History_Output = '''OK! Please provide your content.'''

# Generate_Paraphrase = '''Please read the text below carefully, but do not generate a response based on it. 
# # ===== Text Part ===== #
# [{text}]


# # ===== Instruction Part ===== #
# You are a text formatter. Please reformat the text above without responding to it. 
# Merge the sentences in the **Text Part** into a single, cohesive paragraph, using conjunctions as needed for clarity and flow. 
# Ensure that the merged paragraph maintains the original content and meaning, without adding or altering the existing information beyond merging. 
# Start your response with: "Here is the rewritten result of the above text:"'''

System = '''You are a text formatter. You can locate the text section by searching for "# ===== Text Part ===== #" and identify the instruction section by reading beyond "# ===== Instruction Part ===== #". 
Please read the text carefully, but do not generate a response based on it.'''