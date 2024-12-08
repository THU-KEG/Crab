Generate_Refined_Instruction = '''As a linguist with expertise in contextual language nuances, please refine the #Given Instruction# to increase its specificity and detail, ensuring it aligns more closely with the #Given Output#. 
Please note that refining the instruction will overwrite the #Given Instruction#. Ensure that you do not omit non-text elements such as tables and code, as well as any input text provided in the #Given Instruction#.
This may involve clarifying the subject or object, or defining the circumstances under which the instruction applies. 
You should try your best not to make the #Refined Instruction# become verbose, #Refined Instruction# can only add 10 to 20 words into #Given Instruction#.
Please directly present your modifications, without using any headings or prefixes.

#Given Instruction#
'{Instruction}'

#Given Output#
'{Response}'

#Refined Instruction#
'''



Generate_Constraints_Global = """As a linguist with expertise in contextual language nuances, please add constraints to enrich the #Given Instruction# based on the #Given Output#. 
The goal is to enhance the specificity and detail of the instruction to ensure that the response is more aligned with the output text.



To supplement the #Given instruction# based on the #Given Output#, consider adding details that enhance the response's accuracy and relevance, such as:
1. Desired_Writing_Style: Specify the style requirements for the response to align with the intended message and audience. 
2. Semantic_elements: Clearly articulate the main theme, focus, meaning, or underlying concept of the response.
3. Morphological_Constraints: Outline specific prohibitions, such as avoiding certain words or phrases and refraining from specific formatting styles.
4. Multi-lingual_Constraints: Specify the language(s) in which the response should be written.

#Given Instruction#
'{Instruction}'

#Given Output#
'{Response}'

Please format your response directly in JSON, using 'Constraint_Type' as the key and the specific constraint as its value. Please ensure that the constraints are provided as concise and complete sentences, each containing 10 to 20 words. Additionally, vary the expressions used across different sentences to maintain diversity in phrasing.
If a particular constraint type is not applicable, use the value "NULL". For instance: `"Constraint_Type": "NULL",`.
Do not include any headings or prefixes in your response. 
"""

Generate_Constraints_Local = """As a linguist with expertise in contextual language nuances, please add constraints to enrich the #Given Instruction# based on the #Given Output#. 
The goal is to enhance the specificity and detail of the instruction to ensure that the response is more aligned with the output text.

To supplement the #Given instruction# based on the #Given Output#, consider adding details that enhance the response's accuracy and relevance, such as:
1. Hierarchical_Instructions: Establish a response hierarchy, defining the prioritization and structuring of tasks within the output.
2. Special_Output_Format: Depending on the required format of the output—such as Python, tables, JSON, HTML, LaTeX—impose relevant format constraints.
3. Paragraphs_Constraints: Clearly specify the required number of paragraphs or sections in the text. Additionally, indicate any specific spacing or separators needed—such as horizontal rules, or special symbols like "******"—to enhance readability and visual appeal.
4. Specific_Sentence: Specify a particular phrase to be included either at the beginning or end of the text, clearly indicating its exact placement.
5. Key_Formatting: Specify the formatting style for titles or keywords within the #Given Output#, such as using bold (**bold**), italics (*italics*), or CAPITAL LETTERS. Clearly indicate the specific format to be used, providing examples if necessary, to ensure precise adherence to the desired style. If no specific formatting is required, respond with 'NULL'.
6. Item_Listing_Details: Clearly specify the formatting for individual entries within the text. Direct the use of specific symbols for listing—such as bullet points (•), numbers (1., 2., 3., etc.), or hyphens (-). Ensure that these symbols are explicitly mentioned. You may provide generalized examples, like '- Item Name: Description,' but avoid overly specific examples that could dictate the #Given Output#.

#Given Instruction#
'{Instruction}'

#Given Output#
'{Response}'

Please format your response directly in JSON, using 'Constraint_Type' as the key and the specific constraint as its value. Please ensure that the constraints are provided as concise and complete sentences, each containing 10 to 20 words. Additionally, vary the expressions used across different sentences to maintain diversity in phrasing.
If a specific type of constraint cannot be derived from the #Given Output#, assign the value "NULL". For example: `"Constraint_Type": "NULL",`. 
Ensure that all provided constraints, particularly 'Style_Formatting' and 'Item_Listing_Details', accurately align with the #Given Output#.
Do not include any headings or prefixes in your response.  
"""


