import gradio as gr


def normal_mode(configs):
    ai_role_options = configs['ai_roles']['Useful']
    return gr.Dropdown.update(choices=ai_role_options, value=ai_role_options[0])


def academic_mode(configs):
    ai_role_options = configs['ai_roles']['Academic']
    return gr.Dropdown.update(choices=ai_role_options, value=ai_role_options[0])


def develop_mode(configs):
    ai_role_options = configs['ai_roles']['Develop']
    return gr.Dropdown.update(choices=ai_role_options, value=ai_role_options[0])


def fun_mode(configs):
    ai_role_options = configs['ai_roles']['Fun']
    return gr.Dropdown.update(choices=ai_role_options, value=ai_role_options[0])
