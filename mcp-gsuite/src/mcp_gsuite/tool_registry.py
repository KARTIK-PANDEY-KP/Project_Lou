from . import toolhandler

tool_handlers = {}

def add_tool_handler(tool_class: toolhandler.ToolHandler):
    global tool_handlers
    tool_handlers[tool_class.name] = tool_class

def get_tool_handler(name: str) -> toolhandler.ToolHandler | None:
    if name not in tool_handlers:
        return None
    
    return tool_handlers[name]

def get_all_tool_handlers() -> dict:
    return tool_handlers 