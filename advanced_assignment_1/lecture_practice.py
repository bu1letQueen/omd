class EmojiMixin:
    def to_emoji(self):
        env_to_emoji = {
            "grass": "🌿",
            "fire": "🔥",
            "water": "💧",
            "electric": "⚡",
        }
        if self.poketype in env_to_emoji:
            modified_poketype = env_to_emoji[self.poketype]
        else:
            modified_poketype = self.poketype
        return modified_poketype


class Pokemon(EmojiMixin):
    def __init__(self, name, poketype):
        self.name = name
        self.poketype = poketype

    def __str__(self):
        modified_poketype = self.to_emoji()
        return f'{self.name}/{modified_poketype}'


# tests

# базовый кейс: известный тип должен стать эмодзи в строке
bulbasaur = Pokemon(name="Bulbasaur", poketype="grass")
assert str(bulbasaur) == "Bulbasaur/🌿"

# неизвестный тип: должен остаться как есть
mew = Pokemon(name="Mew", poketype="psychic")
assert str(mew) == "Mew/psychic"

# повторный вызов str не должен ломаться и не должен менять исходный poketype
pikachu = Pokemon(name="Pikachu", poketype="electric")
assert str(pikachu) == "Pikachu/⚡"
assert str(pikachu) == "Pikachu/⚡"
assert pikachu.poketype == "electric"

print("Все тесты прошли")

