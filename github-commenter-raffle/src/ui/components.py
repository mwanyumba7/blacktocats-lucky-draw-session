def render_button(label, id, onclick_function):
    return f'<button id="{id}" onclick="{onclick_function}">{label}</button>'

def render_modal(content, id):
    return f'''
    <div id="{id}" class="modal">
        <div class="modal-content">
            <span class="close" onclick="document.getElementById('{id}').style.display='none'">&times;</span>
            <p>{content}</p>
        </div>
    </div>
    '''

def render_loader():
    return '''
    <div class="loader">
        <p>Loading...</p>
    </div>
    '''