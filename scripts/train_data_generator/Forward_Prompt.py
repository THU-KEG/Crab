Combination_1 = '''{instruction}\n{additional}'''
Combination_2 = '''{instruction}\n\nWhen answering, please ensure that the following constraints are also met.{additional}'''
Combination_3 = '''Please follow the instructions below to generate your response. Additionally, make sure to adhere to the specific constraints mentioned.

Instructions: {instruction}

Additional Constraints: {additional}'''

Combination_4 = '''Please carefully read and follow the instructions below, along with the additional restrictions provided, to generate your response.

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

Combination_9 = '''{additional}\n{instruction}'''
Combination_10 = '''{additional}\n\nQuery:\n{instruction}'''
Combination_11 = '''{instruction}\n\nWhen answering, please ensure that the following constraints are also met.\n{additional}'''

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
    (Combination_2, ""),
]

Base_Connectors = [
    "{item}",
    "- {item}",
    "# {item}",
    "* {item}",
    "> {item}"
]

# Target to long instruction
Long_Combination = [
    (Combination_9, ""),
    (Combination_10, ""),
    (Combination_11, ""),
]

