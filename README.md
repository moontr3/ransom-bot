# Ransom bot

A Discord bot that styles given text as a ransom note with a lot of customizations.

## How to use

[Invite the bot to a server](https://discord.com/oauth2/authorize?client_id=1273037580925009941) <sup>(24/7 uptime is not guaranteed)

_or_

- Clone the repository<br>
```sh
git clone https://github.com/moontr3/ransom-bot.git
```

- Install the required libraries
```sh
pip install -r requirements.txt
```

- Put your token in a `.env` file
```
BOT_TOKEN=<your_token>
```

- Put your ID in the admin list in [`config.py`]('https://github.com/moontr3/ransom-bot/blob/main/config.py')

- Launch the bot
```sh
python main.py
```

- Use `!ransom <text>` to style your text like a ransom note. **This does not support styling settings, unlike slash commands.**

- To access slash commands, send an `!st` command in a server with your bot and reload your Discord client.

## Using as a library

> [!NOTE]
> This can be used as a library and completely works with `colorama` in most terminals, just with different BG colors.

Download [`styler.py`]('https://github.com/moontr3/ransom-bot/blob/main/styler.py') and put it in your project.


### `styler.style_single_string() -> str` function
Randomly styles a string.

#### Arguments

<sup>`*` - required</sup>

| Name | Type | Description |
| ----- | ----- | ----- |
| * `string`         | `str`  | Text to randomly style |
| `reset`          | `bool` | Whether to reset the style after the text (`[0m`) |
| `excluded_pairs` | `List[Tuple[int, int]]` | (BG, Text) color pairs to not generate (useful if you want to exclude styles like white text on white BG etc.) |


#### Example

```py
import styler

text = styler.style_single_string('Hello, World!')
```


### `styler.style_text() -> str` function
Styles given text with the desired settings.


#### Arguments

<sup>`*` - required</sup>

> [!NOTE]
> `codeblock` choices are only supported in Discord.
> 
> To use this library in your own Discord bot, do not forget to put ` ```ansi ` on a new line before your text and ` ``` ` on a new line after your text after using this function.

| Name | Type | Description |
| ----- | ----- | ----- |
| * `text`         | `str`  | Text to style |
| `individual_styling` | `letter` \| `word` | `letter` - individually style each letter<br>`word` - individually style each word |
| `word_separation` | `newline` \| `twonewlines` \| `codeblock` \| `spaces` | `newline` - Put a newline `\n` between each word<br>`twonewlines` - Put two newlines `\n\n` between each word<br>`codeblock` - Put each word in a separate codeblock<br>`spaces` - Put 2 spaces between each word |
| `newline_separation` | `newline` \| `twonewlines` \| `codeblock` | `newline` - As-is; put a newline `\n` between each line<br>`twonewlines` - Put two newlines `\n\n` between each line<br>`codeblock` - Put each line in a separate codeblock |
| `symbol_separation` | `spacebetween` \| `spacein` \| `both` \| `none` | _Doesn't do anything if `individual_styling` is set to `word`_<br>`spacebetween` - Put a space between each letter<br>`spacein` - Put a space either on the left, right, both or no sides of the letter's BG<br>`both` - Both of the above<br>`none` - None of the above |
| `case` | `asis` \| `random` \| `allcaps` \| `alllower` | `asis` - Leave the text case as-is<br>`random` - Randomly choose between lower and upper case for each letter<br>`allcaps` - Make all letters uppercase<br>`alllower` - Make all letters lowercase |


#### Example

```py
import styler

text = styler.style_text('Hello, World!')

# Using for a codeblock in Discord
codeblock = '```ansi\n' + text + '\n```'
```


### `styler.Style()` class
Class to create custom styled text.

> [!NOTE]
> To reset the formatting, put `\u001b[0m` after your text.


#### Arguments

| Name | Type | Description |
| ----- | ----- | ----- |
| `fg` | `int` | Foreground/text color.<br>Below are the names of the colors that Discord uses. Other applications can display these differently.<br>`30` - Gray blue<br>`31` - Red<br>`32` - Green<br>`33` - Yellowuoise<br>`34` - Blue<br>`35` - Pink<br>`36` - Cyan<br>`37` - White |
| `bg` | `int` | Background color.<br>Below are the names of the colors that Discord uses. Other applications can display these differently.<br>`40` - Firefly dark blue<br>`41` - Orange<br>`42` - Marble blue<br>`43` - Greyish turquoise<br>`44` - Gray<br>`45` - Indigo<br>`46` - Light gray<br>`47` - White |
| `bold` | `bool` | Whether the styled text will be bold |
| `underline` | `bool` | Whether the styled text will be underlined |


#### `Style.get_text(self) -> str` function
Returns an ASCII prefix of the style.


#### Usage

```py
import styler

style = styler.Style(32, 40, True, False)
# This style will make a green bold text on a dark blue background.

text = style.get_text() + 'Hello, World' + '\u001b[0m'
# '\u001b[0m' is used to reset the formatting back to default.
```