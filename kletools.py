import json

def parse_kle_positions(layout):
    """
    Generator that takes KLE layout data (list of lists of keys),
    and yields (x, y) positions of each key in the layout.
    """
    y = 0  # Initial Y position
    for row in layout:
        x = 0  # Start X at beginning of row
        i = 0
        while i < len(row):
            key = row[i]
            # Default key size and position offset
            w = h = 1
            x_offset = y_offset = 0

            if isinstance(key, dict):
                # Process key properties (offsets, sizes, etc.)
                x_offset = key.get('x', 0)
                y_offset = key.get('y', 0)
                w = key.get('w', 1)
                h = key.get('h', 1)
                x += x_offset
                y += y_offset
                i += 1
                key = row[i]  # Next item should be the key label (or string)
            # Emit current key's position
            yield (x, y)
            x += w  # Move to next key position
            i += 1
        y += 1  # New row


def parse_kle_stabilizers(layout):
    """
    Generator to yield stabilizer (x, y) positions from KLE JSON data.
    Only yields for keys with width >= 2.
    """

    x, y = 0, 0
    default_key_props = {
        'w': 1, 'h': 1, 'x': 0, 'y': 0
    }

    current_props = default_key_props.copy()

    for row in layout:
        x = 0
        current_props.update(default_key_props)
        for item in row:
            if isinstance(item, dict):
                current_props.update(item)
                continue

            width = current_props.get('w', 1)
            height = current_props.get('h', 1)
            x_offset = current_props.get('x', 0)
            y_offset = current_props.get('y', 0)

            key_x = x + x_offset
            key_y = y + y_offset

            if width >= 2:
                # Assume stabilizer mounts are 0.25 units in from left and right
                stab_left_x = key_x - width / 2 + 0.25
                stab_right_x = key_x + width / 2 - 0.25
                stab_y = key_y+ 0.25 # Center of key vertically

                yield (stab_left_x, stab_y)
                yield (stab_right_x, stab_y)

            # Move x to next key
            x += width
            current_props = default_key_props.copy()
        y += 1  # Move to next row

# Example usage:
# kle_data = '[ [ { "w":2 }, "Shift", "A", "S" ], [ "Z", "X", { "w":2 }, "Enter" ] ]'
# for stab in parse_kle_stabilizers(kle_data):
#     print(stab)