Digit_Format_Max_Min = [  # 15
    "Limit the response to a concise paragraph of no fewer than {min} and no more than {max} words to maintain focus and readability.",
    "Limit the text length to no fewer than {min} and no more than {max} words to maintain conciseness.",
    "Limit your response to at least {min} and a maximum of {max} words to encourage precision and conciseness.",
    "Ensure your response contains a minimum of {min} words and does not exceed {max} words to maintain clarity and brevity.",
    "Your answer should include at least {min} words but should be no more than {max} words to keep it concise and precise.",
    "Please limit your reply to between {min} and {max} words to promote succinctness and accuracy.",
    "Craft your response to fall within the range of {min} to {max} words to ensure it is both detailed and concise.",
    "Keep your response within the {min} to {max} word limit to balance thoroughness with readability.",
    "Your response should be at least {min} words long and capped at {max} words to encourage thoroughness and brevity.",
    "Aim for a response that is no less than {min} words and does not surpass {max} words for optimal clarity and focus.",
    "Respond with a text length ranging from {min} to {max} words to ensure it is comprehensive yet succinct.",
    "Keep your response between {min} and {max} words to achieve a balance of detail and conciseness.",
    "Please ensure your response is no shorter than {min} words and no longer than {max} words to maintain precision and conciseness.",
    "Write your response with a word count that falls between {min} and {max} to ensure it is both informative and to the point.",
    "Formulate your answer to include no fewer than {min} words and no more than {max} words to maintain a clear and concise message.",
]

Digit_Format_Min = [
    "Answer with at least {num} words.",
    "Provide an response containing at least {num} words.",
    "Submit an response that contains at least {num} words.",
    "The reply must be at least {num} words long.",
    "Compose a response with no fewer than {num} words.",
    "Ensure that your answer consists of at least {num} words."
]

Digit_Format_Max = [
    "Answer with at most {num} words.",
    "Ensure your answer does not exceed {num} words.",
    "Your response should be no more than {num} words long.",
    "Limit your reply to a maximum of {num} words.",
    "Provide a response that contains no more than {num} words.",
    "The answer must be {num} words or fewer."
]

Digit_Format_Around = [
    "Answer with around {num} words.",
    "Aim for approximately {num} words in your answer.",
    "Your response should be about {num} words long.",
    "Provide an answer that is roughly {num} words.",
    "Target a word count of around {num} words for your reply.",
    "Keep your response close to {num} words in length."
]


Symbol_Format = {
    ",": [
        "Please ensure that your entire response does not contain any commas.",
        "Could you make sure that your response is free of any commas?",
        "Ensure that commas are excluded from your entire response.",
        "Please verify that there are no commas in your entire response.",
        "Confirm that your response contains no commas throughout."
    ],
    ":": [
        "Avoid the use of colons in your response.",
        "Please refrain from including colons in your response.",
        "Ensure that colons are excluded from your response.",
        "Make sure your response does not contain any colons.",
        "Do not use colons in your response."
    ],
    "?": [
        "Do not include any question marks in your response.",
        "Please ensure your response is free of any question marks.",
        "Make sure to exclude question marks from your response.",
        "Your response should not contain question marks.",
        "Avoid using question marks in your response."
    ],
    "!": [
        "Refrain from using exclamation marks in your response.",
        "Please avoid including exclamation marks in your response.",
        "Ensure that your response does not contain any exclamation marks.",
        "Do not use exclamation marks in your response.",
        "Keep exclamation marks out of your response."
    ]
}

Keyword_Format = [  # 15
    "Include keywords such as {keywords} in the response.",
    "Include key terms such as {keywords} in your response.",
    "Include the following keywords in your response: {keywords}.",
    "Ensure the inclusion of key terms such as {keywords}.",
    "Make sure to include the following keywords in your response: {keywords}, to enhance the relevance and clarity.",
    "Your answer should incorporate these essential keywords: {keywords}, to ensure it addresses all key aspects.",
    "Be certain to integrate the keywords {keywords} throughout your response to maintain focus and precision.",
    "In your reply, include the terms {keywords} to emphasize the critical components and provide clarity.",
    "Ensure that your response features the keywords {keywords} to highlight the main points and improve comprehensibility.",
    "To provide a comprehensive answer, make sure to weave in the following keywords: {keywords}.",
    "Your response should feature the terms {keywords} to cover all crucial points effectively.",
    "Incorporate the keywords {keywords} within your reply to ensure it is thorough and informative.",
    "Be sure to mention {keywords} in your response to highlight the key elements and add depth.",
    "Include the keywords {keywords} in your answer to make sure all important aspects are addressed.",
    "To enhance the quality of your response, don't forget to use the keywords {keywords} throughout.",
]

