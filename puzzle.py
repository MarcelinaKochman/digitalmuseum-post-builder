import random

def generate_puzzle_svg(cols, rows, piece_width=100, piece_height=100):
    svg_parts = []
    width = cols * piece_width
    height = rows * piece_height
    svg_parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">')

    def create_piece(x, y):
        path = ""
        # Start in top-left corner of piece
        px = x * piece_width
        py = y * piece_height
        path += f'M {px} {py} '

        # Top edge
        if y == 0:
            path += f'h {piece_width} '
        else:
            path += top_tab(px, py, piece_width)

        # Right edge
        if x == cols - 1:
            path += f'v {piece_height} '
        else:
            path += right_tab(px + piece_width, py, piece_height)

        # Bottom edge
        if y == rows - 1:
            path += f'h {-piece_width} '
        else:
            path += bottom_tab(px + piece_width, py + piece_height, piece_width)

        # Left edge
        if x == 0:
            path += f'v {-piece_height} '
        else:
            path += left_tab(px, py + piece_height, piece_height)

        path += 'Z'
        return f'<path d="{path}" stroke="black" fill="white"/>'

    def tab_curve(size, direction):
        arc = size * 0.2
        sweep = 1 if direction == 1 else 0
        return f"a {arc},{arc} 0 0,{sweep} {direction * arc},-{direction * arc} " \
               f"a {arc},{arc} 0 0,{sweep} {direction * arc},{direction * arc} "

    def top_tab(x, y, size):
        return f'h {size * 0.3} ' + tab_curve(size, random.choice([-1, 1])) + f'h {size * 0.3} '

    def right_tab(x, y, size):
        return f'v {size * 0.3} ' + tab_curve(size, random.choice([-1, 1])) + f'v {size * 0.3} '

    def bottom_tab(x, y, size):
        return f'h {-size * 0.3} ' + tab_curve(size, -random.choice([-1, 1])) + f'h {-size * 0.3} '

    def left_tab(x, y, size):
        return f'v {-size * 0.3} ' + tab_curve(size, -random.choice([-1, 1])) + f'v {-size * 0.3} '

    # Generate all pieces
    for y in range(rows):
        for x in range(cols):
            svg_parts.append(create_piece(x, y))

    svg_parts.append('</svg>')
    return '\n'.join(svg_parts)

# Przykład użycia
svg_output = generate_puzzle_svg(cols=3, rows=2)

# Zapisz do pliku
with open("puzzle.svg", "w") as f:
    f.write(svg_output)
