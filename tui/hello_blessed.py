import blessed
term = blessed.Terminal()

with term.fullscreen(), term.cbreak(), term.hidden_cursor():
    print(term.move_y(term.height // 2) +
          term.center('Hello blessed!').rstrip())
    term.inkey()
