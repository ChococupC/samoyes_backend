import textwrap


class DebugModel:
    def __init__(self, model = None, method:str = "UnknownMethod", status=True, **kwargs):
        self.model = model
        self.method = method
        self.status = status
        self.detail = self.detail_create(**kwargs)


    def detail_create(self, **kwargs):
        lines = []
        for k, v in kwargs.items():
            lines.append(f"\t--{k}--:")
            wrapped_lines = textwrap.wrap(str(v).strip(), width=130)
            for line in wrapped_lines:
                lines.append(f"\t\t{line}")
        return "\n".join(lines)

class DebugManager:
    def __init__(self):
        self.enabled = True
        self.records = []

    def add(self, model=None, method:str="", status=True, **kwargs):
        if not model:
            raise ValueError("Model need to be added")
        if self.enabled:
            debug_obj = DebugModel(model=model,method=method,status=status,**kwargs)
            self.records.append(debug_obj)
            return debug_obj

    def display(self):
        if self.enabled:
            print("==== Debug Log ====")
            for i, debug_obj in enumerate(self.records, start=1):
                icon = "✅ Success" if debug_obj.status else "❌ Failed"
                print(f"{i}. {debug_obj.method} for {debug_obj.model}: {icon}")
                print(f"{debug_obj.detail}")
            print("==== End Log ====")
