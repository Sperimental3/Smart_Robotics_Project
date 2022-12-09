import openai

openai.api_key = "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"

BASE_PROMPT = ("Baxter is a bartender robot that have to listen to orders of cocktails "
               "and it must return the ingredients. The orders can be of complex cocktails following a given recipe, "
               "or they can be of separate single ingredients. It is also possible for Baxter to receive a sequence of "
               "orders. If the order is not on the recipes list or it is not one of the four basic ingredients "
               "(Gin, Vermut, Campari, Lemon), Baxter will return \"?\"\n\n"
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
               "Response: ?\n\n"
               "Give me a Campari, then a white russian\n"
               "Response: [Campari] ?\n\n"
               )


def array_eq(arr1, arr2):
    l = len(arr1)
    if l != len(arr2): return False
    for i in range(l):
        if arr1[i] != arr2[i]: return False
    return True


def dict2str(ds):
    if type(ds) != 'list':
        ds = [ds]
    text = ''
    for d in ds:
        text += f'- {d.name} at ({d.pos})\n'

    return text


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
        actions = response["choices"][0]["text"].split('[')

        return actions

    """
    def action_prompt(self, action):
        last_action = f'Action: "{action}"\n'
        print(last_action)
        self.prompt += last_action
        result = self._gpt3()
        diff = {}
        rgx = re.compile(r"\-\ ([A-Z])+\ at\ \(+([\-\+0-9\.]+),\ ([\-\+0-9\.]+),\ ([\-\+0-9\.]+)\)")
        matches = rgx.findall(result)
        new_state = {}
        for match in matches:
            new_state[match[0]] = [float(match[1]), float(match[2]), float(match[3])]

        for key in new_state.keys():
            if key not in self.state: continue
            if array_eq(new_state[key], self.state[key]): continue
            diff[key] = {}
            diff[key]['from'] = self.state[key]
            diff[key]['to'] = new_state[key]

        self.state = new_state
        return diff
    """
