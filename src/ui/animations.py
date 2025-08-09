def fade_in(element, duration=500):
    """Fade in animation for a UI element."""
    element.style.opacity = 0
    element.style.display = 'block'
    
    def step(timestamp):
        if not element.style.opacity:
            element.style.opacity = 0
        if element.style.opacity < 1:
            element.style.opacity = parseFloat(element.style.opacity) + (timestamp / duration)
            requestAnimationFrame(step)
    
    requestAnimationFrame(step)

def fade_out(element, duration=500):
    """Fade out animation for a UI element."""
    element.style.opacity = 1
    
    def step(timestamp):
        if element.style.opacity > 0:
            element.style.opacity = parseFloat(element.style.opacity) - (timestamp / duration)
            requestAnimationFrame(step)
        else:
            element.style.display = 'none'
    
    requestAnimationFrame(step)

def animate_winner_selection(winner_element):
    """Animate the winner selection process."""
    fade_in(winner_element)
    setTimeout(lambda: fade_out(winner_element), 3000)  # Keep visible for 3 seconds before fading out