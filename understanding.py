import openai

openai.api_key = "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"

BASE_PROMPT = ("Baxter is a bartender robot that have to listen to orders of cocktails "
               "and it must return the ingredients. The orders can be of complex cocktails following a given recipe, "
               "or they can be of separate single ingredients. It is also possible for Baxter to receive a sequence of "
               "orders. If the order is not on the recipes list or it is not one of the four basic ingredients "
               "(Gin, Vermut, Campari, Lemon), Baxter will return \"[?]\"\n\n"
               "Recipes:\n"
               "Martini: Gin, Vermut\n"
               "Gin lemon: Gin, Lemon\n"
               "Negroni: Gin, Vermut, Campari\n\n"
               "Examples:\n\n"
               "Hey Baxter, give me a Negroni\n"
               "Response: [Gin, Vermut, Campari]\n\n"
               "Hey Baxter, give me a Martini\n"
               "Response: [Gin, Vermut]\n\n"
               "A Negroni please\n"
               "Response: [Gin, Vermut, Campari]\n\n"
               "I want a Gin lemon\n"
               "Response: [Gin, Lemon]\n\n"
               "I just want a simple Vermut\n"
               "Response: [Vermut]\n\n"
               "Baxter, a Campari please\n"
               "Response: [Campari]\n\n"
               "Baxter I want a Martini, then a Campari\n"
               "Response: [Gin, Vermut] [Campari]\n\n"
               "Serve me a gin lemon, then a Vermut\n"
               "Response: [Gin, Lemon] [Vermut]\n\n"
               "Serve me a Margarita\n"
               "Response: [?]\n\n"
               "Give me a Campari, then a white russian\n"
               "Response: [Campari] [?]\n\n"
               )


class Understander:
    def __init__(self):
        self.prompt = BASE_PROMPT

    def understand(self, phrase):
        request = self.prompt + phrase + "\nResponse:"
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=request,
            temperature=0.0,
            max_tokens=400,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        print(response)
        not_clean_orders = response["choices"][0]["text"].split('[')

        orders = []

        for i, not_clean_order in enumerate(not_clean_orders):
            if i == 0:
                continue

            order = []

            for not_clean_ingredient in not_clean_order.split(','):
                ingredient = "".join([j for j in not_clean_ingredient if j.isalpha() or j == '?'])
                ingredient = ingredient.lower()
                assert ingredient == "gin" or ingredient == "campari" or \
                       ingredient == "vermut" or ingredient == "lemon" or ingredient == "?"
                order.append(ingredient)

            orders.append(order)

        return orders