Paragraph_Format = [ #min
    "Each paragraph should not exceed {sentence_number} sentences.",
    "Limit answer to no more than {sentence_number} sentences per paragraph.",
    "Ensure that each paragraph contains no more than {sentence_number} sentences.",
    "Each paragraph should be capped at {sentence_number} sentences.",
    "Restrict the length of each paragraph to a maximum of {sentence_number} sentences.",
    "Do not exceed {sentence_number} sentences in any paragraph.",
    "Keep paragraphs to a maximum of {sentence_number} sentences.",
    "Hold each paragraph to a strict maximum of {sentence_number} sentences.",
    "Ensure paragraphs do not exceed {sentence_number} sentences.",
    "Each paragraph must be limited to {sentence_number} sentences.",
    "Allow no more than {sentence_number} sentences in each paragraph.",
    "Set a cap of {sentence_number} sentences for each paragraph.",
    "Confine each paragraph to {sentence_number} sentences.",
    "Each paragraph should comprise no more than {sentence_number} sentences.",
    "Maintain a limit of {sentence_number} sentences for each paragraph.",
]

Sentence_Format = [ #max
    "Each sentence should have a maximum of {word_number} words.",
    "Limit each sentence to no more than {word_number} words.",
    "Ensure every sentence does not exceed {word_number} words.",
    "Each sentence must be confined to {word_number} words or fewer.",
    "Cap the word count at {word_number} per sentence.",
    "Keep each sentence under {word_number} words.",
    "Allow no more than {word_number} words in each sentence.",
    "Restrict each sentence to {word_number} words maximum.",
    "Each sentence is to contain no more than {word_number} words.",
    "Maintain a word limit of {word_number} per sentence.",
    "Each sentence should not surpass {word_number} words.",
    "Set a limit of {word_number} words for each sentence.",
    "No sentence should exceed {word_number} words in length.",
    "Confine word counts to {word_number} per sentence."
]

Word_Format = [ #max
    "Each word in the answer must have at least {character_number} characters.",
    "Ensure that every word in the answer contains no fewer than {character_number} characters.",
    "Each word of the answer should be at least {character_number} characters long.",
    "Set the minimum character count per word in the answer to {character_number}.",
    "Words in the answer should not be shorter than {character_number} characters.",
    "Maintain a minimum of {character_number} characters in each word of the answer.",
    "Each word in the response must consist of at least {character_number} characters.",
    "No word in the answer should fall below {character_number} characters in length.",
    "Each word within the answer requires a minimum of {character_number} characters.",
    "The words of each answer must meet a minimum length of {character_number} characters.",
    "Impose a minimum length of {character_number} characters for each word in the answer.",
    "Words should hold at least {character_number} characters in any answer.",
    "Ensure a lower limit of {character_number} characters for each word in the answer.",
    "All words in the answer are to be no less than {character_number} characters long."
  ]


Constraints_Check = '''Given the provided text and its corresponding constraint, determine whether the text satisfies the constraint. If the constraint is satisfied, output "YES".  If the constraint is not satisfied, output "NO", provide an explanation of why the text does not satisfy the constraint, and then provide a modified version of the constraint that would make it align with the text. After providing the modified constraint, assess whether the modified constraint serves as a meaningful restriction and include this judgment in your response.

If the original or modified constraint does not serve as a meaningful restriction (i.e., it is too vague or does not impose any actual limit), indicate this by setting "constraint_validity" to "NO". For example, the constraint is "The output should consist of a single paragraph or multiple paragraphs without a specific separation requirement.". This constraint itself has no actual restrictive effect.

The response should be in JSON format with the following structure:
{{
  "satisfaction": "<YES or NO>",
  "explanation": "<reason for the mismatch if applicable>",
  "modified_constraint": "<modified constraint text if applicable>"
  "constraint_validity": "<YES or NO>"
}}
Do not include any headings or prefixes in your response. 

# Example #
Constraint: 'The text must include at least three different colors.'

Text: 'The sky is blue, and the grass is green.'

Response:
{{
  "satisfaction": "NO",
  "explanation": "The text only mentions two colors: blue and green.",
  "modified_constraint": "The text must include at least two different colors.",
  "constraint_validity": "YES"
}}

# Query #
Constraints: '{c}'

Text: '{text}'

Response:'''
