import sys


class View:
    def __init__(self, content, state, only_view_on_errors=False):
        self.content = content
        self.state = state
        self.only_view_on_errors = only_view_on_errors
        self.user_view()

    def user_view(self):
        if self.only_view_on_errors:
            if not self.state:
                return self.print_stderr_content()
        else:
            if self.state:
                return self.print_stdout_content()
            else:
                return self.print_stderr_content()

    def print_stdout_content(self):
        print(self.content, file=sys.stdout)
        return self.content

    def print_stderr_content(self):
        print(self.content, file=sys.stderr)
        return self.content
