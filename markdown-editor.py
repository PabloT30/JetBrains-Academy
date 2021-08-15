valid_formatters = ("plain", "bold", "italic", "header", "link"
                    , "inline-code", "ordered-list", "unordered-list", "new-line")

valid_commands = ("!help", "!done")

formatted_text = ""


def plain():
    text = input("- Text:")
    return text


def bold():
    text = "**" + input("- Text:") + "**"
    return text


def italic():
    text = "*" + input("- Text:") + "*"
    return text


def header():
    while True:
        header_level = input("- Level:")
        if header_level.isnumeric() and int(header_level) in list(range(1, 7)):
            break
        else:
            print("The level should be within the range of 1 to 6")
    text = "#" * int(header_level) + " " + input("- Text:") + "\n"
    return text


def link():
    link_label = input("- Label:")
    link_url = input("- URL:")
    text = f"[{link_label}]" + f"({link_url})"
    return text


def inline_code():
    text = "`" + input("- Text:") + "`"
    return text


def list_(order):
    text = ""
    while True:
        user_input = input("- Number of rows:")
        if user_input.isnumeric() and int(user_input) > 0:
            break
        else:
            print("The number of rows should be greater than zero")
    for i in range(int(user_input)):
        if order == "ordered-list":
            text += f"{i + 1}. " + input(f"Row #{i + 1}") + "\n"
        elif order == "unordered-list":
            text += "* " + input(f"Row #{i + 1}") + "\n"
    return text


def new_line():
    text = "\n"
    return text


def prompt_for_input():
    while True:
        user_input = input("- Choose a formatter:")
        if user_input in valid_formatters or user_input in valid_commands:
            if user_input in valid_formatters:
                return user_input
            elif user_input in valid_commands:
                if user_input == valid_commands[0]:  # !help
                    print("""Available formatters: plain bold italic header link inline-code ordered-list unordered-list new-line
                    Special commands: !help !done""")
                elif user_input == valid_commands[1]:  # !done
                    return "!done"
        else:
            print("Unknown formatting type or command. Please try again.")


def call_formatter(formatter):
    text = ""
    if formatter == valid_formatters[0]:  # plain
        text = plain()
    elif formatter == valid_formatters[1]:  # bold
        text = bold()
    elif formatter == valid_formatters[2]:  # italic
        text = italic()
    elif formatter == valid_formatters[3]:  # header
        text = header()
    elif formatter == valid_formatters[4]:  # link
        text = link()
    elif formatter == valid_formatters[5]:  # inline-code
        text = inline_code()
    elif formatter == valid_formatters[6]:  # ordered-list
        text = list_("ordered-list")
    elif formatter == valid_formatters[7]:  # unordered-list
        text = list_("unordered-list")
    elif formatter == valid_formatters[8]:  # new-line
        text = new_line()
    return text


def add_formatted_text(text):
    global formatted_text
    formatted_text += text


def main():
    while True:
        formatter = prompt_for_input()
        if formatter == "!done":
            output_file = open('output.md', mode='w')
            output_file.write(formatted_text)
            output_file.close()
            break
        text = call_formatter(formatter)
        add_formatted_text(text)
        print(formatted_text)


if __name__ == "__main__":
    main()
