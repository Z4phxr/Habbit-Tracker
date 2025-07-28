from django import template

register = template.Library()

# Red-Yellow-Green gradient for mood values 1-10
def mood_to_color(mood):
    # 1 = red (#d32f2f), 5 = yellow (#ffd600), 10 = green (#43a047)
    stops = [
        (1, (211, 47, 47)),    # red
        (5, (255, 214, 0)),    # yellow
        (10, (67, 160, 71)),  # green
    ]
    if mood is None:
        return '#e0e0e0'
    try:
        mood = int(mood)
    except Exception:
        return '#e0e0e0'
    if mood <= 5:
        c1, c2 = stops[0][1], stops[1][1]
        p = (mood - 1) / (5 - 1)
    else:
        c1, c2 = stops[1][1], stops[2][1]
        p = (mood - 5) / (10 - 5)
    rgb = [round(c1[i] + (c2[i] - c1[i]) * p) for i in range(3)]
    return f'rgb({rgb[0]},{rgb[1]},{rgb[2]})'

@register.filter
def mood_color(mood):
    return mood_to_color(mood)
